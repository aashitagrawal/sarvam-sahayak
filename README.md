# Sarvam Sahayak

Turn a spoken service concern into a clear, editable support ticket. Speak or upload Hindi, Marathi, or Hinglish audio; Saaras transcribes it, Sarvam's chat model writes a concise English ticket and a familiar-language readback, and Bulbul speaks the readback.

## Run locally

Requires Python 3.10+ and a [Sarvam API key](https://dashboard.sarvam.ai/).

```powershell
cd sarvam-sahayak
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Edit `.env` and set `SARVAM_API_KEY` to your key. On macOS/Linux, use `source .venv/bin/activate` and `cp .env.example .env` instead. Then run:

```powershell
streamlit run ui/app.py
```

You may also set `SARVAM_API_KEY` as an environment variable or in local Streamlit secrets. Do not commit `.env` or `.streamlit/secrets.toml`.

## Use

1. Select auto-detect/Hinglish, Hindi, or Marathi. Record up to 30 seconds or upload a short audio clip. You can type instead.
2. Transcribe audio, then correct the transcript if needed.
3. Generate the ticket. Edit each field before downloading the `.txt` file.
4. Play or download the spoken readback.

The ticket is generated in English for support teams. The readback follows the spoken language where possible. No ticket is sent to a service provider automatically.

## Gen Z Translator + Bulbul audio

Open the **💅 Gen Z Translator** tab. Rewrite text in Gen Z slang, optionally translate it into one of 11 Indian languages, and play or download the Bulbul audio.

The same features are available as a REST API (`index.py`):

```powershell
uvicorn index:app --reload --port 8000
```

- `POST /api/translate/genz` `{"text": "..."}` → `{"translation": "..."}`
- `POST /api/audio/bulbul` `{"text": "...", "language_code": "hi-IN", "speaker": "shubh", "pace": 1.0, "translate": false}` → `audio/wav` (spoken text in the `X-Spoken-Text` header, URL-encoded)
- `GET /api/health`

Errors: `400` for invalid input, `502` when Sarvam fails, `503` if `SARVAM_API_KEY` is missing. Interactive docs are at `http://localhost:8000/docs`.

## Project layout

- `ui/app.py`: Streamlit UI (ticket tab + Gen Z tab), deps in `ui/requirements.txt`
- `index.py`: FastAPI REST endpoints (Vercel), deps in `requirements.txt`
- `services/sarvam_service.py`: Sarvam API wrapper (Saaras, chat, Bulbul)
- `services/genz_translator.py`, `services/ticket_generator.py`: LLM prompts and parsing
- `utils/config.py`: loads `SARVAM_API_KEY` via python-dotenv; `utils/styles.py`: Gen Z neon CSS

## API and limits

- `POST /speech-to-text` with `saaras:v4`; auto-detect uses `codemix` mode for Hinglish.
- `POST /v1/chat/completions` with `sarvam-105b` and JSON response mode.
- `POST /text-to-speech` with `bulbul:v3`; readback is limited to 2,500 characters.

Audio upload is limited to 10 MB. Sarvam's synchronous transcription endpoint is intended for audio shorter than 30 seconds. Requests may incur Sarvam usage charges. The app makes calls only when you click an action button. See [ARCHITECTURE.md](ARCHITECTURE.md) for flow and data handling.

## Deploy

Streamlit needs a long-running server with WebSockets, which Vercel's serverless functions do not provide, so the project deploys in two parts:

**REST API → Vercel**
1. Import the GitHub repo in Vercel. Framework Preset: **FastAPI**. Root Directory: **leave empty** (repo root).
2. Add `SARVAM_API_KEY` under *Settings → Environment Variables*.
3. Deploy. Vercel serves `index.py` and installs the root `requirements.txt`; `.vercelignore` leaves out the UI. Open `https://<project>.vercel.app/` (redirects to `/docs`) or `/api/health`.

**Streamlit UI → Streamlit Community Cloud**
1. At [share.streamlit.io](https://share.streamlit.io), create an app from this repo with main file path `ui/app.py` (it installs `ui/requirements.txt`).
2. Under *Advanced settings → Secrets*, add `SARVAM_API_KEY = "..."`.

Both read the key from the environment (`os.environ` via `utils/config.py`), falling back to Streamlit secrets. Never commit `.env`.

## Verify

```powershell
python -m py_compile index.py ui/app.py services/*.py utils/*.py
python -m unittest discover -s tests -v
```

Live API calls require a valid key and network access. The automated checks use mocked responses.

