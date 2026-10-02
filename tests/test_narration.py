"""Regression checks for meaningful narration drift and timeline failures."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("checker", Path(__file__).resolve().parents[1] / "scripts/check_narration.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class NarrationTests(unittest.TestCase):
    def setUp(self):
        self.script = {"cues": ["A key and a value.", "Append one token."], "speech_lead": .4, "end_pause": .5}
        self.visual = [{"start": 0, "end": 4, "text": self.script["cues"][0]},
                       {"start": 4, "end": 8, "text": self.script["cues"][1]}]
        self.speech = [{"start": .4, "end": 3.4, "text": self.script["cues"][0], "tempo": 1},
                       {"start": 4.4, "end": 7.4, "text": self.script["cues"][1], "tempo": 1}]
        self.transcript = copy.deepcopy(self.speech)
        self.vtt = copy.deepcopy(self.speech)

    def check(self):
        return checker.validate(self.script, self.visual, {"speech": self.speech}, self.transcript, self.vtt)

    def test_accepts_valid_arbitrary_cue_count(self):
        self.assertEqual(self.check()[0], 2)

    def test_rejects_paraphrased_voice(self):
        self.speech[0]["text"] = "Keep the key and value."
        with self.assertRaisesRegex(ValueError, "text differs"):
            self.check()

    def test_rejects_short_visual_hold(self):
        self.visual[0]["end"] = 3.5
        with self.assertRaisesRegex(ValueError, "hold ends"):
            self.check()

    def test_rejects_overlapping_passages(self):
        self.visual[1]["start"] = 3.2
        self.speech[1]["start"] = 3.3
        with self.assertRaisesRegex(ValueError, "overlaps"):
            self.check()

    def test_rejects_nonfinite_timing(self):
        self.speech[0]["end"] = float("nan")
        with self.assertRaisesRegex(ValueError, "invalid time"):
            self.check()

    def test_rejects_stale_subtitle(self):
        self.vtt[1]["text"] = "Finish the request."
        with self.assertRaisesRegex(ValueError, "text differs"):
            self.check()

    def test_rejects_accelerated_speech(self):
        self.speech[0]["tempo"] = 1.1
        with self.assertRaisesRegex(ValueError, "accelerated"):
            self.check()

    def test_reads_vtt_identifiers_settings_and_wrapping(self):
        content = "WEBVTT\n\nNOTE generated\nignored\n\ncue-a\n00:00.400 --> 00:03.400 align:start\nA key and\na value.\n\n00:04.400 --> 00:07.400\nAppend one token.\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "captions.vtt"
            path.write_text(content)
            self.vtt = checker.parse_vtt(path)
        self.assertEqual(self.check()[0], 2)


if __name__ == "__main__":
    unittest.main()
