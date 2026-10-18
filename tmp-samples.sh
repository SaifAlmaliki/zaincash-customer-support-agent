#!/bin/bash
set -eu
export PATH="$HOME/.local/bin:$PATH"
cd /home/cvzmh_saif/dev/zaincash-support
graphify query "sample synthetic customer tickets json csv for demo batch upload" --budget 1200
echo "---- files ----"
find data -type f \( -name '*.json' -o -name '*.jsonl' -o -name '*.csv' \) | head -40
