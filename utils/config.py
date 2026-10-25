"""Configuration loading. Secrets come from .env (via python-dotenv), the environment, or Streamlit secrets."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

PLACEHOLDER_KEY = "replace_with_your_sarvam_api_key"


def get_api_key() -> str:
    """Return SARVAM_API_KEY, or "" if unset or still the .env.example placeholder.

    Checks the environment (including .env) first, then Streamlit secrets when running under Streamlit.
    """
    key = os.getenv("SARVAM_API_KEY", "").strip()
    if not key:
        try:
            import streamlit as st

            key = str(st.secrets.get("SARVAM_API_KEY", "")).strip()
        except Exception:  # no secrets file, or Streamlit not installed (e.g. API server)
            key = ""
    return "" if key == PLACEHOLDER_KEY else key
