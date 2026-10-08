import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'patch_font_precision.py'

class FontPatchTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'font precision patch helper is missing')
        spec = importlib.util.spec_from_file_location('font_patch', SCRIPT)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_patch_preserves_length_and_other_bytes(self):
        old = b'prefix\0precision mediump float;\0middle\0precision mediump float;\0suffix'
        fixed, count = self.mod.patch_precision(old)
        self.assertEqual(count, 2)
        self.assertEqual(len(fixed), len(old))
        self.assertEqual(fixed, old.replace(b'precision mediump float;', b'precision highp   float;'))

    def test_already_patched_is_idempotent(self):
        data = b'precision highp   float;\0precision highp   float;'
        self.assertEqual(self.mod.patch_precision(data), (data, 0))

    def test_unrecognized_shader_layout_is_rejected(self):
        for data in [b'', b'precision mediump float;', b'precision mediump float;' * 3]:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self.mod.patch_precision(data)

if __name__ == '__main__':
    unittest.main()
