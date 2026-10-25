"""One Sarvam chat completion using the key in .env or the environment."""

import os
from pathlib import Path

from sarvamai import SarvamAI


env_file = Path(__file__).with_name(".env")
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("SARVAM_API_KEY="):
            os.environ.setdefault("SARVAM_API_KEY", line.split("=", 1)[1].strip().strip('"\''))
            break

key = os.environ.get("SARVAM_API_KEY", "").strip()
if not key:
    raise SystemExit("Add SARVAM_API_KEY to .env before running this script.")

client = SarvamAI(api_subscription_key=key)
response = client.chat.completions(
    model="sarvam-105b-conversations",
    messages=[{"role": "user", "content": "Say hello in one short sentence."}],
)
print(response.choices[0].message.content)
