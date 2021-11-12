from flask_wtf import FlaskForm
from wtforms import StringField


class AtualizaDadosForm(FlaskForm):
    username = StringField('Nome de Usuário')
    cpf = StringField('CPF')
    email = StringField('E-mail')


class AtualizarEnderecoForm(FlaskForm):
    rua = StringField('Rua')
    cidade = StringField('Cidade')
    cep = StringField('Cep')
    bairro = StringField('Bairro')
