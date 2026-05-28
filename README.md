# LostAndFound

## Setup
 - Create a venv and install requirements.txt
 - Postgres database setup in `useful_cmds/db_setup.sh`
 - Create a `server_secrets.py` file from the template
   - `sender_email` an email
   - `sender_password` password (for gmail generated in `My account > Security&sign-in > 2FA > App passwords`)
 - Setup babel (`useful_cmds/babel_init.sh`) and compile messages.po (`$> pybabel compile -d translations`)
