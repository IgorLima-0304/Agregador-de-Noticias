import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def salvar_noticias_no_banco(lista_noticias, categoria):
    conexao = None
    try:
        # Puxa as configurações das variáveis de ambiente
        
        conexao = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5433"),
            database=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            client_encoding='utf8'
        )
        cursor = conexao.cursor()

        for noticia in lista_noticias:
            
            titulo = str(noticia.get('title', '')).encode('utf-8', 'ignore').decode('utf-8')
            fonte = str(noticia.get('source', {}).get('name', '')).encode('utf-8', 'ignore').decode('utf-8')
            url = str(noticia.get('url', ''))

            if titulo and url:
                cursor.execute(
                    """
                    INSERT INTO noticias (titulo, fonte, url, categoria)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING;
                    """,
                    (titulo, fonte, url, categoria)
                )

        
        conexao.commit()
        print(f" Sucesso: Notícias de {categoria} salvas no PostgreSQL!")

    except Exception as e:
       
        msg_erro = str(e).encode('ascii', 'replace').decode('ascii')
        print(f" Erro ao salvar no banco: {msg_erro}")
        
    finally:
        
        if conexao:
            cursor.close()
            conexao.close()