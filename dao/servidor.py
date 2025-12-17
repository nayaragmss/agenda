from flask import *
from dao.banco import *
from dao.usuarioDAO import *
from banco import Session

app = Flask(__name__)

usuarios = [["Maria", "123", "maria@email.com"]]
eventoseatvs = [
    ["Conferência de Sustentabilidade", "Auditório do IFPB, Campus Sousa", "Discussões sobre meio ambiente, economia verde e inovação sustentável.", "2025-10-22"],
    ["Feira de Tecnologia 2025", "Centro de Convenções de São Paulo", "Evento com as últimas inovações em tecnologia, palestras e exposições.", "2025-11-15"],
    ["Festival de Música Independente", "Parque Ibirapuera, São Paulo", "Festival com bandas independentes de todo o Brasil.", "2025-12-01"]
]
app.secret_key = 'AGENDA'

init_db()

@app.before_request
def pegar_sessao():
    g.session = Session()

@app.teardown_appcontext
def encerrar_sessao(exception=None):
        Session.remove()

@app.route('/')
def pagina_principal():
    return render_template("agenda.html")


@app.route('/loginadm', methods=['GET', 'POST'])
def login_adm():
    return render_template('admin/LoginADM.html')


@app.route('/verificar', methods=['POST'])
def verificaradm():
    nome = request.form.get("login")  # campo do formulário
    senha = request.form.get("senha")

    db_session = Session()
    usuario_dao = UsuarioDAO(db_session)

    usuario = usuario_dao.autenticar(nome, senha)

    if usuario:
        session['login'] = usuario.nome
        return render_template('admin/adm.html')
    else:
        return render_template('admin/LoginADM.html', msg='LOGIN OU SENHA INCORRETOS')



@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    return render_template('admin/pagcadastro.html')


@app.route('/adicionarusuario', methods=['POST'])
def adicionar_usuario():
    if 'addevento' in session:
        usuarioDAO = UsuarioDAO(g.session)

        adicionar_usuario = usuarioDAO.criar()

        return render_template('agenda.html', usuarios=adicionar_usuario)
    else:
        return render_template('pagcadastro.html')



@app.route('/addevento', methods=['post'])
def add_evento():
    if 'addevento' in session:
        usuarioDAO = EventoDAO(g.session)

        add_evento = usuarioDAO.criar()

        return render_template('adm.html', usuarios=add_evento)
    else:
        return render_template('agenda.html')
@app.route('/detalhes')
def mostrar_detalhes():
    titulo= request.values.get('titulo')
    achei = None
    for eventos in eventoseatvs:
        if titulo == eventos[0]:
            achei = eventos
            break

    return render_template('detalhes.html', eventos=achei)

@app.route('/remover', methods=['post'])
def remover_evento():
    if 'addevento' in session:
        usuarioDAO = EventoDAO(g.session)

        remover_evento= usuarioDAO.remover()

        return render_template('listareventos.html', usuarios=remover_evento)
    else:
        return render_template('agenda.html')

@app.route('/listareventos', methods=['POST','get'])
def listar():
    if 'login' in session:
        usuarioDAO = UsuarioDAO(g.session)

        usuarios_lista = usuarioDAO.listar_usuarios()

        return render_template('listareventos.html',usuarios=usuarios_lista)
    else:
        return render_template('agenda.html')
if __name__ == '__main__':
    app.run(debug=True)


