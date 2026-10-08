#!/usr/bin/env python3
from pathlib import Path
import sys

CODE_EXTS = {'.c','.cc','.cpp','.cxx','.h','.hh','.hpp','.hxx','.inl','.m','.mm','.py','.sh','.cmake','.txt'}
SKIP_DIRS = {'.git','build','dist','.deps','third_party','external','vendor','subprojects'}

def iter_code(root: Path):
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in CODE_EXTS:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p

def replace_literal(root: Path, old: str, new: str, preferred_parts=()):
    hits=[]
    candidates=[]
    for p in iter_code(root):
        rel=p.relative_to(root)
        if preferred_parts and not any(part in rel.parts for part in preferred_parts):
            continue
        try:
            s=p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        n=s.count(old)
        if n:
            p.write_text(s.replace(old,new), encoding='utf-8')
            hits.append((str(rel),n,old,new))
    return hits

def find_literal(root: Path, needle: str):
    hits=[]
    for p in iter_code(root):
        rel=p.relative_to(root)
        try: s=p.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        n=s.count(needle)
        if n: hits.append((str(rel),n))
    return hits

def write_report(root: Path, title: str, entries, notes):
    rp=root/'PATCH_REPORT.txt'
    lines=[f'{title} USB /app0 source patch', '='*72, '']
    if entries:
        lines.append('Changed source literals:')
        for f,n,o,nn in entries:
            lines += [f'- {f}: {n} occurrence(s)', f'    {o}', f' -> {nn}']
    else:
        lines.append('No literal replacements were made.')
    lines += ['', 'Notes:'] + [f'- {x}' for x in notes]
    rp.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(rp)

def patch_cemu(root):
    entries=[]
    # Keep all writable /data/ps5cemu paths untouched; only game-library defaults move to app0.
    entries += replace_literal(root, '/data/ps5cemu/azahar/games', '/app0/roms/3ds', ('port','patches'))
    entries += replace_literal(root, '/data/ps5cemu/games', '/app0/roms/wiiu', ('port','patches'))
    if not any(e[2]=='/data/ps5cemu/games' for e in entries):
        raise SystemExit('CEMU patch refused: source literal /data/ps5cemu/games was not found in port/ or patches/.')
    if not any(e[2]=='/data/ps5cemu/azahar/games' for e in entries):
        raise SystemExit('CEMU patch refused: source literal /data/ps5cemu/azahar/games was not found in port/ or patches/.')
    write_report(root,'PS5CEMU-HAR',entries,[
        'Wii U direct game files default to /app0/roms/wiiu.',
        '3DS direct game files default to /app0/roms/3ds.',
        'Writable state remains under /data/ps5cemu.',
        'For USB-backed /app0, install/mount PPSA99360 itself from /mnt/usb0/homebrew/PPSA99360.'
    ])

def patch_porpoise(root):
    entries=[]
    entries += replace_literal(root, '/data/porpoise/games', '/app0/roms', ('src','config'))
    if not entries:
        raise SystemExit('Porpoise patch refused: /data/porpoise/games was not found in src/ or config/.')
    write_report(root,'Porpoise',entries,[
        'Primary game-library location becomes /app0/roms.',
        'Saves, covers, settings and caches remain under /data/porpoise.',
        'This mode does not require /mnt to be visible to read games when the app itself is mounted from USB.'
    ])

def patch_xpsemu(root):
    entries=[]
    entries += replace_literal(root, '/data/xemu/games', '/app0/roms', ('ps5','ui','src'))
    if not entries:
        # Some revisions keep the default in a generated/embedded config. Search whole source once, but never docs/build output.
        entries += replace_literal(root, '/data/xemu/games', '/app0/roms')
    if not entries:
        raise SystemExit('XPSemu patch refused: /data/xemu/games was not found in source files.')
    write_report(root,'XPSemu',entries,[
        'Game ISOs/XISOs default to /app0/roms.',
        'BIOS, MCPX, writable HDD image, saves, cache and settings remain under /data/xemu.',
        'Mount PPSA97358 itself from USB so /app0/roms is physically on the external drive.'
    ])

def patch_x360(root):
    present=find_literal(root,'/app0/assets/roms')
    seed=root/'assets'/'game_paths.txt'
    seed.parent.mkdir(parents=True, exist_ok=True)
    seed.write_text('/app0/assets/roms\n', encoding='utf-8')
    entries=[]
    write_report(root,'PS5X360',entries,[
        f'Current source references /app0/assets/roms in {len(present)} source file(s).',
        'No path replacement is necessary: current PS5X360 already supports /app0/assets/roms.',
        'assets/game_paths.txt was written to seed /app0/assets/roms explicitly.',
        'Mount PPSA50011 itself from USB; assets/roms then lives on USB while appearing as /app0/assets/roms.'
    ])

if len(sys.argv)!=3:
    raise SystemExit('usage: patch_repo.py {cemu|porpoise|xpsemu|x360} REPO')
kind=sys.argv[1]
root=Path(sys.argv[2]).resolve()
if not root.exists(): raise SystemExit(f'not found: {root}')
{'cemu':patch_cemu,'porpoise':patch_porpoise,'xpsemu':patch_xpsemu,'x360':patch_x360}[kind](root)
