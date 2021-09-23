from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField


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
