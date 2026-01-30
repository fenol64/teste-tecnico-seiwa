from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.routes.oauth import router as oauth_router
from src.dto.responses import HealthCheckResponse

def custom_openapi():
    """Customiza a documentação OpenAPI/Swagger"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Seiwa - Teste Técnico",
        version="1.0.0",
        description="API RESTful desenvolvida com FastAPI, PostgreSQL e Clean Architecture. Inclui autenticação de usuários, gerenciamento de dados e operações CRUD completas.",
        routes=app.routes,
        tags=[
            {
                "name": "Health",
                "description": "Endpoints para verificação de saúde da aplicação"
            },
            {
                "name": "Authentication",
                "description": "Endpoints para autenticação e gerenciamento de usuários"
            }
        ]
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

def create_app() -> FastAPI:
    app = FastAPI(
        title="API Seiwa - Teste Técnico",
        description="API RESTful desenvolvida com FastAPI, PostgreSQL e Clean Architecture",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get(
        "/health",
        tags=["Health"],
        summary="Health Check",
        description="Verifica se a API está funcionando corretamente",
        response_model=HealthCheckResponse,
        responses={
            200: {
                "description": "API está funcionando normalmente",
                "content": {
                    "application/json": {
                        "example": {"status": "ok"}
                    }
                }
            }
        }
    )
    async def health_check():
        """
        Endpoint de health check para verificar se a API está online e funcionando.

        Retorna um status simples indicando que a aplicação está operacional.
        """
        return {"status": "ok"}

    app.include_router(oauth_router, prefix="/api/v1", tags=["Authentication"])

    # Aplicar schema customizado do OpenAPI
    app.openapi = custom_openapi

    return app

app = create_app()
