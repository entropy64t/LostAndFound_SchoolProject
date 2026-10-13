pybabel extract -F lostandfound/babel.cfg -k lang -o messages.pot .

pybabel init -i messages.pot -d lostandfound/translations -l pl
