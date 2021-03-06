import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy.sql.expression import true
from sqlalchemy import MetaData, Table

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
from app.db.session import engine


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
    res = "".join(secrets.choice(string.ascii_letters + string.digits) for x in range(10))
    return res


def create_anne(anne: str):
    ann = "anne_" + anne[0:4] + "_" + anne[5:9]
    return ann


def create_num_carte(branche: str, num: str):
    key: str = branche[0:1]
    nbr_zero: int = 6 - len(num)
    response: str = "".join("0" for x in range(nbr_zero))
    return f'{key.upper()}{response}{num}'


def decode_schemas(schema: str):
    ann = f"{schema[5:9]}-{schema[10:15]}"
    return ann


def creaate_registre(schema: str):
    reg = schema[12:15]
    return reg


def decode_text(text: str) -> str:
    strd = text.replace(" ", "_")
    return unidecode(strd)


def get_max(sems_a: str, sems_b: str) -> str:
    if len(sems_a) == 0:
        value_1 = 0
    else:
        value_1 = sems_a.upper().partition("S")[2]

    if len(sems_b) == 0:
        value_2 = 0
    else:
        value_2 = sems_b.upper().partition("S")[2]

    if int(value_1) > int(value_2):
        return sems_a
    return sems_b


def get_min(sems_a: str, sems_b: str) -> str:
    if len(sems_a) == 0:
        value_1 = 0
    else:
        value_1 = sems_a.upper().partition("S")[2]

    if len(sems_b) == 0:
        value_2 = 0
    else:
        value_2 = sems_b.upper().partition("S")[2]
    if int(value_1) > int(value_2):
        return sems_b
    return sems_a


def get_sems_min(niveau: str) -> str:
    if niveau.upper() == "L1":
        return "S1"
    elif niveau.upper() == "M1":
        return "S7"
    elif niveau.upper() == "M2":
        return "S9"


def get_sems_max(niveau: str) -> str:
    if niveau.upper() == "L1":
        return "S2"
    elif niveau.upper() == "M1":
        return "S8"
    elif niveau.upper() == "M2":
        return "S10"


def get_credit(value: float, credit: int) -> int:
    if value >= 10:
        return credit
    return 0


def max_value(value_1: str, value_2: str) -> float:
    if value_1 == "" or value_1 is None:
        value_1 = 0
    if value_2 == "" or value_2 is None:
        value_2 = 0

    if float(value_1) >= float(value_2):
        return value_1
    return value_2


def get_niveau(sems_a: str, sems_b: str) -> str:
    if len(get_max(sems_a, sems_b)) == 0:
        return "Invalid semestre"
    else:
        value_1 = get_max(sems_a, sems_b).upper().partition("S")[2]
    if int(value_1) <= 2:
        return "L1"
    elif int(value_1) <= 4:
        return "L2"
    elif int(value_1) <= 6:
        return "L3"
    elif int(value_1) <= 8:
        return "M1"
    elif int(value_1) <= 10:
        return "M2"


def get_niveau_(sems_a: str, sems_b: str) -> str:
    if len(get_max(sems_a, sems_b)) == 0:
        return "Invalid semestre"
    else:
        value_1 = get_max(sems_a, sems_b).upper().partition("S")[2]
    if int(value_1) <= 2:
        return "PREMIERE ANN??E"
    elif int(value_1) <= 4:
        return "DEUXIEME ANN??E"
    elif int(value_1) <= 6:
        return "TROISI??ME ANN??E"
    elif int(value_1) <= 8:
        return "QUATRI??ME ANN??E"
    elif int(value_1) <= 10:
        return "CINQUI??ME ANN??E"


def get_niveau_long(niv: str) -> str:
    if niv == 'l1':
        return "PREMI??RE ANN??E"
    if niv == 'l2':
        return "DEUXI??ME ANN??E"
    if niv == 'l3':
        return "TROISI??ME ANN??E"
    if niv == 'm1':
        return "QUATRI??ME ANN??E"
    if niv == 'm2':
        return "CINQUI??ME ANN??E"


def validation_semestre(etudiant: Any, sems: str, credit: int, total_cred: int, anne: str):
    response = {}
    response["anne"] = anne
    for index, sems_i in enumerate(etudiant.semestre):
        if sems == sems_i:
            if credit == total_cred:
                response["status"] = f"??tudiant(e) ayant valid??(e) la {total_cred} cr??dit d??finitive."
                response["code"] = True
            else:
                response["status"] = f"??tudiant(e) ayant valid??(e) la {total_cred} cr??dit par compensation."
                response["code"] = True
        else:
            response["status"] = "??tudiant(e) redoubl??(e)"
            response["code"] = False
    return response


def check_table_info(schemas: str) -> list:
    all_table = []
    metadata = MetaData(schema=schemas)
    metadata.reflect(bind=engine)
    for table in metadata.tables:
        table_name = table.replace(f'{schemas}.', '')
        if table_name[0:4] != "note":
            all_table.append(table_name)
    return all_table


def check_table_note(schemas: str) -> list:
    all_table = []
    metadata = MetaData(schema=schemas)
    metadata.reflect(bind=engine)
    for table in metadata.tables:
        table_name = table.replace(f'{schemas}.', '')
        if table_name[0:4] == "note":
            all_table.append(table_name)
    return all_table


def check_columns_exist(schemas: str, table_name: str) -> Optional[List[str]]:
    metadata = MetaData(schema=schemas, bind=engine)
    columns = []
    table_ = Table(table_name, metadata, autoload=True)
    for index, table in enumerate(table_.columns):
        columns.append(str(table).partition(".")[2])
    return columns


def compare_list(list_2: list, list_1: list):
    for key_1 in list_1:
        if key_1 in list_2:
            list_2.remove(key_1)
    return list_2


def get_credit(note_ue: float, credit: int) -> int:
    if note_ue is None:
        return 0
    elif note_ue < 10:
        return 0
    else:
        return credit


def get_status(note_ue: float) -> str:
    if note_ue is None:
        return "Non valid??"
    elif note_ue < 10:
        return "Non valid??"
    else:
        return "Valid??"


def test_semestre(semestre: list, sems_act) -> bool:
    for sems in semestre:
        if sems == sems_act:
            return True
    return False


def send_new_account(email_to: str, password: str) -> str:
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.EMAILS_FROM_EMAIL
    sender_password = settings.PASSWORD_FROM_EMAIL

    message = f"""\
        FROM: Facult?? des Sciences
        To: {email_to}
        Subject: Nouveau compte FacScience
        Nouveau compte:\n
        Username: {email_to}
        Password: {password}
        """
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email_to, message)


def check_email_valide(email: EmailStr) -> str:
    response = requests.get("https://isitarealemail.com/api/email/validate",
                            params={"email": email})
    status = response.json()["status"]
    return status


def excel_to_model(list_note: list):
    all_notes = []
    for note in list_note:
        list_ue = []
        for index, items in enumerate(list(note)):
            all_ue = {"num_carte": note["num_carte"]}
            if items[0:3] == "ue_":
                all_ue["name"] = items[3:len(items)]
                data = list(note)[index + 1:len(note)]
                all_ec = []
                for ec in data:
                    if ec[0:3] == "ec_":
                        value = note[ec]
                        if value is None:
                            ec_ = {"name": ec[3:len(ec)], "note": ""}
                        else:
                            ec_ = {"name": ec[3:len(ec)], "note": value}
                        all_ec.append(ec_)
                    else:
                        break
                all_ue["ec"] = all_ec
                list_ue.append(all_ue)
        all_notes.append(list_ue)
    return all_notes


def transpose(data: list) -> list:
    new_data = []
    for i in range(len(data[0])):
        new_row = []
        for j in range(len(data)):
            new_row.append(data[j][i])
        new_data.append(new_row)
    return new_data


def convert_date(date: str) -> str:
    print("eto zw", date)
    mois = ["Janvier", "F??vrier", "Mars", "Avril", "Mai", "Juin", "Juillet",
            "Aout", "S??ptembre", "Octobre", "Novembre","D??cembre", ""]
    # 1995-10-20
    jours = date[8:10]
    annee = date[0:4]
    mois_ = int(date[5:7])
    print("10", mois[10])
    print("11", mois[11])
    print(jours, mois_ - 1, annee)

    return f"{jours} {mois[mois_ - 1]} {annee}"


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)
