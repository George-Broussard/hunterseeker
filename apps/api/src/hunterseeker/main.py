"""ASGI entrypoint: ``uv run fastapi dev src/hunterseeker/main.py``."""

from hunterseeker.core.app import create_app

app = create_app()
