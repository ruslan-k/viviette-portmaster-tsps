from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AudioConfigTests(unittest.TestCase):
    def test_port_local_config_defines_playback(self):
        path = ROOT / 'viviette/asound-viviette.conf'
        self.assertTrue(path.is_file(), 'port-local ALSA configuration is missing')
        text = path.read_text()
        for token in ['pcm.Playback', 'pcm.!default "Playback"', 'card audiocodec', 'device 0', 'ctl.!default']:
            self.assertIn(token, text)

    def test_launcher_gates_config_on_matching_card(self):
        text = (ROOT / 'Viviette.sh').read_text()
        self.assertIn('/proc/asound/cards', text)
        self.assertIn('audiocodec', text)
        self.assertIn('export ALSA_CONFIG_PATH="$GAMEDIR/asound-viviette.conf"', text)
        self.assertLess(text.index('export ALSA_CONFIG_PATH='), text.index('./gmloadernext.aarch64 -c gmloader.json'))

if __name__ == '__main__':
    unittest.main()
