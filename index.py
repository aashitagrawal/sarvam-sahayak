"""REST API for the Gen Z translator and Bulbul audio.

Deployed on Vercel (FastAPI preset auto-detects this file). Run locally with:
    uvicorn index:app --reload --port 8000
"""

from __future__ import annotations

from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, Response
from pydantic import BaseModel, Field

from services.genz_translator import MAX_GENZ_CHARS, translate_genz
from services.sarvam_service import DEFAULT_SPEAKER, SarvamError, SarvamInputError, generate_bulbul_audio
from utils.config import get_api_key

app = FastAPI(title="Sarvam Sahayak API")


class GenZRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_GENZ_CHARS)


class GenZResponse(BaseModel):
    translation: str


class BulbulRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)
    language_code: str = Field("hi-IN", examples=["hi-IN", "bn-IN", "ta-IN"])
    speaker: str = DEFAULT_SPEAKER
    pace: float = Field(1.0, ge=0.5, le=2.0)
    translate: bool = Field(False, description="Translate text into language_code before speaking.")


def _key() -> str:
    key = get_api_key()
    if not key:
        raise HTTPException(503, "SARVAM_API_KEY is not configured on the server.")
    return key


def _run(fn, *args, **kwargs):
    """Map service errors to HTTP status codes: bad input -> 400, upstream failure -> 502."""
    try:
        return fn(*args, **kwargs)
    except SarvamInputError as exc:
        raise HTTPException(400, str(exc)) from exc
    except SarvamError as exc:
        raise HTTPException(502, str(exc)) from exc


@app.post("/api/translate/genz", response_model=GenZResponse)
def genz(req: GenZRequest) -> GenZResponse:
    return GenZResponse(translation=_run(translate_genz, req.text, _key()))


@app.post("/api/audio/bulbul", response_class=Response,
          responses={200: {"content": {"audio/wav": {}}}})
def bulbul(req: BulbulRequest) -> Response:
    audio, spoken = _run(generate_bulbul_audio, req.text, req.language_code, _key(),
                         speaker=req.speaker, pace=req.pace, translate=req.translate)
    # Spoken text goes in a header (URL-encoded) so clients can show what was read.
    return Response(audio, media_type="audio/wav",
                    headers={"Content-Disposition": 'inline; filename="bulbul.wav"',
                             "X-Spoken-Text": quote(spoken)})


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse("/docs")


@app.get("/api/health")
def health() -> dict[str, bool]:
    return {"ok": True, "api_key_configured": bool(get_api_key())}
