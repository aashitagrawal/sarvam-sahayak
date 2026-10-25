import base64
import unittest
from unittest.mock import patch

from sarvam_service import SarvamInputError, generate_bulbul_audio, translate_genz


class FakeResponse:
    ok = True
    status_code = 200

    def __init__(self, body):
        self.body = body

    def json(self):
        return self.body


def chat(text):
    return FakeResponse({"choices": [{"message": {"content": text}}]})


class ServiceTests(unittest.TestCase):
    @patch("sarvam_client.requests.post")
    def test_genz_translation(self, post):
        post.return_value = chat("  This food is bussin, no cap.  ")
        self.assertEqual(translate_genz("This food is great.", "k"), "This food is bussin, no cap.")
        messages = post.call_args.kwargs["json"]["messages"]
        self.assertIn("Gen Z translator", messages[0]["content"])
        self.assertEqual(messages[1]["content"], "This food is great.")

    def test_genz_rejects_empty(self):
        with self.assertRaises(SarvamInputError):
            translate_genz("  ", "k")

    @patch("sarvam_client.requests.post")
    def test_bulbul_with_translation(self, post):
        wav = FakeResponse({"audios": [base64.b64encode(b"RIFF").decode()]})
        post.side_effect = [chat("খাবারটা দারুণ"), wav]
        audio, spoken = generate_bulbul_audio("Food is bussin", "bn-IN", "k", speaker="anushka", translate=True)
        self.assertEqual((audio, spoken), (b"RIFF", "খাবারটা দারুণ"))
        tts = post.call_args.kwargs["json"]
        self.assertEqual((tts["language_code"], tts["speaker"]), ("bn-IN", "anushka"))

    def test_bulbul_rejects_bad_input(self):
        with self.assertRaises(SarvamInputError):
            generate_bulbul_audio("hi", "xx-IN", "k")
        with self.assertRaises(SarvamInputError):
            generate_bulbul_audio("hi", "hi-IN", "k", speaker="bad name!")


if __name__ == "__main__":
    unittest.main()
