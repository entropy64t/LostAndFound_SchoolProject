import os
from zoneinfo import ZoneInfo

sender_address = os.environ.get('lostandfound_sender_address') # "verifier@example.com"
sender_replyto_address = os.environ.get('lostandfound_sender_replyto_address') # "another@example.com"
sender_password = os.environ.get('lostandfound_sender_password') # "supersecret"
secret_key = os.environ.get('lostandfound_secret_key') # "flask_app_secret_key"
connection_string = os.environ.get('lostandfound_connection_string') # "postgresql://user:password@host/LostAndFound"

org_timezone = ZoneInfo("Europe/Warsaw")
