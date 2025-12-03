from flask import *
from dao.banco import *
from dao.usuarioDAO import *

app = Flask(__name__)

usuarios = [
    ["Maria", "123", "maria@email.com"]
]
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
    usuario_dao = usuarioDAO(g.session)
@app.route('/')
def pagina_principal():
    return render_template("agenda.html")


@app.route('/loginadm', methods=['GET', 'POST'])
def login_adm():
    return render_template('admin/LoginADM.html')


@app.route('/verificar', methods=['POST'])
def verificaradm():
        global usuarios
        login = request.form.get("login")
        senha = request.form.get("senha")
        achei = False
        for usuario in usuarios:
            if login == 'Maria' and senha == '123':
                session['login'] = login
                return render_template('admin/adm.html')
        else:
                return render_template('admin/LoginADM.html', msg='LOGIN OU SENHA INCORRETOS')



@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    return render_template('admin/pagcadastro.html')


@app.route('/adicionarusuario', methods=['POST'])
def adicionar_usuario():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    email = request.form.get('email')
    confuser = request.form.get('confuser')
    usuario_dao = UsuarioDAO(g.session)
    if senha == confuser:
        usuarios.append([nome,email,senha])
        for user in usuarios:
            print(user)
        return render_template('admin/LoginADM.html')
    else:
        return render_template('admin/pagcadastro.html')



@app.route('/addevento', methods=['post'])
def add_evento():
    global eventoseatvs
    titulo= request.form.get('titulo')
    local = request.form.get('local')
    descricao = request.form.get('descricao')
    data = request.form.get('data')
    print([titulo, local, descricao, data])
    eventoseatvs.append([titulo, local, descricao, data])

    print(eventoseatvs)
    if len(eventoseatvs) > 0:
        return render_template('agenda.html', eventoeatvs=eventoseatvs)
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
        global eventoseatvs
        titulo = request.form.get("titulo")

        eventoseatvs = [e for e in eventoseatvs if e[0] != titulo]

        return render_template('listareventos.html', eventoseatvs=eventoseatvs)

@app.route('/listareventos', methods=['POST','get'])
def listar():
    if 'login' in session:
        print(len(eventoseatvs))
        if len(eventoseatvs) > 0:
            return render_template('listareventos.html', eventoseatvs=eventoseatvs)

        else:
            return render_template('listareventos.html', eventoeatvs=eventoseatvs )
    else:
        return render_template('admin/LoginADM.html')


if __name__ == '__main__':
    app.run(debug=True)


