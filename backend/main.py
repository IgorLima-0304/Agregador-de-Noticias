import sys
import os
from dotenv import load_dotenv

load_dotenv()



sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.news_api_client import buscar_noticias_por_tema
from database.db_manager import salvar_noticias_no_banco

MINHA_CHAVE = os.getenv("NEWS_API_KEY")

def iniciar_central():
    categorias = ["F1", "Futebol", "Economia"]
    
    print("=== CENTRAL DE NOTÍCIAS INICIANDO ===")
    
    for tema in categorias:
        print(f"\nBuscando novidades sobre: {tema}...")
        noticias = buscar_noticias_por_tema(tema, MINHA_CHAVE)
        
        salvar_noticias_no_banco(noticias, tema)

        for i, noticia in enumerate(noticias, 1):
            titulo = noticia.get('title')
            fonte = noticia.get('source', {}).get('name')
            print(f"  {i}. {titulo} ({fonte})")

            

if __name__ == "__main__":
    iniciar_central()