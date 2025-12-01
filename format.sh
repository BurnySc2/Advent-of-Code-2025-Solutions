#!/bin/bash
set -e

# Convert single to double quotes
uv run ruff check src --select Q --fix
# Remove unused imports
uv run ruff check src --select F --fix
# Sort imports
uv run ruff check src --select I --fix
# Format code
uv run ruff format src
