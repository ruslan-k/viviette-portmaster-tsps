# Third-party components

Only the port scaffold and service/runtime components are distributed. Game data, images, music, sounds, `game.port`, and YoYo's proprietary `libyoyo.so` are intentionally excluded.

## GMLoader-next

- `viviette/gmloadernext.aarch64` is the tested AArch64 loader.
- Upstream: https://github.com/JohnnyonFlame/gmloader-next
- User fork: https://github.com/ruslan-k/gmloader-next
- License: GPL-2.0 (upstream license is included under `licenses/`).
- SHA-256: `7202c9b32d04b6ffd5a3e5264c136281867f3913e99cf7322b4125b8043a4add`.
- Source links identify the project, not a proven corresponding source revision for this pre-existing binary. Exact build provenance has not been recovered.

## Android/NDK support libraries

These are copied unchanged from the installed, working port's external ARM64 support directory. They are not the commercial game engine. They are deliberately kept separate from system Linux libraries; do not substitute host `libm.so.6` for Android `libm.so`.

- `libc++_shared.so`: Android NDK / LLVM libc++ family. Upstream sources and notices: https://github.com/llvm/llvm-project/tree/main/libcxx and https://android.googlesource.com/platform/ndk/ . Applicable license text depends on the original NDK version; exact NDK provenance of the supplied binary is not established.
- `libcompiler_rt.so`: compiler runtime support. Source families: https://github.com/llvm/llvm-project/tree/main/compiler-rt and https://android.googlesource.com/platform/ndk/ . Exact originating version is not established.
- `libm.so`: Android math runtime (Bionic/OpenBSD-derived components). Source and per-file license notices: https://android.googlesource.com/platform/bionic/ . Bionic's notices include BSD-style and other component-specific licenses; this is not represented as a single blanket license.

The external libc++ file differs from the embedded libc++ in the owner-supplied game archive; do not silently replace one with the other. `SHA256SUMS` records the tested external files.

## PortMaster

PortMaster control scripts, platform helpers and gptokeyb are provided by the installed PortMaster/firmware; they are not vendored here. Source: https://github.com/PortsMaster/PortMaster .

## No blanket relicensing

No repository-wide license is applied to third-party binaries or proprietary inputs. Existing upstream/component licenses continue to apply. The font helper contains only a transformation of owner-supplied inputs, hashes and shader declaration strings, not game data.
