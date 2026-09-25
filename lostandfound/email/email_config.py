from string import Template

from lostandfound import lang

from ..config import SENDER_EMAIL_DOMAIN

NAME = "LostAndFound"

NOREPLY_ADDRESS = f"{NAME} <noreply@{SENDER_EMAIL_DOMAIN}>"

OTP_SUBJECT = Template(lang("Your LostAndFound code is $otp"))

OTP_MAIL = Template(
    lang("""Use the following code to verify your LostAndFound account: 
**$otp**

The code is valid for **30 minutes**.""")
)

PWRSET_SUBJECT = lang("Your LostAndFound password reset link")
PWRESET_MAIL = Template(
    lang("""Use the following link to reset your LostAndFound account password:
$link

The link is single-use only and valid for **30 minutes**.""")
)

EMAIL_FOOTER = Template(
    lang("""
Account details:
E-mail: $email
Name: $name""")
)
