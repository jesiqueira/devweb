from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from flask.globals import session
from app import db, bcrypt, mail
from app.controllers.forms import (ContatoForm, LoginForm, RegistroForm, DadosUser,
                                   MedicamentoForm, RequestResetForm, ResetPassowordForm)
from app.models.models import Endereco, Medicamento, Telefone, User, Login
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

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
    page = request.args.get('page', 1, type=int)
    formUser = DadosUser()
    # isouter=True irá reproduzir umas consulta Left Join
    user = db.session.query(User.nome, User.cpf, Login.email, Endereco.rua, Endereco.cidade,  Endereco.cep,  Endereco.bairro).join(
        Login, Login.user_id == User.id).join(Endereco, Endereco.user_id == User.id, isouter=True).filter(User.id == current_user.id).first()

    # medicamentos = Medicamento.query.filter_by(user_id=current_user.id).all()
    medicamentos = Medicamento.query.filter_by(
        user_id=current_user.id).paginate(page=page, per_page=2)

    # print(f'User: {medicamentos}')
    formUser.username.data = user.nome
    formUser.cpf.data = user.cpf
    formUser.email.data = user.email
    formUser.rua.data = user.rua
    formUser.cidade.data = user.cidade
    formUser.cep.data = user.cep
    formUser.bairro.data = user.bairro

    return render_template('account.html', title='Account', user=user, formRegistro=formUser, medicamentos=medicamentos)


@rota.route('/medicamento/new', methods=['GET', 'POST'])
@login_required
def medicamento():
    form = MedicamentoForm()
    if form.validate_on_submit():
        medicamento = Medicamento(nome=form.nome.data, data_validade=form.dataValidade.data,
                                  principio_ativo=form.principioAtivo.data, posologia=form.posologia.data, user_id=current_user.id)
        db.session.add(medicamento)
        db.session.commit()

        flash('Medicamento cadastrado com sucesso..', 'success')
        return redirect(url_for('rota.account'))

    return render_template('medicamento.html', title='Medicamento', legenda='Cadastro de Medicamento', form=form)


@rota.route('/medicamento/<int:medicamento_id>/view',  methods=['GET', 'POST'])
@login_required
def view_medicamento(medicamento_id):
    medicamento = Medicamento.query.get_or_404(medicamento_id)

    if medicamento.user_id != current_user.id:
        about(403)

    form = MedicamentoForm()
    form.nome.data = medicamento.nome
    form.dataValidade.data = medicamento.data_validade
    form.principioAtivo.data = medicamento.principio_ativo
    form.posologia.data = medicamento.posologia
    return render_template('medicamentoView.html', title='Medicamento', legenda='Visualiazar Medicamento', form=form, id_medicamento=medicamento_id)


@rota.route('/medicamento/<int:medicamento_id>/update',  methods=['GET', 'POST'])
@login_required
def update_medicamento(medicamento_id):
    medicamento = Medicamento.query.get_or_404(medicamento_id)

    if medicamento.user_id != current_user.id:
        about(403)

    form = MedicamentoForm()
    if form.validate_on_submit():
        medicamento.nome = form.nome.data
        medicamento.data_validade = form.dataValidade.data
        medicamento.principio_ativo = form.principioAtivo.data
        medicamento.posologia = form.posologia.data
        db.session.commit()
        flash("Medicamento Atualizado com sucesso!", 'success')
        return redirect(url_for('rota.account'))
    elif request.method == 'GET':
        form.nome.data = medicamento.nome
        form.dataValidade.data = medicamento.data_validade
        form.principioAtivo.data = medicamento.principio_ativo
        form.posologia.data = medicamento.posologia
        return render_template('medicamento.html', title='Medicamento', legenda='Update de Medicamento', form=form)


@rota.route('/medicamento/<int:medicamento_id>/delete',  methods=['POST'])
@login_required
def delete_medicamento(medicamento_id):
    medicamento = Medicamento.query.get_or_404(medicamento_id)

    if medicamento.user_id != current_user.id:
        about(403)
    db.session.delete(medicamento)
    db.session.commit()
    flash("Medicamento removido com sucesso!", 'success')
    return redirect(url_for('rota.account'))


def send_reset_email(login):
    token = login.get_reset_token()
    msg = Message('Requerido troca de senha',
                  sender='noreply@demo.com', recipients=[login.email])
    msg.body = f"""Para realizar o troca de senha, acesse o link: {url_for('rota.reset_token', token=token, _external=True)}
    Se não foi você quem solicitou essa alteração pode ignorar e nada será modificado """
    mail.send(msg)

@rota.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('rota.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        login = Login.query.filter_by(email=form.email.data).first()
        send_reset_email(login)
        flash("Um e-mail foi enviado com instruções para trocar a senha!", 'info')
        return redirect(url_for('rota.login'))

    return render_template('reset_request.html', title='Trocar Senha', form=form)


@rota.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('rota.home'))

    login = Login.verify_reset_token(token)

    if login is None:
        flash("O Token é inválido ou expirou!", 'warning')
        return redirect(url_for(rota.reset_request))

    form = ResetPassowordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        login.password = hashed_password
        db.session.commit()
        flash('Senha atualizada com sucesso! agora você pode logar!', 'success')
        return redirect(url_for('rota.login'))

    return render_template('reset_token.html', title='Trocar Senha', form=form)
