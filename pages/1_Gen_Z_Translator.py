"""Gen Z translator with Bulbul audio, shown as a second page of the Streamlit app."""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from sarvam_client import SarvamError
from sarvam_service import BULBUL_LANGUAGES, DEFAULT_SPEAKER, generate_bulbul_audio, get_api_key, translate_genz

load_dotenv()
st.set_page_config(page_title="Gen Z Translator", page_icon="💅", layout="centered")


def api_key() -> str:
    key = get_api_key()
    if not key:
        try:
            key = str(st.secrets.get("SARVAM_API_KEY", "")).strip()
        except (FileNotFoundError, KeyError):
            pass
    return key


st.title("💅 Gen Z Translator")
st.caption("Rewrite any text in Gen Z slang, then hear it in an Indian language with Bulbul.")

key = api_key()
if not key:
    st.warning("Add SARVAM_API_KEY to a local .env file or Streamlit secrets to enable Sarvam APIs.")

source = st.text_area("Your text", height=120, placeholder="e.g. This restaurant's food is really good, you should try it.")
if st.button("Translate to Gen Z", type="primary", disabled=not key or not source.strip()):
    try:
        with st.spinner("Cooking, no cap…"):
            st.session_state.genz = translate_genz(source, key)
        st.session_state.pop("genz_audio", None)
    except SarvamError as exc:
        st.error(str(exc))

if "genz" in st.session_state:
    genz_text = st.text_area("Gen Z version (edit if you like)", value=st.session_state.genz, height=120)

    st.subheader("🔊 Hear it with Bulbul")
    col1, col2 = st.columns(2)
    language = col1.selectbox("Language", list(BULBUL_LANGUAGES), format_func=BULBUL_LANGUAGES.get)
    speaker = col2.text_input("Speaker", value=DEFAULT_SPEAKER, help="Any Bulbul v3 speaker name.")
    translate = st.checkbox("Translate into the selected language before speaking", value=language != "en-IN")

    if st.button("Generate audio", disabled=not key or not genz_text.strip()):
        try:
            with st.spinner("Generating speech with Bulbul…"):
                st.session_state.genz_audio = generate_bulbul_audio(
                    genz_text, language, key, speaker=speaker, translate=translate)
        except SarvamError as exc:
            st.error(str(exc))

    if "genz_audio" in st.session_state:
        audio, spoken = st.session_state.genz_audio
        if spoken != genz_text.strip():
            st.text_area("Spoken text", value=spoken, height=100, disabled=True)
        st.audio(audio, format="audio/wav")
        st.download_button("Download audio (.wav)", data=audio, file_name="genz-bulbul.wav", mime="audio/wav")
