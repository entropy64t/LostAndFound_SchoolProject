# LostAndFound
## Postgres database setup
- ```$ sudo -u postgres -i```
- - ```$ psql```
- - - ```ALTER USER postgres WITH PASSWORD 'postgres291830';```
- - - ```\q```
- ```$ createdb LostAndFound```
- ```$ psql -d LostAndFound -f db_init/db_init.sql```
- ```$ psql -d LostAndFound -f db_init/sample_colours.sql```
- ```$ psql -d LostAndFound -f db_init/sample_locations.sql```
- ```$ psql -d LostAndFound -f db_init/sample_categories.sql```
