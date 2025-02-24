from flask import Flask, render_template, request, redirect, session, flash, url_for

# Classe que representa um jogo com nome, categoria e console
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome            # Nome do jogo
        self.categoria = categoria  # Categoria do jogo
        self.console = console      # Console em que o jogo pode ser jogado

# Criação de instâncias da classe Jogo para popular a lista inicial
jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')

# Lista que armazena os jogos cadastrados
lista = [jogo1, jogo2, jogo3]

# Classe que representa um usuário do sistema
class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome            # Nome completo do usuário
        self.nickname = nickname    # Apelido utilizado para login
        self.senha = senha          # Senha para autenticação

# Criação de instâncias da classe Usuario para autenticação
usuario1 = Usuario("Harry Potter", "HP", "alohomora")
usuario2 = Usuario("Seu João", "Padeiro", "paozinho")
usuario3 = Usuario("Guilherme Cavalcanti", "Dev", "python_eh_vida")

# Dicionário de usuários para facilitar a busca pelo nickname
usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3
}

# Inicialização da aplicação Flask
app = Flask(__name__)
app.secret_key = 'alura'  # Chave secreta para o gerenciamento de sessões

# Rota principal que exibe a lista de jogos cadastrados
@app.route('/')
def index():
    # Renderiza o template 'lista.html', passando o título e a lista de jogos
    return render_template('lista.html', titulo='Jogos', jogos=lista)

# Rota para exibir o formulário de cadastro de um novo jogo
@app.route('/novo')
def novo():
    # Verifica se o usuário está logado; se não, redireciona para a página de login
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    # Se estiver logado, renderiza o template 'novo.html'
    return render_template('novo.html', titulo='Novo Jogo')

# Rota para processar o formulário de criação de um novo jogo (somente POST)
@app.route('/criar', methods=['POST',])
def criar():
    # Recupera os dados enviados pelo formulário
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    # Cria uma nova instância de Jogo com os dados fornecidos
    jogo = Jogo(nome, categoria, console)
    # Adiciona o novo jogo à lista de jogos
    lista.append(jogo)
    # Redireciona para a página inicial para exibir a lista atualizada
    return redirect(url_for('index'))

# Rota que exibe o formulário de login
@app.route('/login')
def login():
    # Captura o parâmetro 'proxima' que indica para onde o usuário deve ser redirecionado após o login
    proxima = request.args.get('proxima')
    # Renderiza o template 'login.html' passando a URL da próxima página
    return render_template('login.html', proxima=proxima)

# Rota que processa a autenticação do usuário (somente POST)
@app.route('/autenticar', methods=['POST',])
def autenticar():
    # Verifica se o usuário informado existe no dicionário de usuários
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        # Compara a senha enviada com a senha armazenada
        if request.form['senha'] == usuario.senha:
            # Armazena o nickname do usuário na sessão, indicando que o usuário está logado
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            # Redireciona para a próxima página solicitada
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    # Se a autenticação falhar, exibe uma mensagem de erro e redireciona para o login
    flash('Usuário não logado.')
    return redirect(url_for('login'))

# Rota para efetuar o logout do usuário
@app.route('/logout')
def logout():
    # Remove o usuário da sessão, definindo como None
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    # Redireciona para a página principal
    return redirect(url_for('index'))

# Inicia a aplicação Flask no modo de debug
app.run(debug=True)