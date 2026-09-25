import resend

from lostandfound.user import User
from lostandfound.utility.markdown import parse_markdown

from ..config import USER_EMAIL_DOMAIN
from .email_config import (
    EMAIL_FOOTER,
    NOREPLY_ADDRESS,
    OTP_MAIL,
    OTP_SUBJECT,
    PWRESET_MAIL,
    PWRSET_SUBJECT,
)


def verify_domain(email: str):
    return email.split("@")[1] == USER_EMAIL_DOMAIN


def send_email(to: str, subject: str, content: str) -> None:
    params: resend.Emails.SendParams = {
        "from": NOREPLY_ADDRESS,
        "to": to,
        "subject": subject,
        "html": content,
    }
    resend.Emails.send(params)


def send_otp(to: str, account: User):
    send_email(
        to,
        parse_markdown(OTP_SUBJECT.substitute(otp=account.otp)),
        parse_markdown(
            OTP_MAIL.substitute(otp=account.otp)
            + EMAIL_FOOTER.substitute(name=account.display_name, email=account.email)
        ),
    )


def send_pwreset(to: str, account: User, reset_link: str):
    send_email(
        to,
        parse_markdown(PWRSET_SUBJECT),
        parse_markdown(
            PWRESET_MAIL.substitute(link=reset_link)
            + EMAIL_FOOTER.substitute(name=account.display_name, email=account.email)
        ),
    )
