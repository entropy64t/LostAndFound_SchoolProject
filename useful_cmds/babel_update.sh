pybabel extract -F lostandfound/babel.cfg -k lang -o messages.pot .

pybabel update -i messages.pot -d lostandfound/translations
