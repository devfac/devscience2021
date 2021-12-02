import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy.sql.expression import true

import emails
from emails.template import JinjaTemplate
from jose import jwt
import secrets, random, string
import smtplib, ssl
from pydantic import EmailStr
import requests
import json
from uuid import UUID
from app.core.config import settings
from unidecode import unidecode


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None

def create_secret():
    res = "".join(secrets.choice(string.ascii_letters+string.digits) for x in range(10))
    return res

def create_anne(anne:str):
    ann = "anne_"+anne[0:4]+"_"+anne[5:9]
    return ann

def decode_schemas(schema:str):
    ann = schema[5:9]+"-"+schema[10:15]
    return ann

def creaate_registre(schema:str):
    reg = schema[12:15]
    return reg

def decode_text(text:str) -> str:
     strd = text.replace(" ","_")
     return unidecode(strd)

def get_max(sems_a:str, sems_b:str)-> str:
    value_1 = sems_a.upper().partition("S")[2]
    value_2 = sems_b.upper().partition("S")[2]
    if int(value_1) > int(value_2):
        return sems_a
    return sems_b

def get_min(sems_a:str, sems_b:str)-> str:
    value_1 = sems_a.upper().partition("S")[2]
    value_2 = sems_b.upper().partition("S")[2]
    if int(value_1) > int(value_2):
        return sems_b
    return sems_a

def get_credit(value:float, credit:int) -> int:
    if value >= 10:
        return credit
    return 0

def max_value(value_1:float, value_2:float) -> float:
    if value_1 >= value_2:
        return value_1
    return value_2


def get_niveau(sems_a:str, sems_b:str)-> str:
    value_1 = get_max(sems_a,sems_b).upper().partition("S")[2]

    if int(value_1) <= 2 :
        return "L1"
    elif int(value_1) <= 4:
        return "L2"
    elif int(value_1) <= 6:
        return "L3"
    elif int(value_1) <= 8:
        return "M1"
    elif int(value_1) <= 10:
        return "M2"

def validation_semestre(etudiant:Any, sems:str, credit:int, total_cred:int,anne:str):
    response = {}
    response["anne"]=anne
    for index,sems_i in enumerate(etudiant.semestre):
        if sems == sems_i:
            if credit == total_cred:
                response["status"]=f"Étudiant(e) ayant validé(e) la {total_cred} crédit définitive."
                response["code"]=True
            else:
                response["status"]= f"Étudiant(e) ayant validé(e) la {total_cred} crédit par compensation."
                response["code"]=True
            response["anne"]=etudiant.anne[index]
        else:
                response["status"]="Étudiant(e) redoublé(e)"
                response["code"]=False
    return response


def send_new_account(email_to: str, password: str) -> str:
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.EMAILS_FROM_EMAIL
    sender_password = settings.PASSWORD_FROM_EMAIL

    message = f"""\
        FROM: Faculté des Sciences
        To: {email_to}
        Subject: Nouveau compte FacScience
        Nouveau compte:\n
        Username: {email_to}
        Password: {password}
        """
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email,sender_password)
        server.sendmail(sender_email,email_to,message)

def check_email_valide(email: EmailStr) -> str:
    response = requests.get("https://isitarealemail.com/api/email/validate",
    params={"email":email})
    status = response.json()["status"]
    return status

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)

