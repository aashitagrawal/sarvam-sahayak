"""Sarvam Sahayak: speech to an editable, professional support ticket."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from sarvam_client import SarvamError, generate_ticket, synthesize, transcribe

load_dotenv()
st.set_page_config(page_title="Sarvam Sahayak", page_icon="🎙️", layout="centered")

LANGUAGES = {
    "Auto-detect / Hinglish": "unknown",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "English": "en-IN",
}


def api_key() -> str:
    key = os.getenv("SARVAM_API_KEY", "").strip()
    if not key:
        try:
            key = str(st.secrets.get("SARVAM_API_KEY", "")).strip()
        except (FileNotFoundError, KeyError):
            pass
    return key


st.title("🎙️ Sarvam Sahayak")
st.caption("Speak naturally. Get a clear support request you can review and share.")

key = api_key()
if not key or key == "replace_with_your_sarvam_api_key":
    st.warning("Add SARVAM_API_KEY to a local .env file or Streamlit secrets to enable Sarvam APIs.")

language_name = st.selectbox("Spoken language", list(LANGUAGES), index=0)
selected_language = LANGUAGES[language_name]
st.info("For best results, use a recording shorter than 30 seconds. Hindi, Marathi, and Hinglish are supported.")

recording = st.audio_input("Record your request")
upload = st.file_uploader("Or upload audio", type=["wav", "mp3", "m4a", "ogg", "webm", "flac"])
audio_file = recording if recording is not None else upload

if audio_file is not None:
    st.audio(audio_file)
    if recording is not None and upload is not None:
        st.caption("Using the recording above. Remove it to use the uploaded file.")
    if st.button("Transcribe audio", disabled=not bool(key), type="primary"):
        try:
            with st.spinner("Transcribing with Saaras…"):
                transcript, detected = transcribe(
                    audio_file.getvalue(), audio_file.name,
                    audio_file.type or "application/octet-stream", selected_language, key
                )
            st.session_state.transcript = transcript
            st.session_state.detected_language = detected
            st.session_state.pop("ticket", None)
            st.session_state.pop("playback", None)
        except SarvamError as exc:
            st.error(str(exc))

transcript = st.text_area(
    "Your words (edit before generating)", key="transcript", height=120,
    placeholder="Or type your request here in Hindi, Marathi, English, or Hinglish…",
)
if st.button("Create support ticket", disabled=not bool(key) or not transcript.strip()):
    try:
        with st.spinner("Preparing your support ticket…"):
            detected = st.session_state.get("detected_language", selected_language)
            st.session_state.ticket = generate_ticket(transcript, detected, key)
        st.session_state.pop("playback", None)
    except SarvamError as exc:
        st.error(str(exc))

if "ticket" in st.session_state:
    st.subheader("Review your ticket")
    ticket = st.session_state.ticket
    subject = st.text_input("Subject", value=ticket["subject"])
    category = st.text_input("Category", value=ticket["category"])
    description = st.text_area("Description", value=ticket["description"], height=160)
    resolution = st.text_area("Requested resolution", value=ticket["requested_resolution"], height=100)
    readback = st.text_area("Readback in your language", value=ticket["readback"], height=100)
    content = (f"Subject: {subject}\nCategory: {category}\n\n"
               f"Description:\n{description}\n\nRequested resolution:\n{resolution}\n")
    st.download_button("Download ticket (.txt)", data=content.encode("utf-8"),
                       file_name="sarvam-sahayak-ticket.txt", mime="text/plain")

    if st.button("Read it aloud", disabled=not bool(key)):
        try:
            detected = st.session_state.get("detected_language", selected_language)
            if detected not in ("hi-IN", "mr-IN", "en-IN"):
                detected = "hi-IN" if selected_language == "unknown" else selected_language
            with st.spinner("Creating speech with Bulbul…"):
                st.session_state.playback = synthesize(readback, detected, key)
        except SarvamError as exc:
            st.error(str(exc))
    if "playback" in st.session_state:
        st.audio(st.session_state.playback, format="audio/wav")
        st.download_button("Download readback (.wav)", data=st.session_state.playback,
                           file_name="sarvam-sahayak-readback.wav", mime="audio/wav")

st.caption("Your recording and ticket stay in this browser session. Audio and text are sent to Sarvam when you use its AI features.")
