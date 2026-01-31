# api/index.py
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

# Para Vercel, exportar a aplicação ASGI diretamente
# Vercel usa uvicorn internamente que espera uma app ASGI
app = app