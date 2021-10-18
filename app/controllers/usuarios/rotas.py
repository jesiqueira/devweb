from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from app.controllers.forms import (ContatoForm, LoginForm, RegistroForm, DadosUser,
                                   MedicamentoForm, RequestResetForm, ResetPassowordForm)
from app.models.models import Endereco, Medicamento, User, Login
from app import db, bcrypt
from app.controllers.usuarios.utils import send_reset_email
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
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
        return redirect(url_for('users.login'))
    return render_template('cadastro.html', title='Cadastro', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        # print(current_user.id)
        return redirect(url_for('users.home'))
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


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('rota.home'))


@users.route('/account')
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

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        login = Login.query.filter_by(email=form.email.data).first()
        send_reset_email(login)
        flash("Um e-mail foi enviado com instruções para trocar a senha!", 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Trocar Senha', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))

    login = Login.verify_reset_token(token)

    if login is None:
        flash("O Token é inválido ou expirou!", 'warning')
        return redirect(url_for(users.reset_request))

    form = ResetPassowordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        login.password = hashed_password
        db.session.commit()
        flash('Senha atualizada com sucesso! agora você pode logar!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Trocar Senha', form=form)