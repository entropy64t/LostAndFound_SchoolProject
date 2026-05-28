pybabel extract -F babel.cfg -k lang -o messages.pot .

pybabel init -i messages.pot -d translations -l pl