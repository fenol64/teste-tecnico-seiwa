from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.bootstrap.container import Container
from src.dto.signup import CreateUserDTO
from src.controller.oauth.signup import SignUpHandler
from src.infrastructure.database.connection import get_db

# Remover criação automática de tabelas - usar Alembic migrations
# Base.metadata.create_all(bind=engine)

# Criar instância do FastAPI
app = FastAPI(
    title="API teste tecnico da seiwa",
    description="API inicial criada com FastAPI",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API teste tecnico da seiwa!",
        "docs": "/api/docs",
    }

@app.post('/api/v1/signup')
async def signup(user: CreateUserDTO, db: Session = Depends(get_db)):
    container = Container(db=db)
    handler = SignUpHandler(sign_up_usecase=container.signup_usecase)
    return handler.handle(user)


# Rota de health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

