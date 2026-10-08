#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIND="${1:-}"
if [[ ! "$KIND" =~ ^(cemu|porpoise|xpsemu|x360|all)$ ]]; then
  echo "usage: $0 {cemu|porpoise|xpsemu|x360|all}" >&2
  exit 2
fi
BASE="$HOME/ps5-usb-patched"
mkdir -p "$BASE"
clone_clean(){
  local url="$1" dir="$2" tag="${3:-}"
  if [[ -e "$dir" ]]; then
    echo "REFUSED: existing work directory $dir; do not erase previous builds." >&2
    echo "Continue manually from that source, or rename/backup the directory yourself before starting fresh." >&2
    exit 4
  fi
  git clone "$url" "$dir"
  if [[ -n "$tag" ]]; then (cd "$dir" && git checkout "$tag"); fi
}

build_cemu(){
  local R="$BASE/PS5CEMU-HAR"
  echo "== PS5CEMU-HAR v3.0.0 =="
  clone_clean https://github.com/premohq/PS5CEMU-HAR.git "$R" v3.0.0
  python3 "$HERE/scripts/patch_repo.py" cemu "$R"
  (cd "$R" && make release)
  local P="$R/build/app/PPSA99360"
  python3 "$HERE/scripts/postbuild_layout.py" cemu "$P"
  echo "READY: $P"
}

build_porpoise(){
  local R="$BASE/Porpoise"
  echo "== Porpoise v2.5 =="
  clone_clean https://github.com/elripalda/Porpoise-Dolphin-Emulator-for-PS5.git "$R" v2.5
  python3 "$HERE/scripts/patch_repo.py" porpoise "$R"
  # Uses the PS5_PayloadSDK / PS5_Vulkan / PS5_Mesa environment already prepared on this WSL.
  (cd "$R" && make app)
  local P="$R/dist/PPSA99764"
  python3 "$HERE/scripts/postbuild_layout.py" porpoise "$P"
  echo "READY: $P"
}

build_xpsemu(){
  local R="$BASE/XPSemu"
  echo "== XPSemu main =="
  clone_clean https://github.com/ZiZc3/XPSemu.git "$R"
  python3 "$HERE/scripts/patch_repo.py" xpsemu "$R"
  export PS5_VULKAN="${PS5_VULKAN:-$HOME/PS5_Vulkan}"
  export PS5_PAYLOAD_SDK="${PS5_PAYLOAD_SDK:-$PS5_VULKAN/.deps/native/ps5-payload-sdk}"
  export RADV_ARCHIVE="${RADV_ARCHIVE:-$PS5_VULKAN/.deps/native/radv-release/lib/libvulkan_radeon.ps5.a}"
  (cd "$R" && bash ps5/deps/build-deps.sh compat zlib libiconv glib pixman libsamplerate sdl3 vulkan libpcap curl libslirp)
  (cd "$R" && bash ps5/configure-ps5.sh)
  (cd "$R" && ninja -C build-ps5 qemu-system-i386 || true)
  (cd "$R" && bash ps5/build-title.sh)
  local P="$R/dist/PPSA97358"
  python3 "$HERE/scripts/postbuild_layout.py" xpsemu "$P"
  echo "READY: $P"
}

build_x360(){
  local R="$BASE/PS5X360"
  echo "== PS5X360 current main =="
  clone_clean https://github.com/BrinooTk/PS5X360.git "$R"
  python3 "$HERE/scripts/patch_repo.py" x360 "$R"
  echo
  echo "PS5X360 source is prepared, but its official BUILD.md requires a prepared native runtime + PS5_Vulkan reference tree."
  echo "Source ready at: $R"
  echo "For USB game storage no executable patch is actually required: current source already uses /app0/assets/roms."
  echo "Mount the complete PPSA50011 folder from USB and put games under assets/roms."
}

case "$KIND" in
  cemu) build_cemu;; porpoise) build_porpoise;; xpsemu) build_xpsemu;; x360) build_x360;;
  all) build_cemu; build_porpoise; build_xpsemu; build_x360;;
esac
