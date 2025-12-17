from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)

    def __init__(self, nome, email, senha):
        return f"<Evento(id='{self.id}', nome='{self.nome}', email='{self.email}', senha='{self.senha}')>"

class Evento(Base):
    __tablename__ = 'eventos'

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    local = Column(String)
    descricao = Column(String)
    data = Column(String)

    def __repr__(self):
        return f"<Evento(id='{self.id}', titulo='{self.titulo}', local='{self.local}', descricao='{self.descricao}', data='{self.data}')>"