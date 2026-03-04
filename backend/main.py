import uvicorn
import sys
import os
from dotenv import load_dotenv # Importação corrigida

# Garante que o diretório 'backend' está no path do Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Carrega o .env logo no início para garantir que a API e o DB vejam as senhas
    load_dotenv() 
    
    print("🚀 Iniciando o Servidor FastAPI do Agregador de Notícias...")
    print(f"📂 Pasta atual: {os.getcwd()}")
    
    # Executa o app FastAPI usando Uvicorn
    # host 0.0.0.0 permite acesso de outros dispositivos na mesma rede (bom para o App Mobile)
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)