# LostAndFound

LostAndFound is a web application for decentralized trafcking of lost and found items across public buildings (e.g. schools, office buildings, libraries, community centers). Users who have verified ownership of the organization's email address can create and browse reports. Lost and found reports are tried to be automatically matched into pairs based on a simple scoring system.

The instance deployed for the 5th High School in Kraków is available at <https://lost-and-found-app.graysmoke-0e4ec27f.westeurope.azurecontainerapps.io/login>. [Give feedback for that instance.](https://forms.gle/QAZikmCdNK2SZ5t56)

The sample list of rooms comes from [dominik-korsa/timetable](https://github.com/dominik-korsa/timetable).

## Contributing

Read the below section for details on how to deploy for development. Then see [CONTRIBUTING.md](https://github.com/entropy64t/LostAndFound_SchoolProject/tree/main?tab=contributing-ov-file).

## Deployment

1. Configure the databse
    - Install PostgreSQL on your system.
    - Customize `db_init/sample_categories.sql`, `db_init/sample_colours.sql`, `db_init/sample_grades.sql`, `db_init/sample_locations.sql` according to your needs. (The database schema is in `db_init/db_init.sql`.)
    - Replace the `postgres` database user's password in `useful_cmds/db_setup.sh` to match your set password. Or use any other PostgreSQL user with similar permissions.
    - `$ useful_cmds/db_setup.sh`
2. Prepare Python and Flask
    - Create a venv and install `requirements.txt`
    - Set environment variables required in `server_secrets.py` using `$ export varname="value"`
        - `lostandfound_sender_address` - an email address you own from which automated system emails will be sent
        - `lostandfound_sender_password` - the SMTP password for that account (for Gmail this must be a key generated in `My Account > Security & sign-in > 2-Step Verification > App passwords`)
        - `lostandfound_sender_replyto_address` - what email address replies to those automated emails should go to
        - `lostandfound_secret_key` - a secret long random string, e.g. Python's `secrets.token_hex(16)`
        - `lostandfound_connection_string` - the PostgreSQL connection string: `postgresql://user:password@host/LostAndFound`, create a dedicated PostgreSQL user for the Flask web app and replace `user` and `password`
    - Replace the timezone in `server_secrets.py` with your instance's timezone
    - Replace `email_domain` in `server_secrets.py` with your organization's email address domain (for users to verify their accounts).
    - Setup Babel: compile messages.po (`$ pybabel compile -d translations`)
3. Run the server
    - In a development environment, run directly from Flask:
        - `$ flask --app app.py run`
    - In a production environment:
        - Change `app.run(...)` in `app.py` to `app.run(host="0.0.0.0", port=5000)`
        - Run the Gunicorn WSGI server: `$ gunicorn --bind 0.0.0.0:5000 app:app`
        - You can use a different port.
