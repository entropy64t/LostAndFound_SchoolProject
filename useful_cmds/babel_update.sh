pybabel extract -F babel.cfg -k lang -o messages.pot .

pybabel update -i messages.pot -d translations