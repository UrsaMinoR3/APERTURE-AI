from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .core.database import Base, engine
from .models import RequestLog  # registers model with Base metadata
from .routers import idp, logs, stt, tts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aperture AI",
    description=(
        "REST API integrating **Azure OpenAI** and **Deepgram** for voice processing "
        "and intelligent document analysis.\n\n"
        "Speech-to-Text, Text-to-Speech, and Document Analysis are open, no API key "
        "required. The `/logs` endpoint (request history) requires the `X-API-Key` header."
    ),
    version="1.0.0",
)

_STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

app.include_router(stt.router, tags=["Speech-to-Text"])
app.include_router(tts.router, tags=["Text-to-Speech"])
app.include_router(idp.router, tags=["Intelligent Document Processing"])
app.include_router(logs.router, tags=["Database"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(_STATIC_DIR / "index.html")
