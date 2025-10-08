from flask import *

app = Flask(__name__)

usuarios = [
    ["Maria", "123", "maria@email.com"]
]
eventoseatvs = []

@app.route('/')
def pagina_principal():
    return render_template("agenda.html")

@app.route('/loginadm', methods=['GET', 'POST'])
def login_adm():
    return render_template('LoginADM.html')

@app.route('/menuadm',  methods=['GET', 'POST'])
def menu_adm():
    return render_template("menuadm.html")

@app.route('/verificar', methods=['POST'])
def verificaradm():
        global usuarios
        login = request.form.get("login")
        senha = request.form.get("senha")
        achei = False
        for usuario in usuarios:
            if login == usuario[0] and senha == usuario[1]:
                achei = True
                break

        if achei:
                return render_template('adm.html')
        else:
                return render_template('LoginADM.html', msg='LOGIN OU SENHA INCORRETOS')

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    return render_template('pagcadastro.html')

@app.route('/adicionarusuario', methods=['POST'])
def adicionar_usuario():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    email = request.form.get('email')
    confuser = request.form.get('confuser')

    if senha == confuser:
        usuarios.append([nome,email,senha])
        for user in usuarios:
            print(user)
        return render_template('LoginADM.html')
    else:
        return render_template('pagcadastro.html')


@app.route('/addevento', methods=['post'])
def add_evento():
    global eventoseatvs
    titulo= request.form.get('titulo')
    descricao = request.form.get('descricao')
    data = request.form.get('data')
    print([titulo, descricao, data])
    eventoseatvs.append([titulo, descricao, data])

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


if __name__ == '__main__':
    app.run(debug=True)


