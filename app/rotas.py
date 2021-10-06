from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask.globals import session
from app import db, bcrypt
from app.controllers.forms import ContatoForm, LoginForm, RegistroForm, DadosUser
from app.models.models import Endereco, Telefone, User, Login
from flask_login import login_user, current_user, logout_user, login_required


rota = Blueprint('rota', __name__)

dados_cv = [
    {
        'titulo': "​MAPFRE Seguros Gerais S.A",
        'descricao': "Suporte remoto via Microsoft System Center, atendimento no sistema operacional Windows, instalação do pacote Office, Active Directory para alteração e criação de senhas e usuários, instalação e atualização dos sistemas via Ghost, configuração de rede e IP. Atendimento a colaboradores da companhia, utilizando a ferramenta de abertura e controle de chamados Remedy e HP Service Manager.",
        'inicio': '14/10/2014',
        'termino': 'Atual',
    },
    {
        'titulo': 'INTERADAPT​ ​SOLUTIONS​ ​S.A',
        'descricao': "Suporte remoto via (VNC), atendimento nos sistemas operacionais XP ao Windows Seven, instalação do pacote Office 2007 ao 2010, Active Directory para alteração e criação de senhas e usuários, instalação e atualização dos sistemas via Ghost, configuração de rede e IP. Atendimento a colaboradores da companhia, utilizando a ferramenta de abertura e controle de chamados Remedy.",
        'inicio': '23/09/2013',
        'termino': '12/10/2014',
    },
    {
        'titulo': 'VETRO​ ​INDÚSTRIA​ ​COMERCIO​ ​E​ ​SERVIÇOS​ ​LTDA',
        'descricao': '​Suporte técnico ao usuário, manutenção em computadores, redes, servidores, telefonia e monitoramento.',
        'inicio': '18/12/2012',
        'termino': '19/09/2013',
    },
    {
        'titulo': 'TECUMSEH​ ​DO​ ​BRASIL​ ​LTDA',
        'descricao': 'Organizar a linha de produção, alocar pessoas, distribuir as tarefas da equipe, viabilizar material para a produção, garantir o bom andamento do processo e o cumprimento dos prazos, metas e especificações técnicas estabelecidas, realizar testes de qualidade em compressores herméticos.',
        'inicio': '09/12/2002',
        'termino': '04/01/2012',
    }
]


@rota.route('/')
@rota.route('/home')
def home():
    return render_template('home.html', title='Home')


@rota.route('/about')
def about():
    info_cv = dados_cv
    return render_template('about.html', title='Sobre', info_cv=info_cv)


@rota.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()

    if form.validate_on_submit():
        flash(f'Dados enviado com sucesso {form.username.data}!', 'success')
        return redirect(url_for('contato'))
    return render_template('contato.html', title='Contato', form=form)


@rota.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('rota.home'))
    form = RegistroForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(nome=form.username.data, cpf=form.cpf.data)
        db.session.add(user)
        db.session.commit()
        login = Login(email=form.email.data,
                      senha=hashed_password, user_id=user.id)
        db.session.add(login)
        db.session.commit()
        flash('Cadastro Criado com sucesso! agora você pode logar!', 'success')
        return redirect(url_for('rota.login'))
    return render_template('cadastro.html', title='Cadastro', form=form)


@rota.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        # print(current_user.id)
        return redirect(url_for('rota.home'))
    form = LoginForm()
    if form.validate_on_submit():
        login = Login.query.filter_by(email=form.email.data).first()

        if login and bcrypt.check_password_hash(login.senha, form.password.data):
            login_user(login, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('rota.home'))
        else:
            flash(
                "Login não teve sucesso. Por favor verifique o e-mail e a senha.", 'danger')
    return render_template('login.html', title='Login', form=form)


@rota.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('rota.home'))


@rota.route('/account')
@login_required
def account():
    formUser = DadosUser()
    # user = User.query.filter_by(id=current_user.id).first()
    user = db.session.query(User.nome, User.cpf, Login.email).join(
        Login, Login.user_id == User.id).filter(User.id == current_user.id).first()

    endereco = Endereco.query.filter_by(Endereco, Endereco.user_id == current_user.id).first()
    
    
    print(f'User: {user}')
    formUser.username.data = user.nome
    formUser.cpf.data = user.cpf
    formUser.email.data = user.email
    formUser.rua.data = endereco.rua
    return render_template('account.html', title='Account', user=user, formUser=formUser)
