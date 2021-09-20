from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from wtforms.fields.html5 import EmailField


class ContatoForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[
                           DataRequired(), Length(min=5, max=30)])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('Telefone', validators=[DataRequired()])
    texto = TextAreaField('Descreva o motivo do contato', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembre - me')
    submit = SubmitField('Login')
