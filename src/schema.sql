CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  date_of_birth DATE,
  residence_country TEXT,
  city TEXT,
  street TEXT,
  phone_number TEXT,
  marital_status TEXT,
  annual_salary INTEGER
);

CREATE TABLE IF NOT EXISTS cards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  expiration TEXT,
  card_number TEXT,
  balance INTEGER,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  execution_date DATE,
  execution_hour TEXT,
  destination TEXT,
  amount TEXT,
  card_id INTEGER NOT NULL,
  FOREIGN KEY (card_id) REFERENCES cards(id)
);
