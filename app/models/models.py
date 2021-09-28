from sqlalchemy.orm import backref
from app import db


class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    senha = db.Column(db.String(60), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, unique=True)

    def __init__(self, email, senha, user_id):
        self.email = email
        self.senha = senha
        self.user_id = user_id

    def __repr__(self):
        return f"Login('{self.email}')"

# ---------------Mapear one-to-Many---------


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    login = db.relationship('Login', backref='author',
                            lazy=True, uselist=False)
    dependente = db.relationship('Dependente', backref='parente')
    telefone = db.relationship('Telefone', backref='telefone')
    medicamento = db.relationship('Medicamento', backref='medicamento')
    endereco = db.relationship('Endereco', backref='endereco', lazy=True)

    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def __repr__(self):
        return f"User('{self.nome}', '{self.cpf}')"


class Endereco(db.Model):
    __tablename__ = 'endereco'
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(40), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    bairro = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def __init__(self, rua, cidade, cep, bairro):
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.bairro = bairro

    def __repr__(self):
        return f"Endereco('{self.rua}', '{self.cidade}', '{self.cep}', '{self.bairro}')"


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
                            db.ForeignKey('dependente.id'), primary_key=True),
                  db.Column('medicamento_id', db.Integer,
                            db.ForeignKey('medicamento.id'), primary_key=True)
                  )

medDoenca = db.Table('medDoenca',
                     db.Column('medicamento_id', db.Integer,
                               db.ForeignKey('medicamento.id'), primary_key=True),
                     db.Column('doenca_id', db.Integer,
                               db.ForeignKey('doenca.id'), primary_key=True)
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
    medicamentoDescript = db.relationship(
        'Medicamento', secondary=depMed, lazy='dynamic', backref=db.backref('medicamentoDescript', lazy=True))

    def __init__(self, nome, user_id):
        self.nome = nome
        self.user_id = user_id

    def __repr__(self):
        return f"Dependente('{self.nome}')"


class Doenca(db.Model):
    __tablename__ = 'doenca'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    sintoma = db.Column(db.String(400), nullable=False)

    # ----Referencia para mapeamento Many to Many-----------
    doencaMedcamento = db.relationship(
        'Medicamento', secondary=medDoenca, backref=db.backref('doencaMedicamento', lazy='dynamic'))

    def __init__(self, nome, sintoma):
        self.nome = nome
        self.sintoma = sintoma

    def __repr__(self):
        return f"Doenca('{self.nome}', '{self.sintoma}')"
