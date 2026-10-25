"""Custom CSS for the Gen Z tab. Scoped to the ``st-key-genz`` container so the ticket tab keeps its normal look."""

from __future__ import annotations

import html

GENZ_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

.st-key-genz {
  font-family: 'Outfit', sans-serif;
  background: radial-gradient(circle at 10% 0%, #3b0a5c 0%, transparent 45%),
              radial-gradient(circle at 100% 100%, #003b4f 0%, transparent 50%),
              #0b0b14;
  border: 1px solid rgba(255, 0, 200, .35);
  border-radius: 24px;
  padding: 28px 24px;
  box-shadow: 0 0 32px rgba(255, 0, 200, .18), inset 0 0 40px rgba(0, 240, 255, .05);
  color: #f2ecff;
}
.st-key-genz * { font-family: 'Outfit', sans-serif; }
.st-key-genz label, .st-key-genz p, .st-key-genz span { color: #e6dcff; }

.genz-title {
  font-size: 2.4rem; font-weight: 800; line-height: 1.1; margin: 0 0 4px;
  background: linear-gradient(90deg, #ff3cac, #b04cff, #2bd2ff);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.genz-sub { color: #b9a9e6; margin-bottom: 18px; }

.st-key-genz textarea {
  background: rgba(20, 16, 40, .85) !important; color: #fff !important;
  border: 1.5px solid #7b2cff !important; border-radius: 16px !important;
  font-size: 1.05rem !important;
}
.st-key-genz textarea:focus { border-color: #2bd2ff !important; box-shadow: 0 0 14px rgba(43, 210, 255, .5) !important; }
.st-key-genz textarea::placeholder { color: #8f7fbf !important; }

.st-key-genz .stButton button, .st-key-genz .stDownloadButton button {
  background: linear-gradient(90deg, #ff3cac 0%, #784ba0 50%, #2b86c5 100%);
  color: #fff; border: none; border-radius: 999px; padding: .6rem 1.6rem;
  font-weight: 800; letter-spacing: .3px;
  box-shadow: 0 0 16px rgba(255, 60, 172, .45);
  transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
}
.st-key-genz .stButton button:hover, .st-key-genz .stDownloadButton button:hover {
  transform: translateY(-2px) scale(1.04); filter: saturate(1.3);
  box-shadow: 0 0 26px rgba(43, 210, 255, .7), 0 0 40px rgba(255, 60, 172, .5); color: #fff;
}
.st-key-genz .stButton button:disabled { opacity: .45; transform: none; box-shadow: none; }

.genz-card {
  margin: 18px 0; padding: 20px 22px; border-radius: 20px;
  background: rgba(255, 255, 255, .06); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1.5px solid transparent;
  background-image: linear-gradient(rgba(18, 14, 34, .9), rgba(18, 14, 34, .9)),
                    linear-gradient(120deg, #ff3cac, #b04cff, #2bd2ff);
  background-origin: border-box; background-clip: padding-box, border-box;
  box-shadow: 0 0 24px rgba(176, 76, 255, .35);
}
.genz-card .tag { font-size: .8rem; font-weight: 800; letter-spacing: 1.5px; color: #2bd2ff; }
.genz-card .text { font-size: 1.25rem; font-weight: 600; color: #fff; margin-top: 6px; white-space: pre-wrap; }

.st-key-genz [data-baseweb="select"] > div {
  background: rgba(20, 16, 40, .85); border: 1.5px solid #7b2cff; border-radius: 14px; color: #fff;
}
.st-key-genz audio { width: 100%; border-radius: 999px; box-shadow: 0 0 18px rgba(43, 210, 255, .45); }
.st-key-genz hr { border-color: rgba(176, 76, 255, .3); }
</style>
"""


def genz_card(text: str, tag: str = "✨ GEN Z TRANSLATION") -> str:
    """Return HTML for the neon output card. ``text`` is escaped, so model output cannot inject markup."""
    return (f'<div class="genz-card"><div class="tag">{html.escape(tag)}</div>'
            f'<div class="text">{html.escape(text)}</div></div>')
