# Viviette — PortMaster / TrimUI Smart Pro S

Port scaffold for **Viviette** on **TrimUI Smart Pro S (TSPS), SpruceOS, AArch64**.
Verified on that device: gameplay, keyboard-mapped controls, and readable English dialogue after the Mali shader precision fix. Other handhelds are not verified.

**This repository does not contain the game, game assets, `game.port`, `libyoyo.so`, personal saves, or commercial archives.** Purchase the game and supply your own legally obtained files. Owning the game does not make an incompatible build compatible with this runner.

## Requirements

- TSPS running SpruceOS with PortMaster installed; launch through the normal PORTS menu.
- A 64-bit ARM system (AArch64), glibc **2.30 or newer**, system SDL2 / OpenGL ES libraries, and a working GPU driver.
- Bash and PortMaster's `control.txt`, platform helper, and `gptokeyb`. These are supplied by the firmware/PortMaster and are not bundled here.
- **Your own already prepared, compatible `game.port`.** The verified configuration uses Switch-variant GameMaker VM data and `force_platform: os_switch`.

### Important game-data limitation

This repository **is not a ready-to-use converter for the retail Windows release**. Copying a stock Steam/GOG `data.win` in place of `game.droid` is not a working installation method: that data did not launch with the available ARM64 runners during earlier tests.

The verified `game.port` already contains prepared game data, including account/viewport changes. This repository does not automate reproducing those transformations from a clean retail dump. If you only have a stock Windows release or an unprocessed Switch dump, this scaffold alone is insufficient: compatible prepared data from your own copy must be obtained separately. No third-party commercial files are distributed here.

The exact verified inputs have these hashes:

```text
assets/game.droid SHA-256:
dc72cfb60db5c32b050970b14d893aebc7dd67e0749a8d34f82b81f6be21d83d

lib/arm64-v8a/libyoyo.so SHA-256 after the font fix:
bd8bb7584b544e8a9830389f9b13a6595fd494966e39a06059b24f00161f7444
```

## Installation

1. Select **Code → Download ZIP**, or clone the repository:
   ```sh
   git clone https://github.com/ruslan-k/viviette-portmaster-tsps.git
   cd viviette-portmaster-tsps
   ```
2. On a computer with Python 3, process **your own compatible, prepared** archive:
   ```sh
   python3 tools/patch_font_precision.py /path/to/your/game.port --output viviette/game.port
   ```
   The helper verifies the known game-data and runner versions, changes only two GLSL declarations from `mediump` to `highp`, checks ZIP integrity, and leaves game data unchanged. Already patched archives are supported. Unknown builds are rejected, and existing output files are never overwritten. This is **not** a game-data converter.
3. Copy **`Viviette.sh` and the entire `viviette` directory** into the SD card's PORTS directory. The verified SpruceOS installation uses `/mnt/SDCARD/Roms/ports/`. Preserve filename spelling and case:
   ```text
   Roms/ports/
   ├── Viviette.sh
   └── viviette/
       ├── game.port                 # your own game archive
       ├── gmloader.json
       ├── gmloadernext.aarch64
       ├── viviette.gptk
       ├── lib/arm64-v8a/
       │   ├── libc++_shared.so
       │   ├── libcompiler_rt.so
       │   └── libm.so
       └── saves/
   ```
4. If the filesystem supports Unix permissions:
   ```sh
   chmod +x /mnt/SDCARD/Roms/ports/Viviette.sh
   chmod +x /mnt/SDCARD/Roms/ports/viviette/gmloadernext.aarch64
   ```
   On FAT, use SpruceOS's normal mount settings; the launcher also sets the loader's executable permission.
5. Refresh the game list and launch **Viviette from the PORTS menu**. Do not start the payload directly over SSH: the menu must release the display/audio through SpruceOS's normal principal launch flow.

The game files `assets/game.droid` and `assets/options.ini` are already **inside `game.port`**. A separate external `assets/` directory is not required by this configuration. The launcher locates the ports directory through PortMaster's `$directory` variable rather than a hardcoded device path.

Existing saves can be copied separately into `viviette/saves/` while the game is closed. Do not remove this directory when updating the port. Personal saves are not included here.

## Controls

The current mapping uses `gptokeyb`, which emulates keyboard input:

- D-pad / left stick — movement (arrow keys).
- A → Z — confirm / interact.
- B → X — back / cancel.
- X → A, Y → S.
- Start → Enter; Select → Escape.
- L1 → Page Up; R1 → Page Down.

These are the button-to-key assignments in the configuration, not a guarantee of a specific in-game action for every key. Button names follow PortMaster's naming; physical labels may differ on other devices.

## Font rendering fix

The verified runner's default GLSL uses `precision mediump float;`. With a 4096×4096 atlas on Mali, small glyph coordinates were rounded, clipping or duplicating individual columns. Replacing two declarations with the equal-length string `precision highp   float;` resolved the defect while preserving normal spacing and game textures.

Expanding glyph sprite frames to 16×16 was an unsuccessful experiment: it increased character spacing. **That experiment is not included in this port.**

## Troubleshooting and verification limits

- Launch log: `viviette/log.txt`, recreated on every launch.
- `control.txt` / platform-helper errors: first check PortMaster installation and normal menu-based launching.
- Shared-library / GLIBC errors: check the AArch64 architecture and firmware libraries. This binary does not support ARMv7 or x86.
- Corrupted text: check that the prepared `game.port` with the patched ARM64 runner is being used.
- Audio is not claimed to be fixed by this port: the observed TSPS log contained the ALSA error `Unknown PCM Playback`. The font patch does not change audio; verify the target device's ALSA route separately.
- Compatibility, performance, and save/load behavior on another device must be tested separately.

## Verify scaffold files

```sh
sha256sum -c SHA256SUMS
python3 -m unittest discover -s tests -v
bash -n Viviette.sh
```

`SHA256SUMS` covers the repository's scaffold files, not your personal `game.port`.

## Credits / licensing

- Game: **DYA Games / Viviette**. All game data and the proprietary game runner must be supplied by the owner; none are hosted here.
- Loader: [JohnnyonFlame/gmloader-next](https://github.com/JohnnyonFlame/gmloader-next), [ruslan-k/gmloader-next](https://github.com/ruslan-k/gmloader-next), GPL-2.0. GPL text: `licenses/gmloader-next-GPL-2.0.txt`.
- PortMaster: https://github.com/PortsMaster/PortMaster.
- Runtime support libraries are third-party Android/NDK components, not game assets. See `THIRD_PARTY.md` for source and license references and binary hashes.

The binaries are the tested files from the installed TSPS port. An exact compiler/source-revision mapping for these pre-existing binaries has not been independently established; no reproducible-build claim is made.
