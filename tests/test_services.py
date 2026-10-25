import base64
import json
import unittest
from unittest.mock import patch

from services.genz_translator import translate_genz
from services.sarvam_service import SarvamError, SarvamInputError, generate_bulbul_audio, synthesize, transcribe
from services.ticket_generator import generate_ticket

POST = "services.sarvam_service.requests.post"


class FakeResponse:
    ok = True
    status_code = 200

    def __init__(self, body):
        self.body = body

    def json(self):
        return self.body


def chat(text):
    return FakeResponse({"choices": [{"message": {"content": text}}]})


def wav(data=b"RIFF"):
    return FakeResponse({"audios": [base64.b64encode(data).decode()]})


class SarvamServiceTests(unittest.TestCase):
    @patch(POST)
    def test_hinglish_transcription(self, post):
        post.return_value = FakeResponse({"transcript": "Mera bill galat hai", "language_code": "hi-IN"})
        self.assertEqual(transcribe(b"audio", "clip.wav", "audio/wav", "unknown", "k"), ("Mera bill galat hai", "hi-IN"))
        self.assertEqual(post.call_args.kwargs["data"]["mode"], "codemix")
        self.assertEqual(post.call_args.kwargs["headers"]["api-subscription-key"], "k")

    @patch(POST)
    def test_tts_payload_matches_bulbul_v3(self, post):
        post.return_value = wav(b"RIFFtest")
        self.assertEqual(synthesize("Namaste", "ta-IN", "k", speaker="Ritu", pace=1.2), b"RIFFtest")
        self.assertTrue(post.call_args.args[0].endswith("/text-to-speech"))
        self.assertEqual(post.call_args.kwargs["json"], {
            "model": "bulbul:v3", "text": "Namaste", "language_code": "ta-IN",
            "speaker": "ritu", "pace": 1.2, "output_audio_codec": "wav"})

    def test_tts_rejects_bad_input(self):
        cases = [(("hi", "xx-IN"), {}), (("hi", "hi-IN"), {"speaker": "bad name!"}),
                 (("hi", "hi-IN"), {"pace": 3}), (("x" * 2501, "hi-IN"), {})]
        for args, kwargs in cases:
            with self.subTest(args=args[1], kwargs=kwargs), self.assertRaises(SarvamInputError):
                synthesize(*args, "k", **kwargs)

    def test_missing_key_is_input_error(self):
        with self.assertRaises(SarvamInputError):
            synthesize("hi", "hi-IN", "")

    @patch(POST)
    def test_http_error_is_safe(self, post):
        post.return_value = FakeResponse({})
        post.return_value.ok, post.return_value.status_code = False, 403
        with self.assertRaisesRegex(SarvamError, "API key"):
            synthesize("hi", "hi-IN", "k")

    @patch(POST)
    def test_bulbul_with_translation(self, post):
        post.side_effect = [chat("খাবারটা দারুণ"), wav()]
        audio, spoken = generate_bulbul_audio("Food is bussin", "bn-IN", "k", speaker="priya", translate=True)
        self.assertEqual((audio, spoken), (b"RIFF", "খাবারটা দারুণ"))
        self.assertIn("Bengali", post.call_args_list[0].kwargs["json"]["messages"][0]["content"])


class GenZTests(unittest.TestCase):
    @patch(POST)
    def test_genz_translation(self, post):
        post.return_value = chat("  This food is bussin, no cap.  ")
        self.assertEqual(translate_genz("This food is great.", "k"), "This food is bussin, no cap.")
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], "sarvam-105b")
        self.assertIn("Gen Z translator", payload["messages"][0]["content"])
        self.assertEqual(payload["messages"][1], {"role": "user", "content": "This food is great."})
        self.assertNotIn("response_format", payload)

    def test_genz_rejects_empty_and_long(self):
        for text in ("  ", "x" * 4001):
            with self.assertRaises(SarvamInputError):
                translate_genz(text, "k")


class TicketTests(unittest.TestCase):
    @patch(POST)
    def test_ticket_fields(self, post):
        ticket = dict(subject="Incorrect bill", category="Billing", description="Bill is wrong.",
                      requested_resolution="Review the bill.", readback="Mera bill review karein.")
        post.return_value = chat(json.dumps(ticket))
        self.assertEqual(generate_ticket("Mera bill galat hai", "hi-IN", "k"), ticket)
        self.assertEqual(post.call_args.kwargs["json"]["response_format"], {"type": "json_object"})

    @patch(POST)
    def test_bad_ticket_response_is_safe(self, post):
        post.return_value = chat("{}")
        with self.assertRaises(SarvamError):
            generate_ticket("Help", "en-IN", "k")


class ApiTests(unittest.TestCase):
    def setUp(self):
        try:
            from fastapi.testclient import TestClient
        except ImportError:
            self.skipTest("fastapi not installed")
        import api
        self.client = TestClient(api.app)
        patcher = patch("api.get_api_key", return_value="k")
        patcher.start()
        self.addCleanup(patcher.stop)

    @patch(POST)
    def test_endpoints(self, post):
        post.return_value = chat("bet")
        self.assertEqual(self.client.post("/api/translate/genz", json={"text": "ok"}).json(), {"translation": "bet"})
        post.return_value = wav()
        r = self.client.post("/api/audio/bulbul", json={"text": "hi", "language_code": "hi-IN"})
        self.assertEqual((r.status_code, r.headers["content-type"], r.content), (200, "audio/wav", b"RIFF"))
        bad = self.client.post("/api/audio/bulbul", json={"text": "hi", "language_code": "zz"})
        self.assertEqual(bad.status_code, 400)


if __name__ == "__main__":
    unittest.main()
