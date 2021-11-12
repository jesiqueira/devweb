from typing import ClassVar
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField, DateField
from app.models.models import User, Login


class ContatoForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[
                           DataRequired(), Length(min=5, max=40)])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('Telefone', validators=[DataRequired()])
    texto = TextAreaField('Descreva o motivo do contato',
                          validators=[DataRequired()])
    submit = SubmitField('Enviar')


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembre - me')
    submit = SubmitField('Login')


class RegistroForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[
                           DataRequired(), Length(min=5, max=40)])
    cpf = StringField('CPF', validators=[
                      DataRequired(), Length(min=14, max=14)])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password_conf = PasswordField('Confirme a Senha', validators=[
                                  DataRequired(), EqualTo('password')])

    submit = SubmitField('Registrar me')

    def validate_username(self, username):

        user = User.query.filter_by(nome=username.data).first()
        if user:
            raise ValidationError(
                'Já existe esse usuário em nosso Banco de Dados, cadastre um usuário diferente.')

    def validate_cpf(self, cpf):

        cpf = User.query.filter_by(cpf=cpf.data).first()
        if cpf:
            raise ValidationError(
                'Já existe esse cpf em nosso Banco de Dados, cadastre um cpf diferente.')

    def validate_email(self, email):

        email = Login.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'Já existe esse e-mail em nosso Banco de Dados, cadastre um e-mail diferente.')


class DadosUser(FlaskForm):
    username = StringField('Nome de Usuário')
    cpf = StringField('CPF')
    email = StringField('E-mail')
    rua = StringField('Rua')
    cidade = StringField('Cidade')
    cep = StringField('Cep')
    bairro = StringField('Bairro')


class MedicamentoForm(FlaskForm):
    nome = StringField('Medicamento', validators=[
                       DataRequired(), Length(min=5, max=40)])
    dataValidade = DateField('Data Validade', validators=[DataRequired()])
    principioAtivo = TextAreaField(
        'Principio Ativo', validators=[DataRequired(), Length(min=20, max=400)])
    posologia = TextAreaField('Posologia', validators=[
                              DataRequired(), Length(min=20, max=400)])

    submit = SubmitField('Salvar')


class RequestResetForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar Reset de Senha')

    def validate_email(self, email):
        email = Login.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError(
                'Não encontramos esse e-mail em nossa base, informe e-mail diferente ou Cadastra-se.')


class ResetPassowordForm(FlaskForm):
    password = PasswordField('Senha', validators=[DataRequired()])
    password_conf = PasswordField('Confirme a Senha', validators=[
                                  DataRequired(), EqualTo('password')])
    submit = SubmitField('Troca a Senha')
