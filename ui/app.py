"""Sarvam Sahayak: speech-to-ticket and a Gen Z translator with Bulbul audio.

Run with:  streamlit run ui/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Make the project root (services/, utils/) importable; Streamlit only adds this file's folder to sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.genz_translator import MAX_GENZ_CHARS, translate_genz
from services.sarvam_service import (BULBUL_LANGUAGES, BULBUL_SPEAKERS, DEFAULT_SPEAKER, SarvamError,
                                     generate_bulbul_audio, synthesize, transcribe)
from services.ticket_generator import generate_ticket
from utils.config import get_api_key
from utils.styles import BASE_CSS, GENZ_CSS, TICKET_CSS, genz_card, step_header, ticket_preview

st.set_page_config(page_title="Sarvam Sahayak", page_icon="🎙️", layout="centered")

TICKET_LANGUAGES = {
    "Auto-detect / Hinglish": "unknown",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "English": "en-IN",
}


def render_ticket_tab(key: str) -> None:
    """Speech -> transcript -> editable support ticket -> spoken readback, as three step cards."""
    st.markdown(TICKET_CSS, unsafe_allow_html=True)

    with st.container(key="tstep1"):
        st.markdown(step_header(1, "Tell us what happened", "Record or upload a clip under 30 seconds, or just type below."),
                    unsafe_allow_html=True)
        language_name = st.selectbox("🌐 Spoken language", list(TICKET_LANGUAGES), index=0)
        selected_language = TICKET_LANGUAGES[language_name]
        rec_col, up_col = st.columns(2)
        recording = rec_col.audio_input("🎙️ Record")
        upload = up_col.file_uploader("📁 Or upload", type=["wav", "mp3", "m4a", "ogg", "webm", "flac"])
        audio_file = recording if recording is not None else upload

        if audio_file is not None:
            st.audio(audio_file)
            if recording is not None and upload is not None:
                st.caption("Using the recording. Remove it to use the uploaded file.")
            if st.button("📝 Transcribe audio", disabled=not key, type="primary"):
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
                    st.toast("Transcript ready ✅")
                except SarvamError as exc:
                    st.error(str(exc))

    with st.container(key="tstep2"):
        st.markdown(step_header(2, "Check your words", "Fix anything the transcript got wrong, then create the ticket."),
                    unsafe_allow_html=True)
        transcript = st.text_area(
            "Your words", key="transcript", height=120, label_visibility="collapsed",
            placeholder="Type your request here in Hindi, Marathi, English, or Hinglish…",
        )
        if st.button("✨ Create support ticket", type="primary", disabled=not key or not transcript.strip()):
            try:
                with st.spinner("Preparing your support ticket…"):
                    detected = st.session_state.get("detected_language", selected_language)
                    st.session_state.ticket = generate_ticket(transcript, detected, key)
                st.session_state.pop("playback", None)
                st.toast("Ticket created 🎫")
            except SarvamError as exc:
                st.error(str(exc))

    if "ticket" not in st.session_state:
        return
    with st.container(key="tstep3"):
        st.markdown(step_header(3, "Review & share", "Edit any field, download it, or hear it read back."),
                    unsafe_allow_html=True)
        ticket = st.session_state.ticket
        detected = st.session_state.get("detected_language", selected_language)
        language_label = BULBUL_LANGUAGES.get(detected, "Auto")
        st.markdown(ticket_preview(ticket["subject"], ticket["category"], language_label), unsafe_allow_html=True)

        subj_col, cat_col = st.columns([2, 1])
        subject = subj_col.text_input("Subject", value=ticket["subject"])
        category = cat_col.text_input("Category", value=ticket["category"])
        description = st.text_area("Description", value=ticket["description"], height=150)
        resolution = st.text_area("Requested resolution", value=ticket["requested_resolution"], height=90)
        readback = st.text_area("🗣️ Readback in your language", value=ticket["readback"], height=90)
        content = (f"Subject: {subject}\nCategory: {category}\n\n"
                   f"Description:\n{description}\n\nRequested resolution:\n{resolution}\n")

        dl_col, speak_col = st.columns(2)
        dl_col.download_button("⬇️ Download ticket (.txt)", data=content.encode("utf-8"),
                               file_name="sarvam-sahayak-ticket.txt", mime="text/plain", use_container_width=True)
        if speak_col.button("🔊 Read it aloud", disabled=not key, use_container_width=True):
            try:
                if detected not in BULBUL_LANGUAGES:
                    detected = "hi-IN" if selected_language == "unknown" else selected_language
                with st.spinner("Creating speech with Bulbul…"):
                    st.session_state.playback = synthesize(readback, detected, key)
            except SarvamError as exc:
                st.error(str(exc))
        if "playback" in st.session_state:
            st.audio(st.session_state.playback, format="audio/wav")
            st.download_button("⬇️ Download readback (.wav)", data=st.session_state.playback,
                               file_name="sarvam-sahayak-readback.wav", mime="audio/wav")


def render_genz_tab(key: str) -> None:
    """Text -> Gen Z slang card -> Bulbul audio in a chosen Indian language."""
    st.markdown(GENZ_CSS, unsafe_allow_html=True)
    with st.container(key="genz"):
        st.markdown('<div class="genz-title">Gen Z Translator 💅🔥</div>'
                    '<div class="genz-sub">Drop boring text, get pure aura. Then hear it in your language. No cap. 🧢</div>',
                    unsafe_allow_html=True)
        source = st.text_area("Your text", key="genz_source", height=130, max_chars=MAX_GENZ_CHARS,
                              placeholder="Spill the tea here bestie... ☕", label_visibility="collapsed")
        if st.button("✨ Yeet into Gen Z", disabled=not key or not source.strip()):
            try:
                with st.spinner("Cooking, fr fr… 🍳"):
                    st.session_state.genz_text = translate_genz(source, key)
                st.session_state.pop("genz_audio", None)
                st.success("Ate and left no crumbs 💅")
            except SarvamError as exc:
                st.error(f"😵 Big L: {exc}")

        if "genz_text" not in st.session_state:
            return
        st.markdown(genz_card(st.session_state.genz_text), unsafe_allow_html=True)
        with st.expander("✏️ Tweak the slang before speaking"):
            st.text_area("Edit", key="genz_text", height=110, label_visibility="collapsed")
        text = st.session_state.genz_text

        st.markdown("---")
        st.markdown("#### 🔊 Make Bulbul say it")
        col1, col2, col3 = st.columns([1.2, 1, 1])
        language = col1.selectbox("Language 🌏", list(BULBUL_LANGUAGES), format_func=BULBUL_LANGUAGES.get,
                                  key="genz_language")
        speaker = col2.selectbox("Voice 🎤", BULBUL_SPEAKERS, index=BULBUL_SPEAKERS.index(DEFAULT_SPEAKER),
                                 format_func=str.title, key="genz_speaker")
        pace = col3.slider("Pace ⚡", 0.5, 2.0, 1.0, 0.1, key="genz_pace")
        translate = st.toggle("Translate into the selected language first", value=language != "en-IN",
                              key=f"genz_translate_{language}")

        if st.button("🎧 Drop the audio", disabled=not key or not text.strip()):
            try:
                with st.spinner("Bulbul is warming up the vocals… 🎶"):
                    st.session_state.genz_audio = generate_bulbul_audio(
                        text, language, key, speaker=speaker, pace=pace, translate=translate)
                st.success("Audio is bussin, hit play ▶️")
            except SarvamError as exc:
                st.error(f"😵 Audio flopped: {exc}")

        if "genz_audio" in st.session_state:
            audio, spoken = st.session_state.genz_audio
            if spoken != text.strip():
                st.markdown(genz_card(spoken, tag=f"🌏 SPOKEN IN {BULBUL_LANGUAGES[language].upper()}"),
                            unsafe_allow_html=True)
            st.audio(audio, format="audio/wav")
            st.download_button("⬇️ Download the vibes (.wav)", data=audio, file_name="genz-bulbul.wav",
                               mime="audio/wav")


def main() -> None:
    st.markdown(BASE_CSS, unsafe_allow_html=True)
    st.markdown('<div class="app-hero"><h1>🎙️ Sarvam Sahayak</h1>'
                '<p>Speak naturally. Get a clear support request, or vibe-check your text. ✨</p></div>',
                unsafe_allow_html=True)
    key = get_api_key()
    if not key:
        st.warning("Add SARVAM_API_KEY to a local .env file or Streamlit secrets to enable Sarvam APIs.")
    ticket_tab, genz_tab = st.tabs(["🎫 Support ticket", "💅 Gen Z Translator"])
    with ticket_tab:
        render_ticket_tab(key)
    with genz_tab:
        render_genz_tab(key)
    st.caption("Your recording and text stay in this browser session. Audio and text are sent to Sarvam when you use its AI features.")


main()
