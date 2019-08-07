CREATE TABLE user (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE gameworld (
  id TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL,
  driver BLOB NOT NULL,
  avatar TEXT NOT NULL,
  game_world TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);
