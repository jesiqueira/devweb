from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    sobrenome = db.Column(db.String(40), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    login = db.relationship('Login', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.nome}', '{self.sobrenome}','{self.cpf}')"


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    senha = db.Column(db.String(60), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Login('{self.email}')"
