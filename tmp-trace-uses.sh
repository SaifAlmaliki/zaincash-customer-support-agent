#!/bin/bash
set -eu
cd /home/cvzmh_saif/dev/zaincash-support
grep -n "from \"@/lib/stages\"\|from './stages'\|stages\." employee-frontend/src -r --include='*.ts' --include='*.tsx' | head -30
grep -n "stage-trace\|tool-reference" employee-frontend/src -r --include='*.css' | head -20
