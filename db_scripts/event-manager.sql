CREATE TABLE user_types(
	user_type_id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(30) NOT NULL,
	PRIMARY KEY(user_type_id)
);

CREATE TABLE countries(
	name VARCHAR(30) NOT NULL,
	iso VARCHAR(2) NOT NULL,
	PRIMARY KEY(iso)
);

CREATE TABLE states(
	state_id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(30) NOT NULL,
	abbr VARCHAR(3) NOT NULL,
	country_iso VARCHAR(2) NOT NULL,
	PRIMARY KEY(state_id),
	FOREIGN KEY(country_iso) REFERENCES countries(iso)
);

CREATE TABLE companies (
	company_id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(50) NOT NULL,
	commercial_name VARCHAR(50) NOT NULL,
	logo_url VARCHAR(255),
	phone VARCHAR(10) NOT NULL,
	rfc VARCHAR(50) NOT NULL,
	email VARCHAR(100) NOT NULL,
	website_url VARCHAR(255),
	employee_count INT NOT NULL,
	address VARCHAR(255),
	state_id INT NOT NULL,
	zip_code VARCHAR(50) NOT NULL,
	PRIMARY KEY(company_id),
	FOREIGN KEY(state_id) REFERENCES states(state_id)
);

CREATE TABLE users (
	user_id INT GENERATED ALWAYS AS IDENTITY,
	username VARCHAR(20) NOT NULL,
	email VARCHAR(30) NOT NULL,
	password VARCHAR(60) NOT NULL,
	user_type_id INT,
	company_id INT,
	PRIMARY KEY(user_id),
	FOREIGN KEY(user_type_id) REFERENCES user_types(user_type_id),
	FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE events (
	event_id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(60) NOT NULL,
	description VARCHAR(255) NOT NULL,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	tables INT NOT NULL,
	PRIMARY KEY(event_id)
);

CREATE TABLE tables_event (
	table_id INT GENERATED ALWAYS AS IDENTITY,
	table_num INT NOT NULL,
	event_id INT NOT NULL,
	user_id INT,
	PRIMARY KEY(table_id),
	FOREIGN KEY(event_id) REFERENCES events(event_id),
	FOREIGN KEY(user_id) REFERENCES users(user_id)	
);

-- If you want to delete any table
DROP TABLE users;
DROP TABLE companies;
DROP TABLE states;
DROP TABLE countries;
DROP TABLE events;
DROP TABLE tables_event;
DROP TABLE user_types;

-- If you want to see the tuples in a table
SELECT * FROM user_types;
SELECT * FROM countries;
SELECT * FROM states;
SELECT * FROM companies;
SELECT * FROM users;
SELECT * FROM events;
SELECT * FROM tables_event;