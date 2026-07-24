import os
import secrets
import sys
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"
KEY_LINE = "ENCRYPTION_KEY="

def main() -> int:
    if not ENV_PATH.exists():
        ENV_PATH.touch()
        print(f"created empty {ENV_PATH}")

    existing = ENV_PATH.read_text().splitlines() if ENV_PATH.stat().st_size else []

    for line in existing:
        if line.startswith(KEY_LINE) and len(line) > len(KEY_LINE):
            print(f"ENCRYPTION_KEY already set in {ENV_PATH}, leaving it alone")
            return 0

    new_key = secrets.token_hex(16)
    with ENV_PATH.open("a") as f:
        if existing and not existing[-1].endswith("\n"):
            f.write("\n")
        f.write(f"{KEY_LINE}{new_key}\n")

    print(f"wrote ENCRYPTION_KEY to {ENV_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())