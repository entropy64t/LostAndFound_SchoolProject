from string import Template

from flask_babel import gettext as lang

from lostandfound.utility.markdown import parse_markdown

from ..config import SENDER_EMAIL_DOMAIN

NAME = "LostAndFound"

NOREPLY_ADDRESS = f"noreply@{SENDER_EMAIL_DOMAIN}"
NOREPLY_FULLNAME = f"{NAME} <{NOREPLY_ADDRESS}>"
CONTACT_ADDRESS = f"contact@{SENDER_EMAIL_DOMAIN}"
CONTACT_FULLNAME = f"{NAME} <{CONTACT_ADDRESS}>"


def otp_subject():
    return Template(lang("email.otp.subject"))


def otp_mail():
    return Template(parse_markdown(lang("email.otp.content")))


def pwreset_subject():
    return lang("email.pwreset.subject")


def pwreset_mail():
    return Template(parse_markdown(lang("email.pwreset.content")))


def email_footer():
    return Template(lang("email.footer"))
