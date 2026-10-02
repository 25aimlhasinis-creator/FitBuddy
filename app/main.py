from contextlib import asynccontextmanager
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from app.api import router as api_router
    from app.config import APP_HOST, APP_PORT, BASE_DIR
    from app.database import init_db
    from app.routes import router as page_router
else:
    from .api import router as api_router
    from .config import APP_HOST, APP_PORT, BASE_DIR
    from .database import init_db
    from .routes import router as page_router

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield

app = FastAPI(title="FitBuddy – AI Fitness Plan Generator", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(page_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=APP_HOST, port=APP_PORT, reload=True)
