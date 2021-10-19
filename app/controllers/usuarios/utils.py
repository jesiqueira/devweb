from flask import url_for
from flask_mail import Message
from app import mail


def send_reset_email(login):
    token = login.get_reset_token()
    msg = Message('Requerido troca de senha',
                  sender='edmar.ade@gmail.com', recipients=[login.email])
    msg.body = f"""Para realizar o troca de senha, acesse o link: {url_for('users.reset_token', token=token, _external=True)}
    Se não foi você quem solicitou essa alteração pode ignorar e nada será modificado """
    print(msg)
    mail.send(msg)
