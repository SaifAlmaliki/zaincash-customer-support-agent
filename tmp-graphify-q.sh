#!/bin/bash
set -eu
export PATH="$HOME/.local/bin:$PATH"
cd /home/cvzmh_saif/dev/zaincash-support
graphify explain "match_transaction" --budget 1500
