from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend" / "static"

app = FastAPI(
    title="SIPC Genesis",
    description="Piattaforma metodologica per la gestione dei procedimenti contributivi.",
    version="0.1.0-alpha",
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def home() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "application": "SIPC Genesis",
        "version": "0.1.0-alpha",
    }


@app.get("/api/system")
def system_info() -> dict[str, object]:
    return {
        "principle": "Territory First",
        "pilot_municipality": "Collina d'Oro",
        "modules": [
            "Core Engine",
            "GIS Engine",
            "Practice Engine",
            "Methodology Engine",
            "Knowledge Engine",
            "Cognitive Engine",
        ],
    }
