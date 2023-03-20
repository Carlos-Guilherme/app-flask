from flask import Flask, render_template, request, url_for, g
import sqlite3

app = Flask(__name__)

DATABASE = 'app_login.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS dados_clientes (login text, senha text)')
        db.row_factory = sqlite3.Row
    return db

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/cadastro/')
def cadastrar():
    return render_template('cadastro.html')

@app.route('/validar_cadastro/', methods=['POST', 'GET'])
def validar_cadastro():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()

        login = request.form['login_cadastro']
        senha = request.form['senha_cadastro']
        
        cursor.execute("SELECT * FROM dados_clientes WHERE login=?", (login,))
        resultado = cursor.fetchone()
        

        # verifique se a consulta retornou algum resultado
        if resultado:
            return "Login já existente"
        else:
            # Inserindo dados
            cursor.execute(f'INSERT INTO dados_clientes VALUES("{login}", "{senha}")')
            # Salvando as alterações
            db.commit()
            
            return 'Dados cadastrados'
    return 'erro'

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/validar_login/', methods=['POST', 'GET'])
def validar_login():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()

        login = request.form['login']
        senha = request.form['senha']
        
        # execute uma consulta SQL para verificar se o login e senha existem na tabela
        cursor.execute("SELECT * FROM dados_clientes WHERE login=? AND senha=?", (login, senha))
        resultado = cursor.fetchone()

        # verifique se a consulta retornou algum resultado
        if resultado:
            return "Login efetuado"
        else:
            return "cadastro não existe"
    else:
        return 'erro'
    

if __name__ == '__main__':
    app.run(debug=True)