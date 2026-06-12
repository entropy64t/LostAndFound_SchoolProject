BEGIN;

CREATE EXTENSION IF NOT EXISTS citext;

DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS colours;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS grades;
DROP TYPE IF EXISTS reportType;

CREATE TABLE grades (
	id serial PRIMARY KEY,
	name text
);

CREATE TABLE users (
	id serial PRIMARY KEY,
	email citext UNIQUE NOT NULL,
	display_name text NOT NULL,
	password text NOT NULL,
	otp text,
	otp_creation timestamptz,
	pwreset text,
	pwreset_creation timestamptz,
	account_verified boolean NOT NULL,
	grade integer REFERENCES grades(id)
);

CREATE TABLE locations (
	id serial PRIMARY KEY,
	building_level smallint,
	name text
);

CREATE TABLE colours (
	id serial PRIMARY KEY,
	name text,
    display_name text,
    display_name_pl text,
	colour_value text
);

CREATE TABLE categories (
	id serial PRIMARY KEY,
	name text,
    name_pl text
);

CREATE TYPE reportType AS ENUM ('lost', 'found');

CREATE TABLE reports (
	id serial PRIMARY KEY,
	creation_date timestamptz,
	author integer REFERENCES users(id) ON DELETE CASCADE,
	type reportType NOT NULL,

	category integer REFERENCES categories(id),
	colour integer REFERENCES colours(id),
	title text,
	description text,
	image_urls text[],

	last_seen timestamptz,
	last_seen_location integer REFERENCES locations(id),
	item_owner integer REFERENCES users(id) ON DELETE SET NULL,
	pickup_location integer REFERENCES locations(id)
);

CREATE TABLE matches (
    id serial PRIMARY KEY,
    lost_item integer REFERENCES reports(id) ON DELETE CASCADE,
    found_item integer REFERENCES reports(id) ON DELETE CASCADE,
    score integer,
    creation_date timestamptz
);

COMMIT;
