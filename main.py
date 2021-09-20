from flask import Flask, render_template, flash, redirect, url_for
from controllers.forms import ContatoForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '709bb33e1d3b513e4a9ee78a2a940063'

dados_cv = [
    {
        'titulo': "​MAPFRE Seguros Gerais S.A",
        'descricao':"Suporte remoto via Microsoft System Center, atendimento no sistema operacional Windows, instalação do pacote Office, Active Directory para alteração e criação de senhas e usuários, instalação e atualização dos sistemas via Ghost, configuração de rede e IP. Atendimento a colaboradores da companhia, utilizando a ferramenta de abertura e controle de chamados Remedy e HP Service Manager.",
        'inicio': '14/10/2014',
        'termino': 'Atual',
    },
    {
        'titulo' : 'INTERADAPT​ ​SOLUTIONS​ ​S.A',
        'descricao':"Suporte remoto via (VNC), atendimento nos sistemas operacionais XP ao Windows Seven, instalação do pacote Office 2007 ao 2010, Active Directory para alteração e criação de senhas e usuários, instalação e atualização dos sistemas via Ghost, configuração de rede e IP. Atendimento a colaboradores da companhia, utilizando a ferramenta de abertura e controle de chamados Remedy.",
        'inicio': '23/09/2013',
        'termino': '12/10/2014',
    },
    {
        'titulo' :'VETRO​ ​INDÚSTRIA​ ​COMERCIO​ ​E​ ​SERVIÇOS​ ​LTDA',
        'descricao' :'​Suporte técnico ao usuário, manutenção em computadores, redes, servidores, telefonia e monitoramento.',
        'inicio' : '18/12/2012',
        'termino' : '19/09/2013',
    },
    {
        'titulo' : 'TECUMSEH​ ​DO​ ​BRASIL​ ​LTDA',
        'descricao' :'Organizar a linha de produção, alocar pessoas, distribuir as tarefas da equipe, viabilizar material para a produção, garantir o bom andamento do processo e o cumprimento dos prazos, metas e especificações técnicas estabelecidas, realizar testes de qualidade em compressores herméticos.',
        'inicio' : '09/12/2002',
        'termino' : '04/01/2012',
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/about')
def about():
    info_cv = dados_cv
    return render_template('about.html', title='Sobre', info_cv = info_cv)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    
    if form.validate_on_submit():
        flash(f'Dados enviado com sucesso {form.username.data}!', 'success')
        return redirect(url_for('contato'))
    return render_template('contato.html', title='Contato', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
