from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.routes.oauth import router as oauth_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="API teste tecnico da seiwa",
        description="API inicial criada com FastAPI",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    app.include_router(oauth_router, prefix="/api/v1")

    return app

app = create_app()
