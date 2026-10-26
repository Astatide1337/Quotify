from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

import Backend


class TTSDeviceTests(unittest.TestCase):
    def test_cpu_tts_passes_text_without_shell_interpolation(self):
        torch = types.ModuleType("torch")
        torch.cuda = types.SimpleNamespace(is_available=lambda: False)
        tts = types.ModuleType("TTS")
        tts.__path__ = []
        api = types.ModuleType("TTS.api")
        api.TTS = Mock()
        text = 'A quote with "double quotes" and $(literal text).'
        with tempfile.TemporaryDirectory() as directory:
            output = str(Path(directory) / "speech.wav")
            with patch.dict(sys.modules, {"torch": torch, "TTS": tts, "TTS.api": api}), patch.object(Backend.os, "system") as shell:
                Backend.TTS(text, "fixture-speaker", output)
            shell.assert_not_called()
            api.TTS.assert_called_once_with("tts_models/multilingual/multi-dataset/xtts_v2")
            api.TTS.return_value.to.assert_called_once_with("cpu")
            api.TTS.return_value.to.return_value.tts_to_file.assert_called_once_with(
                text=text, speaker_wav="Speakers/fixture-speaker.wav", language="en", file_path=output,
            )


if __name__ == "__main__":
    unittest.main()
