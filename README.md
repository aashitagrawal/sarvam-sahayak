# Sarvam Sahayak

Turn a spoken service concern into a clear, editable support ticket. Speak or upload Hindi, Marathi, or Hinglish audio; Saaras transcribes it, Sarvam's chat model writes a concise English ticket and a familiar-language readback, and Bulbul speaks the readback.

## Run locally

Requires Python 3.10+ and a [Sarvam API key](https://dashboard.sarvam.ai/).

```powershell
cd sarvam-sahayak
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `SARVAM_API_KEY` to your key. On macOS/Linux, use `source .venv/bin/activate` and `cp .env.example .env` instead. Then run:

```powershell
streamlit run app.py
```

You may also set `SARVAM_API_KEY` as an environment variable or in local Streamlit secrets. Do not commit `.env` or `.streamlit/secrets.toml`.

## Use

1. Select auto-detect/Hinglish, Hindi, or Marathi. Record up to 30 seconds or upload a short audio clip. You can type instead.
2. Transcribe audio, then correct the transcript if needed.
3. Generate the ticket. Edit each field before downloading the `.txt` file.
4. Play or download the spoken readback.

The ticket is generated in English for support teams. The readback follows the spoken language where possible. No ticket is sent to a service provider automatically.

## API and limits

- `POST /speech-to-text` with `saaras:v4`; auto-detect uses `codemix` mode for Hinglish.
- `POST /v1/chat/completions` with `sarvam-105b` and JSON response mode.
- `POST /text-to-speech` with `bulbul:v3`; readback is limited to 2,500 characters.

Audio upload is limited to 10 MB. Sarvam's synchronous transcription endpoint is intended for audio shorter than 30 seconds. Requests may incur Sarvam usage charges. The app makes calls only when you click an action button. See [ARCHITECTURE.md](ARCHITECTURE.md) for flow and data handling.

## Verify

```powershell
python -m py_compile app.py sarvam_client.py
python -m unittest discover -s tests -v
```

Live API calls require a valid key and network access. The automated checks use mocked responses.

