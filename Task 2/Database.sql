DROP TABLE IF EXISTS users Cascade;
CREATE TABLE users(
	id serial PRIMARY KEY,
	user_login TEXT NOT NULL Unique, 
	user_password TEXT NOT NULL,
	UNIQUE(user_login));
	

DROP TABLE IF EXISTS notes;
CREATE TABLE notes(
	user_id INT NOT NULL,
	note_id serial PRIMARY KEY, 
	note TEXT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (id))