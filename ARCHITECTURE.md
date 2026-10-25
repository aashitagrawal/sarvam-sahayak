# Architecture

```text
Browser (Streamlit)
  ├─ microphone / uploaded clip / typed text
  ├─ editable transcript and ticket
  ├─ audio playback
  └─ .txt and .wav downloads
          │ explicit button clicks
          ▼
Python app + services/
  ├─ Saaras v4: audio → transcript
  ├─ Sarvam-105B: transcript → structured ticket + local-language readback
  └─ Bulbul v3: readback → WAV audio
```

## Processing

1. Streamlit receives audio in memory. The user can choose auto-detection, Hindi, Marathi, or English.
2. `services.sarvam_service.transcribe` sends multipart audio to Saaras. The transcript is displayed for correction.
3. `generate_ticket` sends the corrected transcript to Sarvam Chat Completions with instructions to preserve facts and return five fields: subject, category, description, requested resolution, and readback. It validates that all fields exist and are nonempty.
4. The user edits the ticket. The app builds the downloadable text from the current edits.
5. `synthesize` sends the editable readback to Bulbul, decodes the returned base64 WAV, and exposes browser playback and a download.

## Security and failure behavior

- The key is read server-side from `SARVAM_API_KEY` or Streamlit secrets and sent only in the Sarvam request header. `.env` and Streamlit secrets are ignored by Git.
- Uploaded audio, transcripts, tickets, and generated speech stay in Streamlit session memory. The app does not create a database or submit tickets externally.
- Audio/transcript/readback necessarily leave the app for Sarvam processing after the related action. Avoid recording secrets or sensitive account details unless this is appropriate for your use case.
- Requests have timeouts. The app reports missing/invalid keys, network failures, rate limits, invalid input, and malformed responses without exposing the API key.
- This is an MVP. It does not identify a service provider, manage accounts, queue long recordings, or provide a persistent ticket history.

## Official API references

- [Saaras REST transcription](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)
- [Sarvam Chat Completions V1](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1)
- [Bulbul REST text to speech](https://docs.sarvam.ai/api-reference/text-to-speech/convert)
- [Authentication](https://docs.sarvam.ai/api-reference/authentication)
