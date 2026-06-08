Pull requests are welcome. For new features or fixing bugs, please create a GitHub issue first. Otherwise, you can fix grammar and spelling for UI labels and their translations. Before contributing, read the information below.

Consult [the deployment manual](https://github.com/entropy64t/LostAndFound_SchoolProject/tree/main?tab=readme-ov-file#deployment) to run the app on your development machine.

This project uses [Flask](https://flask.palletsprojects.com/en/stable/) for the backend, [Jinja](https://jinja.palletsprojects.com/en/stable/) to render HTML pages, [SQLAlchemy](https://www.sqlalchemy.org/) for interacting with the [PostgreSQL](https://www.postgresql.org/) databse, and [Babel](https://babel.pocoo.org/en/latest/) for managing Polish translations.

The project structure is as follows:
- `/`
    - `routes.py` manages most backend logic, specifically all HTTP endpoints
    - Several other python scripts do ORM, email sending, and report scoring
- `/templates` contains all Jinja HTML templates, rendered from `routes.py`
- `/static` contains CSS styles for `/templates`
- `/translations` contains GNU gettext PO files used by Babel
