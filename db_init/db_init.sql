BEGIN;

CREATE EXTENSION citext;

CREATE TABLE users (
	id serial PRIMARY KEY,
	email citext UNIQUE NOT NULL,
	password text NOT NULL,
	passwordSalt text NOT NULL,
	otp text,
	otpSalt text,
	accountVerified boolean NOT NULL
);

CREATE TABLE locations (
	id serial PRIMARY KEY,
	buildingLevel smallint,
	name text
);

CREATE TABLE colours (
	id serial PRIMARY KEY,
	name text,
	colourValue integer
);

CREATE TABLE categories (
	id serial PRIMARY KEY,
	name text
);

CREATE TYPE reportType AS ENUM ('lost', 'found');

CREATE TABLE reports (
	id serial PRIMARY KEY,
	creationDate timestamptz,
	author integer REFERENCES users(id),
	type reportType NOT NULL,

	category integer REFERENCES categories(id),
	colour integer REFERENCES colours(id),
	title text,
	description text,
	imageUrls text[],

	lastSeen timestamptz,
	lastSeenLocation integer REFERENCES locations(id),
	itemOwner integer REFERENCES users(id),
	pickupLocation integer REFERENCES locations(id)
);

COMMIT;
