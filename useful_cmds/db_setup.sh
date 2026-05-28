#!/bin/sh

# Switch to postgres user and execute commands
sudo -u postgres bash <<'EOF'

psql <<SQL
ALTER USER postgres WITH PASSWORD 'postgres291830';
\q
SQL

createdb LostAndFound

psql -d LostAndFound -f db_init/db_init.sql
psql -d LostAndFound -f db_init/sample_colours.sql
psql -d LostAndFound -f db_init/sample_locations.sql
psql -d LostAndFound -f db_init/sample_categories.sql
psql -d LostAndFound -f db_init/sample_grades.sql

EOF

# Return to root shell
exec sudo -i
