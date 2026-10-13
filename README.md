# LostAndFound

LostAndFound is a web application for decentralized tracking of lost and found items across public buildings (e.g. schools, office buildings, libraries, community centers). Users who have verified ownership of the organization's email address can create and browse reports. Lost and found reports are tried to be automatically matched into pairs based on a simple scoring system.

The instance deployed for the 5th High School in Kraków is available at <https://finditvlo.pl>. [Give feedback for that instance.](https://forms.gle/QAZikmCdNK2SZ5t56)

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
    - Copy `server_secrets.py.template` to `server_secrets.py`
    - Set environment variables required in `server_secrets.py` using `$ export varname="value"` or by placing them in a `.env` file in the project root directory
        - `TIMEZONE` - your instance's timezone as an IANA timezone string
        - `RESEND_API` - a [Resend](https://resend.com) API key for sending automated emails from your domain (set to an empty string to use SMTP for email sending instead)
        - `SENDER_EMAIL_DOMAIN` - the domain name for sending emails, as configured in Resend
        - `FALLBACK_SENDER_ADDRESS` - an alternative email address for automated system emails
        - `FALLBACK_SENDER_PASSWORD` - the SMTP password for that account (for Gmail this must be a key generated in `My Account > Security & sign-in > 2-Step Verification > App passwords`)
        - `USER_EMAIL_DOMAIN` - your organization's email address domain (for users to verify their accounts)
        - `EMAIL_WHITELIST` - an additional whitelist of accepted user verification email addresses, separated by `|`
        - `SECRET_KEY` - a secret long random string, e.g. Python's `secrets.token_hex(16)`
        - `DB_URI` - the PostgreSQL connection string: `postgresql://user:password@host/LostAndFound`, create a dedicated PostgreSQL user for the Flask web app and replace `user` and `password`
    - Setup Babel: compile messages.po (`$ pybabel compile -d lostandfound/translations`)
3. Run the server
    - In a development environment, run directly from Flask:
        - `$ flask --app lostandfound/app.py run`
    - In a production environment:
        - Run the Gunicorn WSGI server: `$ gunicorn --bind 0.0.0.0:5000 lostandfound.app:app`
        - You can use a different port.
