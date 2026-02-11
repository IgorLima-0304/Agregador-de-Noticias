import requests

def buscar_noticias_por_tema(tema, api_key):
    
    url = f"https://newsapi.org/v2/everything?q={tema}&language=pt&sortBy=publishedAt&pageSize=5&apiKey={api_key}"
    
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        
        if dados.get("status") == "ok":
            return dados.get("articles", [])
        else:
            print(f"Erro na API: {dados.get('message')}")
            return []
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return []