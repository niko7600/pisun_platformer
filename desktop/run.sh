#!/usr/bin/env bash
cd "$(dirname "$0")/.."
python3 -m pip install -q -r desktop/requirements.txt 2>/dev/null || python3 -m pip install -q --break-system-packages -r desktop/requirements.txt
exec python3 main.py "$@"
