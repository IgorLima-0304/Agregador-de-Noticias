from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class NoticiaModel(Base):
    __tablename__ = 'noticias'
    id = Column(Integer, primary_key=True)
    titulo = Column(Text, nullable=False)
    fonte = Column(String(100))
    categoria = Column(String(50))
    url = Column(Text, unique=True)
    data_coleta = Column(DateTime, default=datetime.datetime.utcnow)

# Configuração da Conexão (PC Novo - Porta 5433)
DB_URL = "postgresql://postgres:3233@localhost:5433/postgres"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

# Garante que a tabela existe
Base.metadata.create_all(engine)

def salvar_noticias_no_banco(lista_noticias, tema, categoria):
    """Salva notícias evitando duplicatas e títulos nulos"""
    session = Session()
    try:
        for dado in lista_noticias:
            titulo = dado.get('title')
            url = dado.get('url')
            fonte = dado.get('source', {}).get('name', 'Fonte Desconhecida')

            if not titulo or str(titulo).strip().lower() == 'none':
                continue 

            nova_noticia = NoticiaModel(
                titulo=titulo.strip(),
                fonte=fonte,
                categoria=categoria,
                url=url
            )
            
            exists = session.query(NoticiaModel).filter_by(url=url).first()
            if not exists:
                session.add(nova_noticia)
        
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao salvar: {e}")
    finally:
        session.close()

def buscar_noticias(categoria=None, termo=None):
    """
    Busca notícias no banco. 
    Permite filtrar por categoria ou por termo (ex: nome de candidato).
    """
    session = Session()
    try:
        query = session.query(NoticiaModel)
        
        if categoria:
            query = query.filter(NoticiaModel.categoria == categoria)
        
        if termo:
            # Filtro para curadoria: busca o termo no título
            query = query.filter(NoticiaModel.titulo.ilike(f"%{termo}%"))
            
        # Retorna as mais recentes primeiro
        noticias = query.order_by(desc(NoticiaModel.data_coleta)).all()
        
        # Converte objetos do banco para dicionários (que o FastAPI entende)
        return [
            {
                "id": n.id,
                "titulo": n.titulo,
                "fonte": n.fonte,
                "categoria": n.categoria,
                "url": n.url,
                "data": n.data_coleta.strftime("%d/%m/%Y %H:%M")
            } for n in noticias
        ]
    finally:
        session.close()