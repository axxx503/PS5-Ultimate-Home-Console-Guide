# USB paths and verified outcomes — v1.3.0

This file mirrors the tested state documented in the current Visual Edition.

| Emulator / tool | Path | Tested outcome |
|---|---|---|
| **ProsperoEden / Nintendo Switch** | `/mnt/usb0/PPSA99008/assets/` | **Confirmed working** — `prod.keys` detected, 238 NCA firmware files detected, and a game detected/launched in the tested setup |
| **PS5SX2 / PS2** | `/mnt/usb0/games/`, `/mnt/usb0/PCSX2/games/`, or `/mnt/usb0/PS5SX2/games/` | **Confirmed working** |
| **Porpoise / Dolphin** | External USB library supported; tested setup ultimately worked after the sandbox/daemon work | **Confirmed working** |
| **PS5CEMU-HAR / Wii U + 3DS** | `/mnt/usb0/homebrew/PPSA99360/roms/3ds/` and `roms/wiiu/` | **Confirmed working** — 3DS library detected and Ocarina of Time 3D launched; Wii U path configured |
| **PS5X360 / Xbox 360** | `/mnt/usb0/homebrew/PPSA50011/assets/roms/` or a readable USB game folder | **Confirmed working** — Tenchu Z reached its title screen |
| **XPSemu / Original Xbox** | `/mnt/usb0/xemu/games/` | **Partial / unresolved** — USB discovery works; Otogi still stops on a black screen/no-frames condition |
| **RetroArch** | Current guide documents the internal layout | **Not tested yet in this setup** |
| **PS3** | N/A | **No normal ready-to-use PS3 emulator is included in this setup** |
| **PS5 App Dumper** | `/mnt/usb0/homebrew/ps5-app-dumper/dumps/` | Demon's Souls `PPSA01341` dump located successfully |

## ProsperoEden — tested USB compatibility layout

The working session used the legacy-compatible `assets` layout inside the USB-mounted title:

```text
/mnt/usb0/PPSA99008/
└── assets/
    ├── keys/
    │   └── prod.keys
    ├── firmware/
    │   └── *.nca
    ├── roms/
    │   ├── *.xci
    │   └── *.nsp
    └── updates/
        └── *.nsp
```

Inside the app this is exposed as `/app0/assets`. This is the path that removed the missing-keys problem in the tested setup.

## Exact title migration workflow

1. Copy the complete `PPSAxxxxx` title folder to the USB location used by ShadowMountPlus.
2. Verify the whole title exists — `eboot.bin`, `sce_sys`, `sce_module` and runtime files when applicable. Do not copy only `eboot.bin`.
3. Preserve the internal copy in `/data/homebrew_backup/` until the USB-backed title is proven working.
4. After a **title/helper/application change**, perform one **full Shutdown** (not Rest Mode). Game-only copies normally do not need another shutdown.
5. Boot, reload the exploit chain, etaHEN/kstuff, any title-specific helper, then ShadowMountPlus.
6. Launch the title and verify the USB-backed `/app0` before moving a whole library.
7. Keep rollback copies until the USB build is proven stable.

## WFM ZIP helper

If Web File Manager says `WFM 7zip helper is not running`, importing `wfm-7zip-helper.elf` is not the same as running it. Load the helper for the current session, or extract the archive on the PC and upload/move the resulting folder.

## XPSemu stop point

- `/data/xemu` contains the user-owned MCPX ROM, BIOS, HDD image and logs.
- Games were discovered at `/mnt/usb0/xemu/games`.
- Full disc images must be converted to XISO-compatible images.
- Otogi XISO reached program `46530002`, then `FFFF0002`; the log reported `no frames from the game for 15 s`.
- `imports.txt errno 2` appeared but has not been proven causal.
- Status remains **UNRESOLVED**. Do not reinstall the entire chain blindly.

## PS5 App Dumper output

During dumping, the source can appear under `/mnt/sandbox/pfsmnt/PPSAxxxxx-app0`, but the completed tested output was under:

```text
/mnt/usb0/homebrew/ps5-app-dumper/dumps/
  PPSA01341-app0_Demon's_Souls/
  PPSA01341-app0_Demon's_Souls.dump-info.json
  log.txt
```

The folder is the actual dump. The JSON file is metadata and `log.txt` is the operation log.
