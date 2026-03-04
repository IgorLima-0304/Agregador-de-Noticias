from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.db import Base

class Noticia(Base):
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    fonte = Column(String)
    url = Column(String, unique=True, index=True)
    categoria = Column(String, index=True)
    data_coleta = Column(DateTime, default=datetime.utcnow)
