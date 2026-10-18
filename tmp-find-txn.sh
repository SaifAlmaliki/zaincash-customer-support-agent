#!/bin/bash
set -eu
cd /home/cvzmh_saif/dev/zaincash-support
grep -n -R "ZC2410000123" data backend --include='*.json' --include='*.jsonl' --include='*.csv' --include='*.py' --include='*.sql' --include='*.yaml' | head -30
