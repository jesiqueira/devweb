from flask import url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
# from flask_mail import Message
# from app import mail


# def send_reset_email(login):
#     token = login.get_reset_token()
#     msg = Message('Requerido troca de senha',
#                   sender='edmar.ade@gmail.com', recipients=[login.email])
#     msg.body = f"""Para realizar o troca de senha, acesse o link: {url_for('users.reset_token', token=token, _external=True)}
#     Se não foi você quem solicitou essa alteração pode ignorar e nada será modificado """
#     mail.send(msg)

#     print()
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


def send_reset_email(login):
    token = login.get_reset_token()

    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=MAIL_USERNAME, password=MAIL_PASSWORD)
        body=f"""<p>Para realizar o troca de senha, acesse o link: <a href='{url_for("users.reset_token", token=token, _external=True)}'>Clique</a>
        Se não foi você quem solicitou essa alteração pode ignorar e nada será modificado<p>"""
        email_msg = MIMEMultipart()
        email_msg['Subject'] = 'Reset Senha meu Site'
        email_msg.attach(MIMEText(body, 'html'))
        connection.sendmail(
            from_addr=MAIL_USERNAME,
            to_addrs=login.email,
            msg=email_msg.as_string()
        )
