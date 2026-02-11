import os
from dotenv import load_dotenv

#tenta carregar o arquivo .env
carregou = load_dotenv()

print("=== 🧪 TESTE DE VARIÁVEIS DE AMBIENTE ===")
if carregou:
    print("✅ Arquivo .env encontrado e carregado!")
else:
    print("❌ Erro: Arquivo .env não encontrado na pasta atual.")

# Verifica cada variável individualmente
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {'****' if os.getenv('DB_PASSWORD') else 'Não encontrada'}")
print(f"NEWS_API_KEY: {'****' if os.getenv('NEWS_API_KEY') else 'Não encontrada'}")
print("=========================================")