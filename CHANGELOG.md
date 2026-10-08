# Changelog

All notable public changes to this guide are documented here.

## [1.3.0] - 2026-10-08

### Added
- Added **Nintendo Switch / ProsperoEden** to the Visual Edition as a confirmed-working emulator in the tested firmware 13.40 setup.
- Documented the tested ProsperoEden identity: `PPSA99008`, session build `v1.000.070`.
- Added the USB compatibility layout that worked in practice: `/mnt/usb0/PPSA99008/assets/` exposed inside the app as `/app0/assets`.
- Documented successful detection of `prod.keys`, **238 NCA** firmware files, and a game in the Switch library.
- Archived the detailed ProsperoEden session guide under `docs/reference/`.

### Corrected status tracking
- PS5SX2: confirmed working.
- Porpoise / Dolphin: confirmed working in the tested setup.
- PS5CEMU-HAR: confirmed working; 3DS library and Ocarina of Time 3D were tested, with Wii U configured.
- PS5X360: confirmed working; Tenchu Z reached its title screen.
- XPSemu: remains partial/unresolved at the Otogi black-screen/no-frames stage.
- RetroArch: documented but not tested yet in this setup.
- PS3: no normal ready-to-use emulator is included in the tested stack.

### Updated
- Replaced the repository DOCX/PDF with the current Visual Edition containing the Switch section.
- Updated README, USB notes, release notes, preview images, and version metadata to match the current Visual Edition.

## [1.2.0] - 2026-10-08

- Merged the legacy bilingual PS5 Homebrew & Emulator Project Knowledge Base into the maintained guide and archived the original source under `docs/reference/`.
- Added etaHEN/Porpoise Legacy Jailbreak CMD Server history, sandbox diagnosis, emulator state matrix, and a reusable troubleshooting/continuation contract.
- Added the exact USB title migration/rollback/full-Shutdown workflow used in the tested setup.
- Added Web File Manager 7zip-helper runtime behavior and fallback extraction workflow.
- Expanded XPSemu Alpha 2 notes through XISO conversion and the Otogi black-screen/no-frames stop point.
- Added PS5 App Dumper output locations and the tested PPSA01341 Demon's Souls dump layout.

## [1.1.0] - 2026-10-08

- Documented working USB-backed 3DS and Xbox 360 title folders with verified paths.
- Added the WSL/CEMU v3.0.0 source-build procedure and Azahar submodule recovery.
- Added exact rollback and full Shutdown flow after title moves, not after each game copy.
- Added a PC-only release check/staging app; no unattended PS5 installations.

## [1.0.0] - 2026-10-07

- First public English Visual Edition.
- Visual 16:9-style page layout focused on readability.
- Firmware 13.40 tested workflow notes.
- Homebrew chain, Remote Play, file tools, emulator sections, storage strategy, and troubleshooting.
- Public/privacy-safe wording with no personal IP addresses, account IDs, or pairing credentials.
