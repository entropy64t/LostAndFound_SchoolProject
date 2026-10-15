import resend
import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from lostandfound.models import User

from ..config import EMAIL_WHITELIST, USER_EMAIL_DOMAIN, FALLBACK_SENDER_ADDRESS, FALLBACK_SENDER_PASSWORD
from .email_config import (
    CONTACT_FULLNAME,
    email_footer,
    otp_mail,
    otp_subject,
    pwreset_mail,
    pwreset_subject,
)


def verify_domain(email: str):
    if email in EMAIL_WHITELIST.split("|"):
        return True
    return email.split("@")[1] == USER_EMAIL_DOMAIN

port = 465
context = ssl.create_default_context()

def send_email(to: str, subject: str, content: str):
    try:
        params: resend.Emails.SendParams = {
            "from": CONTACT_FULLNAME,
            "to": to,
            "subject": subject,
            "html": content,
        }
        response = resend.Emails.send(params)
        return response
    except:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as mail_server:
            mail_server.login(FALLBACK_SENDER_ADDRESS, FALLBACK_SENDER_PASSWORD)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = CONTACT_FULLNAME
            msg['To'] = to
            msg.attach(MIMEText(content, 'plain'))
            msg.attach(MIMEText(content, 'html'))

            mail_server.send_message(msg, FALLBACK_SENDER_ADDRESS)

def send_otp(to: str, account: User, otp_plaintext: str):
    send_email(
        to,
        otp_subject().substitute(otp=otp_plaintext),
        otp_mail().substitute(otp=otp_plaintext)
        + email_footer().substitute(name=account.display_name, email=account.email),
    )


def send_pwreset(to: str, account: User, reset_link: str):
    send_email(
        to,
        pwreset_subject(),
        pwreset_mail().substitute(link=reset_link)
        + email_footer().substitute(name=account.display_name, email=account.email),
    )
