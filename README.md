<p align="center">
  <img src="assets/github-banner.png" alt="PS5 Ultimate Home Console Guide - English Edition" width="100%">
</p>

<p align="center">
  <img alt="Edition" src="https://img.shields.io/badge/Edition-English-2d69f5">
  <img alt="Firmware" src="https://img.shields.io/badge/Primary%20Firmware-13.40-16a36b">
  <img alt="Version" src="https://img.shields.io/badge/Version-1.3.0-7753f5">
  <img alt="Updated" src="https://img.shields.io/badge/Updated-Oct%202026-314567">
  <img alt="License" src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-d58b00">
</p>

<p align="center"><strong>A visual, beginner-friendly PS5 homebrew and emulation guide built from a real firmware 13.40 setup.</strong></p>

<p align="center">
  <a href="docs/PS5-Ultimate-Home-Console-Guide-EN.pdf"><strong>Download PDF</strong></a> ·
  <a href="docs/PS5-Ultimate-Home-Console-Guide-EN.docx">DOCX</a> ·
  <a href="https://github.com/axxx503/PS5-Ultimate-Home-Console-Guide-AR">العربية</a>
</p>

---

## New in v1.3.0 — Nintendo Switch / ProsperoEden

> **Confirmed in the tested setup:** ProsperoEden ran on firmware 13.40 and successfully detected the user's own Switch keys, firmware data, and game library.

- Added **Nintendo Switch / ProsperoEden** to the Visual Edition.
- Tested title ID: `PPSA99008`; session build: `v1.000.070`.
- Working USB compatibility layout: `/mnt/usb0/PPSA99008/assets/`, exposed inside the app as `/app0/assets`.
- Confirmed: `prod.keys` detected, **238 NCA** firmware files detected, and a game detected/launched.
- Added the detailed ProsperoEden session record to `docs/reference/`.
- Updated the emulator status matrix to match the real test history.

[**Exact USB runbook**](docs/USB-READ-ME.md) · [**ProsperoEden session guide**](docs/reference/ProsperoEden-PS5-Complete-Guide-AR.pdf) · [**USB source patch pack**](tools/usb-source-pack/) · [**PC release tracker**](tools/release-tracker/)

## What this project is

This repository contains the **English Visual Edition** of the *PS5 Ultimate Home Console Guide*. Each page focuses on one task, decision, warning, or troubleshooting flow rather than reading like a dense technical manual.

The guide is centered on a **tested PS5 firmware 13.40 workflow**. Homebrew changes quickly, so re-check upstream release notes before applying a step to another firmware or newer build.

## Download

| Format | Best for | File |
|---|---|---|
| **PDF** | Reading, mobile, printing, sharing | [Download the PDF](docs/PS5-Ultimate-Home-Console-Guide-EN.pdf) |
| **DOCX** | Editing, archiving, adapting the guide | [Download the DOCX](docs/PS5-Ultimate-Home-Console-Guide-EN.docx) |

## Preview

<table>
<tr>
<td width="50%"><img src="assets/preview-01.png" alt="Guide cover"></td>
<td width="50%"><img src="assets/preview-02.png" alt="Priority map"></td>
</tr>
<tr>
<td width="50%"><img src="assets/preview-03.png" alt="Nintendo Switch / ProsperoEden section"></td>
<td width="50%"><img src="assets/preview-04.png" alt="Troubleshooting checklist"></td>
</tr>
</table>

## What the guide covers

- **Base homebrew chain:** WebKit entry, WebKit Autoloader, Payload Manager, etaHEN and kstuff.
- **File and title tools:** Web File Manager, ShadowMountPlus, installable-release vs source-code checks.
- **Remote Play:** chiaki-ng and the local ActRemoteLink workflow.
- **Nintendo Switch:** ProsperoEden, tested USB `assets` layout, keys/firmware/game detection.
- **Emulation:** PS5SX2, Porpoise, PS5CEMU-HAR, PS5X360, XPSemu, RetroArch / PSP.
- **Storage strategy:** when external USB is supported and when sandbox restrictions matter.
- **Troubleshooting:** real failure modes, logs, checks, and the fastest order to diagnose them.

## Tested-status snapshot

| Platform / emulator | Current project status |
|---|---|
| Nintendo Switch — ProsperoEden | **Confirmed working** |
| PS2 — PS5SX2 | **Confirmed working** |
| GameCube / Wii — Porpoise | **Confirmed working** |
| Wii U / 3DS — PS5CEMU-HAR | **Confirmed working** |
| Xbox 360 — PS5X360 | **Confirmed working** |
| Original Xbox — XPSemu | **Partial / unresolved** |
| RetroArch | **Not tested yet** |
| PS3 | **No normal ready-to-use emulator in this tested stack** |

## Status labels used in the guide

| Label | Meaning |
|---|---|
| **Confirmed** | Worked in the tested setup. |
| **Upstream** | Comes from the project's own documentation or release notes. |
| **Unresolved** | Observed or investigated, but not presented as a guaranteed fix. |

## Tested environment

- Primary firmware: **PS5 13.40**
- Edition date: **October 2026**
- Intended use: public, privacy-safe documentation
- Large game libraries remain external wherever the emulator supports it

## Safety, ownership, and legal use

Use only backups, BIOS/firmware files, keys, and game content that you are legally entitled to use and that you obtained from hardware/software you own. This repository does **not** distribute games, BIOS files, firmware dumps, console keys, account credentials, or private pairing data.

Back up saves before changing account activation state, save associations, emulator storage, or other system data.

## Referenced upstream projects

- [PS5 WebKit Autoloader](https://github.com/itsPLK/ps5-webkit-autoloader)
- [PS5 Payload Manager](https://github.com/itsPLK/ps5-payload-manager)
- [etaHEN](https://github.com/etaHEN/etaHEN)
- [etaHEN Unified 11.00-13.60](https://github.com/GronedWaffel/etahen-11.00-13.60)
- [ShadowMountPlus](https://github.com/jakovasaur/ShadowMountPlus)
- [ActRemoteLink](https://github.com/francoataffarel/ActRemoteLink)
- [chiaki-ng](https://streetpea.github.io/chiaki-ng/)
- [ProsperoEden](https://github.com/A1vinSmith/prosperoeden)
- [PS5SX2](https://github.com/Swordpdf/PS5SX2)
- [Porpoise](https://github.com/elripalda/Porpoise-Dolphin-Emulator-for-PS5)
- [PS5CEMU-HAR](https://github.com/premohq/PS5CEMU-HAR)
- [PS5X360](https://github.com/BrinooTk/PS5X360)
- [XPSemu](https://github.com/ZiZc3/XPSemu)
- [PS5 RetroArch](https://github.com/mihawk-99/PS5_RetroArch)
- [GoldHEN](https://github.com/GoldHEN/GoldHEN) — referenced only to clarify that it is a PS4 project

## Corrections and contributions

Found an outdated path, changed release behavior, or a better upstream source? Open an issue using the correction template. Include the **page/section**, **firmware**, **project version**, and a link to the relevant upstream documentation when possible.

See [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

## Versioning

Current public edition: **v1.3.0**. See [CHANGELOG.md](CHANGELOG.md).

## License

Guide text and original visual layout are released under **CC BY-NC-SA 4.0**. Third-party names, trademarks, software, and linked materials retain their own licenses and ownership. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).

## Support

If this guide saved you time and you want to support future documentation and localization work: [Buy Me a Coffee](https://buymeacoffee.com/axxx503).

---

<p align="center"><sub>Not affiliated with Sony Interactive Entertainment or any referenced homebrew/emulator project.</sub></p>
