import smtplib, ssl
import threading
from server_secrets import *

port = 465
context = ssl.create_default_context()

def verify_domain(address):
    return address.split('@')[-1] == "v-lo.krakow.pl"

def mail_service_send(receiver_address, account_otp, account_mail, account_name):
    message_subject = "Your LostAndFound code is " + account_otp

    message = "Subject:" + message_subject + "\n\nUse the following code to verify your LostAndFound account:\n" + account_otp + "\n\nAccount details:\nE-mail: " + account_mail + "\nName: " + account_name
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as mail_server:
        mail_server.login(sender_address, sender_password)
        mail_server.sendmail(sender_address, receiver_address, message)

def send_message_email(receiver_address, account_otp, account_mail, account_name):
    thread = threading.Thread(target=mail_service_send, daemon=True, args=(receiver_address, account_otp, account_mail, account_name))
    thread.start()
