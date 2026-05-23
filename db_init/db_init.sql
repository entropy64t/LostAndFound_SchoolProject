BEGIN;

CREATE EXTENSION IF NOT EXISTS citext;

DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS colours;
DROP TABLE IF EXISTS categories;
DROP TYPE IF EXISTS reportType;

CREATE TABLE users (
	id serial PRIMARY KEY,
	email citext UNIQUE NOT NULL,
	password text NOT NULL,
	password_salt text NOT NULL,
	otp text,
	otp_salt text,
	account_verified boolean NOT NULL
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
	colour_value integer
);

CREATE TABLE categories (
	id serial PRIMARY KEY,
	name text
);

CREATE TYPE reportType AS ENUM ('lost', 'found');

CREATE TABLE reports (
	id serial PRIMARY KEY,
	creation_date timestamptz,
	author integer REFERENCES users(id),
	type reportType NOT NULL,

	category integer REFERENCES categories(id),
	colour integer REFERENCES colours(id),
	title text,
	description text,
	image_urls text[],

	last_seen timestamptz,
	last_seen_location integer REFERENCES locations(id),
	item_owner integer REFERENCES users(id),
	pickup_location integer REFERENCES locations(id)
);

COMMIT;
