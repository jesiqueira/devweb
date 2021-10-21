# -*- coding: utf-8 -*-
from flask import url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib


def send_reset_email(login):
    token = login.get_reset_token()

    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=os.environ.get('MAIL_USERNAME'),
                         password=os.environ.get('MAIL_PASSWORD'))
        body = f"""<b>Para realizar o troca de senha,
        <a href="{url_for('users.reset_token', token=token, _external=True)}">Clique Aqui</a>
        Se não foi você quem solicitou essa alteração pode ignorar e nada será modificado!<b>"""
        email_msg = MIMEMultipart()
        email_msg['Subject'] = 'Reset Senha meu Site'
        email_msg.attach(MIMEText(body, 'html'))
        connection.sendmail(
            from_addr=os.environ.get('MAIL_USERNAME'),
            to_addrs=login.email,
            msg=email_msg.as_string().encode('utf-8')
        )
