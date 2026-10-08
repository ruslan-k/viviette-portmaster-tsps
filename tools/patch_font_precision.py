#!/usr/bin/env python3
"""Apply the verified Viviette Mali font fix to an owner-supplied game.port.

This is not a Windows/Switch game-data converter. No game files are embedded.
"""
import argparse
import hashlib
import io
from pathlib import Path
import struct
import zipfile

GAME_SHA256 = 'dc72cfb60db5c32b050970b14d893aebc7dd67e0749a8d34f82b81f6be21d83d'
FIXED_RUNNER_SHA256 = 'bd8bb7584b544e8a9830389f9b13a6595fd494966e39a06059b24f00161f7444'
OLD = b'precision mediump float;'
NEW = b'precision highp   float;'
RUNNER = 'lib/arm64-v8a/libyoyo.so'


def patch_precision(data):
    count = data.count(OLD)
    if count == 2 and data.count(NEW) == 0:
        return data.replace(OLD, NEW), count
    if count == 0 and data.count(NEW) == 2:
        return data, 0
    raise ValueError('Unrecognized GLSL layout; expected two original or two patched declarations')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True,
                        help='New archive; existing files are never overwritten')
    args = parser.parse_args()
    try:
        with zipfile.ZipFile(args.source) as source:
            if source.testzip() is not None:
                raise ValueError('Source ZIP failed its CRC test')
            if len(source.namelist()) != len(set(source.namelist())):
                raise ValueError('Duplicate archive entry names')
            game = source.read('assets/game.droid')
            if len(game) < 8 or game[:4] != b'FORM' or struct.unpack_from('<I', game, 4)[0] + 8 != len(game):
                raise ValueError('Invalid FORM container (or untrimmed overlay)')
            if hashlib.sha256(game).hexdigest() != GAME_SHA256:
                raise ValueError('Unsupported game data: use the already prepared, verified Viviette port data; stock data.win is not supported')
            patched, count = patch_precision(source.read(RUNNER))
            if hashlib.sha256(patched).hexdigest() != FIXED_RUNNER_SHA256:
                raise ValueError('Unsupported runner version; no output written')
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w') as dest:
                for info in source.infolist():
                    dest.writestr(info, patched if info.filename == RUNNER else source.read(info.filename))
        with zipfile.ZipFile(io.BytesIO(buffer.getvalue())) as check:
            if check.testzip() is not None or check.read('assets/game.droid') != game:
                raise ValueError('Output verification failed')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as output:
            output.write(buffer.getvalue())
        print('Shader declarations changed:', count)
        print('Game data unchanged; output ZIP verified')
        print('Saved:', args.output)
        print('SHA-256:', hashlib.sha256(buffer.getvalue()).hexdigest())
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
