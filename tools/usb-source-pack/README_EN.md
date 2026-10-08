# PS5 USB Emulator Source Pack (tested CEMU workflow)

This source-only helper switches game-library defaults to `/app0/roms/3ds` and `/app0/roms/wiiu` for PS5CEMU-HAR v3.0.0, intended for USB-backed app folders registered by ShadowMountPlus. Writable data remains under `/data/ps5cemu`.

On WSL, unpack to `C:\PS5_USB_Emulators_Source_Pack`, then `cd /mnt/c/PS5_USB_Emulators_Source_Pack` and run `bash build_usb_patched.sh cemu`.

If `Azahar` stops on missing submodules, run:

```sh
cd ~/ps5-usb-patched/PS5CEMU-HAR/.deps/PS5_Azahar
git submodule update --init --recursive
cd ~/ps5-usb-patched/PS5CEMU-HAR
bash tools/build-azahar.sh --reconfigure
make release
python3 /mnt/c/PS5_USB_Emulators_Source_Pack/scripts/postbuild_layout.py cemu build/app/PPSA99360
```

**Safety:** The builder now REFUSES to replace an existing clone. Do not relaunch it after a partial build. The other emulator targets are experimental source tooling; no executable compatibility or build success is claimed. Never include BIOS, keys, saves, game dumps or third-party prebuilt app binaries in GitHub.
