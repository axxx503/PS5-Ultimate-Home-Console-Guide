# PS5 Release Tracker — PC companion

This is a small Python app for your PC. It checks latest official GitHub releases and optionally downloads an asset into `staging/` after approval. It NEVER writes to your PS5, USB drive or installed emulators; it does not auto-install.

Run `Run-Updater.bat` on Windows (Python 3 with Tkinter) or `python3 updater.py --lang en` on Linux. Headless mode: `python3 updater.py --check`; optional staging: `python3 updater.py --stage x360`.

The locally calculated SHA-256 is an integrity record, **not** proof of publisher authenticity. Review upstream notes and published signatures/hashes, back up your titles, then install manually after verifying custom `/app0` paths survive. Source ZIPs and prebuilt binaries are not bundled here.

This tool is NOT an updater embedded in the PS5 emulator. ShadowMountPlus `update_emulators` refers to fakelib component replacement, not these full titles.
