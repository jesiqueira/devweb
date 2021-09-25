from enum import unique
from app import db


class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    senha = db.Column(db.String(60), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)

    def __repr__(self):
        return f"Login('{self.email}')"

# ---------------Mapear one-to-Many---------


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    sobrenome = db.Column(db.String(40), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    login = db.relationship('Login', backref='author', lazy=True, uselist=False)
    dependente = db.relationship('Dependente', backref='parente')
    telefone = db.relationship('Telefone', backref='telefone')
    medicamento = db.relationship('Medicamento', backref='medicamento')

    def __init__(self, nome, sobrenome, cpf, login):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.login = login

    def __repr__(self):
        return f"User('{self.nome}', '{self.sobrenome}','{self.cpf}')"

class Endereco(db.Model):
    __tablename__= 'endereco'
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(40), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    cep = db.Column(db.String(20), nullable=False)


class Telefone(db.Model):
    __tablename__ = 'telefone'
    id = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, ddd, numero):
        self.ddd = ddd
        self.numero = numero

    def __repr__(self):
        return f"Telefone('{self.ddd}', '{self.numero}')"


# ---------------Mapear Many-to-Many---------
depMed = db.Table('depMed',
                  db.Column('depentende_id', db.Integer,
                            db.ForeignKey('dependente.id')),
                  db.Column('medicamento_id', db.Integer,
                            db.ForeignKey('medicamento.id'))
                  )


class Medicamento(db.Model):
    __tablename__ = 'medicamento'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    data_validade = db.Column(db.DateTime, nullable=False)
    principio_ativo = db.Column(db.String(300), nullable=False)
    posologia = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, nome, data_validade, principio_ativo, posologia):
        self.nome = nome
        self.data_validade = data_validade
        self.principio_ativo = principio_ativo
        self.posologia = posologia

    def __repr__(self):
        return f"Medicamento('{self.nome}', '{self.data_validade}','{self.principio_ativo}', '{self.posologia}'"


class Dependente(db.Model):
    __tablename__ = 'dependente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # ----Referencia para mapeamento Many to Many-----------
    medicamentoDescription = db.relationship(
        'medicamento', secondary=depMed, backref=db.backref('medicamentoDescript', lazy='dynamic'))

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"Dependente('{self.nome}')"
