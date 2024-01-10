
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL
    CHECK (position('@' IN email) > 1),
  username VARCHAR(25) NOT NULL,

  image_url TEXT,
  header_image_url TEXT,
  bio TEXT,
  location TEXT,
  
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
password TEXT NOT NULL,
);

CREATE TABLE boardgames (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
)

CREATE TABLE follows (
    user_being_followed_id INTEGER references users ON DELETE CASCADE
    user_following_id INTEGER references users ON DELETE CASCADE,
    PRIMARY KEY (user_being_followed_id, user_following_id)
)

CREATE TABLE ownerships (
    owner TEXT REFERENCES users ON DELETE CASCADE,
    owned_game TEXT REFERENCES boardgames ON DELETE CASCADE,
    PRIMARY KEY (owner, owned_game)
)


CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  salary INTEGER CHECK (salary >= 0),
  equity NUMERIC CHECK (equity <= 1.0),
  company_handle VARCHAR(25) NOT NULL
    REFERENCES companies ON DELETE CASCADE
);

CREATE TABLE applications (
  username VARCHAR(25)
    REFERENCES users ON DELETE CASCADE,
  job_id INTEGER
    REFERENCES jobs ON DELETE CASCADE,
  PRIMARY KEY (username, job_id)
);