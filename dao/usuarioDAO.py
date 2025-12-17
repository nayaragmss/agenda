from sqlalchemy.orm import*
from modelos.modelos import*
class UsuarioDAO:
    def __init__(self, session: scoped_session):
        self.session = session

    def criar(self, usuario):
        self.session.add(usuario)
        self.session.commit()

    def buscar_por_email(self, email):
        return self.session.query(Usuario).filter_by(email=email).first()

    def listar_usuarios(self):
        return self.session.query(Usuario).all()

    def autenticar(self, nome, senha):
            user = self.buscar_por_nome(nome)
            if user and user.senha == senha:
                return user
            return None


class EventoDAO:
    def __init__(self, session: scoped_session):
        self.session = session

    def criar(self, evento):
        self.session.add(evento)
        self.session.commit()

    def listar_eventos(self):
        return self.session.query(Evento).all()

    def buscar_por_titulo(self, titulo):
        return self.session.query(Evento).filter_by(titulo=titulo).first()

    def remover(self, evento):
        self.session.delete(evento)
        self.session.commit()
