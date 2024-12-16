from src.instance.db import get_db
from datetime import datetime

def getUserInfosUid(uid):
    db = get_db()
    result = db.execute('SELECT * FROM users WHERE id = ?', (uid,)).fetchone()

    return result if result else None

def getUserInfos(firstName, lastName, birth):
    cvbirth = datetime.strptime(birth, "%Y-%m-%d")
    convertedBirth = cvbirth.strftime("%Y-%m-%d")
    print(convertedBirth)
    db = get_db()
    result = db.execute('SELECT * FROM users WHERE first_name = ? AND last_name = ? AND date_of_birth = ?', (firstName, lastName, convertedBirth,  )).fetchone()

    return result if result else None

def getCardInfos(card_id):
    db = get_db()
    result = db.execute('SELECT * FROM cards WHERE id = ?', (card_id,)).fetchone()
    
    return result if result else None

