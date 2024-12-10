from src.instance.db import get_db

def insertUser(name, email, password):
    db = get_db()
    db.execute('INSERT INTO users (first_name, email, password) VALUES (?, ?, ?)', (name, email, password))
    db.commit()

def getUserByEmail(email):
    db = get_db()
    result = None
    result = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if result is not None:
        return True
    else:
        return False

def checkIfUserAlreadyExists(name, email, password):
    db = get_db()
    result = None
    result = db.execute('SELECT * FROM users WHERE first_name = ? AND email = ? AND password = ?', (name, email, password,)).fetchone()
    if result is not None:
        return True
    else:
        return False

def finishAuth(lastName, birth, city_residence, city, street, phone, status, salary, user_id):
    db = get_db()
    db.execute(
        '''
        UPDATE users
        SET last_name = ?, date_of_birth = ?, residence_country = ?, city = ?, street = ?, phone_number = ?, marital_status = ?, annual_salary = ?
        WHERE id = ?
        ''',
        (lastName, birth, city_residence, city, street, phone, status, salary, user_id)
    )
    db.commit()
