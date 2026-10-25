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


BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;800&display=swap');

html, body, .stApp, .stApp * { font-family: 'Outfit', sans-serif; }
.stApp {
  background: radial-gradient(circle at 15% -10%, #23164a 0%, transparent 40%),
              radial-gradient(circle at 110% 20%, #0c2c3d 0%, transparent 35%), #0b0b14;
}
[data-testid="stHeader"] { background: transparent; }
/* Keep Streamlit's icon font: the Outfit override would otherwise print icon names as text. */
.stApp [data-testid="stIconMaterial"], .stApp .material-symbols-rounded { font-family: 'Material Symbols Rounded' !important; }
.app-hero { text-align: center; margin: 4px 0 14px; }
.app-hero h1 {
  font-size: 2.6rem; font-weight: 800; margin: 0;
  background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.app-hero p { color: #9d97c2; margin: 4px 0 0; }

.stTabs [role="tablist"] {
  gap: 6px; background: #13131f; padding: 6px; border-radius: 999px;
  border: 1px solid #262640; width: fit-content; margin: 0 auto 18px;
}
.stTabs [role="tab"] { border-radius: 999px; padding: 8px 22px; color: #a7a3c7; background: transparent; }
.stTabs [role="tab"]:hover { color: #fff; }
.stTabs [role="tab"][aria-selected="true"] { background: linear-gradient(90deg, #6d4aff, #3b82f6); color: #fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
</style>
"""

TICKET_CSS = """
<style>
[class*="st-key-tstep"] {
  background: linear-gradient(180deg, rgba(30, 28, 52, .85), rgba(19, 19, 31, .85));
  border: 1px solid #2a2847; border-radius: 20px; padding: 22px 22px 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, .35);
  transition: border-color .2s ease;
}
[class*="st-key-tstep"]:hover { border-color: #4c3fa0; }
.tstep-head { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
.tstep-num {
  width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center;
  font-weight: 800; color: #fff; background: linear-gradient(135deg, #7c5cff, #3b82f6);
  box-shadow: 0 0 14px rgba(124, 92, 255, .55);
}
.tstep-title { font-size: 1.2rem; font-weight: 600; color: #f1efff; }
.tstep-sub { color: #8f8ab3; font-size: .92rem; margin: 0 0 10px 46px; }

[class*="st-key-tstep"] textarea, [class*="st-key-tstep"] input {
  background: #10101b !important; border-radius: 12px !important; color: #f1efff !important;
}
[class*="st-key-tstep"] [data-baseweb="input"], [class*="st-key-tstep"] [data-baseweb="textarea"],
[class*="st-key-tstep"] [data-baseweb="select"] > div {
  background: #10101b; border: 1px solid #2f2c52; border-radius: 12px;
}
[class*="st-key-tstep"] [data-baseweb="input"]:focus-within,
[class*="st-key-tstep"] [data-baseweb="textarea"]:focus-within { border-color: #7c5cff; box-shadow: 0 0 0 3px rgba(124, 92, 255, .2); }
[class*="st-key-tstep"] [data-testid="stFileUploaderDropzone"] { background: #10101b; border: 1.5px dashed #3a3566; border-radius: 14px; }

[class*="st-key-tstep"] .stButton button, [class*="st-key-tstep"] .stDownloadButton button {
  border-radius: 12px; font-weight: 600; padding: .55rem 1.2rem;
  border: 1px solid #3a3566; background: #1b1a2e; color: #e8e5ff;
  transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
}
[class*="st-key-tstep"] .stButton button:hover, [class*="st-key-tstep"] .stDownloadButton button:hover {
  transform: translateY(-1px); border-color: #7c5cff; color: #fff; box-shadow: 0 6px 18px rgba(124, 92, 255, .3);
}
[class*="st-key-tstep"] .stButton button[kind="primary"] {
  background: linear-gradient(90deg, #7c5cff, #3b82f6); border: none; color: #fff;
}
[class*="st-key-tstep"] .stButton button:disabled { opacity: .45; transform: none; box-shadow: none; }

.ticket-preview {
  border-radius: 16px; padding: 16px 18px; margin: 4px 0 14px;
  background: linear-gradient(135deg, rgba(124, 92, 255, .14), rgba(59, 130, 246, .08));
  border: 1px solid rgba(124, 92, 255, .4);
}
.ticket-preview .meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.ticket-preview .id { color: #8f8ab3; font-size: .8rem; letter-spacing: 1px; }
.ticket-preview .chip {
  font-size: .78rem; font-weight: 600; padding: 3px 10px; border-radius: 999px;
  background: rgba(52, 211, 153, .15); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, .35);
}
.ticket-preview .chip.lang { background: rgba(96, 165, 250, .15); color: #93c5fd; border-color: rgba(96, 165, 250, .35); }
.ticket-preview .subject { font-size: 1.25rem; font-weight: 600; color: #fff; margin-top: 8px; }
.st-key-tstep3 audio { width: 100%; border-radius: 999px; }
</style>
"""


def ticket_preview(subject: str, category: str, language: str) -> str:
    """Return HTML for the ticket summary header. All values are escaped."""
    return ('<div class="ticket-preview"><div class="meta"><span class="id">🎫 SUPPORT TICKET</span>'
            f'<span class="chip">{html.escape(category)}</span>'
            f'<span class="chip lang">🌐 {html.escape(language)}</span></div>'
            f'<div class="subject">{html.escape(subject)}</div></div>')


def step_header(num: int, title: str, subtitle: str) -> str:
    """Return HTML for a numbered step header."""
    return (f'<div class="tstep-head"><div class="tstep-num">{num}</div>'
            f'<div class="tstep-title">{html.escape(title)}</div></div>'
            f'<p class="tstep-sub">{html.escape(subtitle)}</p>')


def genz_card(text: str, tag: str = "✨ GEN Z TRANSLATION") -> str:
    """Return HTML for the neon output card. ``text`` is escaped, so model output cannot inject markup."""
    return (f'<div class="genz-card"><div class="tag">{html.escape(tag)}</div>'
            f'<div class="text">{html.escape(text)}</div></div>')
