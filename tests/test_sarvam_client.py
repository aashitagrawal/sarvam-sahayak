import base64
import json
import unittest
from unittest.mock import patch

from sarvam_client import SarvamError, generate_ticket, synthesize, transcribe


class FakeResponse:
    ok = True
    status_code = 200

    def __init__(self, body):
        self.body = body

    def json(self):
        return self.body


class ClientTests(unittest.TestCase):
    @patch("sarvam_client.requests.post")
    def test_hinglish_transcription(self, post):
        post.return_value = FakeResponse({"transcript": "Mera bill galat hai", "language_code": "hi-IN"})
        text, language = transcribe(b"audio", "clip.wav", "audio/wav", "unknown", "test-key")
        self.assertEqual((text, language), ("Mera bill galat hai", "hi-IN"))
        self.assertEqual(post.call_args.kwargs["data"]["mode"], "codemix")
        self.assertEqual(post.call_args.kwargs["headers"]["api-subscription-key"], "test-key")

    @patch("sarvam_client.requests.post")
    def test_ticket_fields(self, post):
        ticket = dict(subject="Incorrect bill", category="Billing", description="Bill is wrong.",
                      requested_resolution="Review the bill.", readback="Mera bill review karein.")
        post.return_value = FakeResponse({"choices": [{"message": {"content": json.dumps(ticket)}}]})
        self.assertEqual(generate_ticket("Mera bill galat hai", "hi-IN", "test-key"), ticket)

    @patch("sarvam_client.requests.post")
    def test_tts_decodes_audio(self, post):
        post.return_value = FakeResponse({"audios": [base64.b64encode(b"RIFFtest").decode()]})
        self.assertEqual(synthesize("Namaste", "hi-IN", "test-key"), b"RIFFtest")

    @patch("sarvam_client.requests.post")
    def test_bad_ticket_response_is_safe(self, post):
        post.return_value = FakeResponse({"choices": [{"message": {"content": "{}"}}]})
        with self.assertRaises(SarvamError):
            generate_ticket("Help", "en-IN", "test-key")


if __name__ == "__main__":
    unittest.main()
