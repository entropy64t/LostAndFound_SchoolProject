import resend

from lostandfound.user import User

from ..config import EMAIL_WHITELIST, USER_EMAIL_DOMAIN
from .email_config import (
    NOREPLY_ADDRESS,
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


def send_email(to: str, subject: str, content: str):
    params: resend.Emails.SendParams = {
        "from": NOREPLY_ADDRESS,
        "to": to,
        "subject": subject,
        "html": content,
    }
    return resend.Emails.send(params)


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
