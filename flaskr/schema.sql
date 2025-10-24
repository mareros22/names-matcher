DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS name;
DROP TABLE IF EXISTS family;

CREATE TABLE name (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT UNIQUE NOT NULL,
   sex TEXT,
   count INTEGER,
   year INTEGER,
   lands ARRAY
);

CREATE TABLE family (
   fam_id TEXT PRIMARY KEY,
   member1 INTEGER,
   member2 INTEGER,
   password TEXT NOT NULL,
   male TEXT,
   female TEXT,
   unisex TEXT,
   FOREIGN KEY (member1) REFERENCES user (id),
   FOREIGN KEY (member2) REFERENCES user (id)
);

CREATE TABLE user (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT UNIQUE NOT NULL,
   password TEXT NOT NULL,
   fam_id TEXT,
   FOREIGN KEY (fam_id) REFERENCES family (fam_id)
);

CREATE TABLE liked_names(
   user_id INTEGER PRIMARY KEY,
   name_id ARRAY
)