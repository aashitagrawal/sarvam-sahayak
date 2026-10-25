"""Vercel entrypoint for the REST API (see vercel.json).

Run locally with:  uvicorn api.index:app --reload --port 8000

If the app fails to import (e.g. a missing module in the serverless bundle), a tiny
fallback ASGI app reports the error instead of an opaque FUNCTION_INVOCATION_FAILED.
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for path in (str(ROOT), str(HERE)):
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from _app import app
except Exception as exc:  # pragma: no cover - only hit in a broken deployment
    traceback.print_exc()
    _ERROR = json.dumps({
        "error": "API failed to start",
        "detail": f"{type(exc).__name__}: {exc}",
        "root_contents": sorted(p.name for p in ROOT.iterdir()),
    }).encode()

    async def app(scope, receive, send):
        if scope["type"] != "http":
            return
        await send({"type": "http.response.start", "status": 500,
                    "headers": [(b"content-type", b"application/json")]})
        await send({"type": "http.response.body", "body": _ERROR})
