from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import os
from pathlib import Path
from dotenv import load_dotenv

# --- SISTEMA DE LOCALIZAÇÃO DO .ENV ---
# Isso garante que a API ache o .env na pasta 'backend' mesmo rodando via main.py
base_path = Path(__file__).resolve().parent
env_path = base_path / ".env"
load_dotenv(dotenv_path=env_path)

# Debug para o seu terminal (ajuda o TDAH a confirmar se está ok)
chave_carregada = os.getenv("NEWS_API_KEY")
print(f"🚀 [API uPixel] Carregando .env de: {env_path}")
print(f"🔑 [API uPixel] Status da Chave: {'✅ Encontrada' if chave_carregada else '❌ NÃO ENCONTRADA'}")

# Importamos as funções que já criamos no db_manager
from database.db_manager import salvar_noticias_no_banco, buscar_noticias
from scrapers.news_api_client import buscar_noticias_por_tema

app = FastAPI(
    title="uPixel News Aggregator API",
    description="API para o Agregador de Notícias focado em curadoria.",
    version="1.0.0"
)

# Configuração de CORS (Essencial para o seu futuro App Mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema para resposta (O que a API devolve para o App)
class NoticiaResponse(BaseModel):
    id: int
    titulo: str
    fonte: str
    url: str
    categoria: str
    data: Optional[str] = None 

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "API uPixel operante. Acesse /docs para testar."}

@app.get("/noticias/", response_model=List[NoticiaResponse])
def get_noticias(categoria: str = None, termo: str = None):
    """
    Retorna as notícias do banco. 
    Use o parâmetro 'termo' para filtrar candidatos ou temas específicos.
    """
    noticias = buscar_noticias(categoria=categoria, termo=termo)
    return noticias

@app.post("/noticias/atualizar/")
def fetch_and_save_noticias():
    """
    Aciona o scraper e popula o banco de dados.
    """
    categorias = ["F1", "Futebol", "Economia", "Política"]
    MINHA_CHAVE = os.getenv("NEWS_API_KEY")
    
    if not MINHA_CHAVE:
        raise HTTPException(
            status_code=500, 
            detail=f"NEWS_API_KEY não encontrada no .env. Caminho tentado: {env_path}"
        )
        
    resultado_geral = {}
    
    for tema in categorias:
        try:
            noticias_api = buscar_noticias_por_tema(tema, MINHA_CHAVE)
            if noticias_api:
                # Passamos noticias_api, o tema para log e o tema para categoria
                salvar_noticias_no_banco(noticias_api, tema, tema)
                resultado_geral[tema] = f"{len(noticias_api)} processadas."
            else:
                resultado_geral[tema] = "Sem resultados na API externa."
        except Exception as e:
            resultado_geral[tema] = f"Erro no processamento: {str(e)}"
            
    return {
        "status": "Concluído",
        "detalhes": resultado_geral
    }