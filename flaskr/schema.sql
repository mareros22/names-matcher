DROP TABLE IF EXISTS names;
DROP TABLE IF EXISTS sex;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS origins;
DROP TABLE IF EXISTS yearCounts;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS families;
DROP TABLE IF EXISTS familyMembers;
DROP TABLE IF EXISTS likedNames;
DROP TABLE IF EXISTS dislikedNames;
DROP TABLE IF EXISTS preferences;
DROP TABLE IF EXISTS notes;

/*Tables to manage names and related data*/
CREATE TABLE names(
    name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE sex(
    name VARCHAR(255),
    sex VARCHAR(255)
);

CREATE TABLE countries(
    country VARCHAR(255) PRIMARY KEY
);

CREATE TABLE origins(
    country varchar(255),
    name varchar(255)
);

CREATE TABLE yearCounts(
    name VARCHAR(255),
    year INTEGER,
    count INTEGER
);

/*Tables to manage users, families, and user activity*/
CREATE TABLE users(
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL

);

CREATE TABLE families(
    familyID VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE familyMembers(
    familyID VARCHAR(255),
    username VARCHAR(255)
);

CREATE TABLE likedNames(
    username VARCHAR(255),
    name VARCHAR(255)
);

CREATE TABLE dislikedNames(
    username VARCHAR(255),
    name VARCHAR(255)
);

CREATE TABLE preferences(
    familyID VARCHAR(255) PRIMARY KEY,
    male TEXT,
    female TEXT,
    unisex TEXT
);

CREATE TABLE notes(
    username VARCHAR(255),
    name VARCHAR(255),
    note VARCHAR(511)
);
