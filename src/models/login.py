from src.instance.db import get_db

def isUserRegistered(email,password):
    db = get_db()
    result = None
    result = db.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password,)).fetchone()
    if result is not None:
        return True
    else:
        return False


