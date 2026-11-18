CREATE DATABASE IF NOT EXISTS wellledger CHARACTER SET utf8mb4;
USE wellledger;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(32) NOT NULL UNIQUE,
    salt VARCHAR(32) NOT NULL,
    password_hash VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS workspaces (
    user_id INT PRIMARY KEY,
    data TEXT NOT NULL,
    saved_at VARCHAR(24) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS daily_expenses (
    user_id INT NOT NULL,
    entry_date DATE NOT NULL,
    category VARCHAR(64) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (user_id, entry_date, category),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sleep_nights (
    user_id INT NOT NULL,
    night DATE NOT NULL,
    hours DECIMAL(5,2) NOT NULL,
    reviewed BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (user_id, night),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS health_entries (
    user_id INT NOT NULL,
    entry_date DATE NOT NULL,
    section VARCHAR(16) NOT NULL,
    details TEXT NOT NULL,
    PRIMARY KEY (user_id, entry_date, section),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
