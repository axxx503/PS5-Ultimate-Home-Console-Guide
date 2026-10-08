#!/usr/bin/env python3
from pathlib import Path
import sys
if len(sys.argv)!=3:
    raise SystemExit('usage: postbuild_layout.py {cemu|porpoise|xpsemu|x360} PPSA_DIR')
kind=sys.argv[1]; root=Path(sys.argv[2]).resolve()
if not root.exists(): raise SystemExit(f'not found: {root}')
def keep(p, text):
    p.mkdir(parents=True, exist_ok=True)
    (p/'PUT_YOUR_OWN_GAMES_HERE.txt').write_text(text+'\n', encoding='utf-8')
if kind=='cemu':
    keep(root/'roms'/'wiiu','Wii U: WUA/WUD/WUX or unpacked code/content/meta folders.')
    keep(root/'roms'/'3ds','3DS: direct-play dumps such as 3DS/CCI/CXI/3DSX. CIA installs remain under /data.')
elif kind=='porpoise':
    keep(root/'roms','GameCube/Wii disc backups (ISO/RVZ and formats supported by Porpoise).')
elif kind=='xpsemu':
    keep(root/'roms','Original Xbox XISO images. Keep BIOS/MCPX/HDD under /data/xemu.')
elif kind=='x360':
    keep(root/'assets'/'roms','Xbox 360 games: one folder per game, matching PS5X360 documentation.')
else: raise SystemExit('unknown emulator')
print(root)
