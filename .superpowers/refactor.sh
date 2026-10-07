cd ~/dev/zaincash-support/backend && source ~/.local/bin/env
uv run pytest -q 2>&1 | tail -1
uv run ruff check app tests 2>&1 | tail -1
cd ..
git add -A backend
git commit -q -m 'refactor(pipeline): organize stages into stage1-6 folders matching the flow; add runner.md stage map'
echo "=== final structure ==="
find app/pipeline -name '*.py' -not -path '*__pycache__*' | sort
