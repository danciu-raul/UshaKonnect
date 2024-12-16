from src.instance.db import get_db

# CARD

def insertCard(expiration, card_number, balance, user_id):
    db = get_db()
    db.execute('INSERT INTO cards (expiration, card_number, balance, user_id) VALUES (?, ?, ?, ?)', (expiration, card_number, balance, user_id))
    db.commit()

def updateBalance(card_id, amount, balance):
    db = get_db()
    firstChar = amount[0]
    rest = amount[1:]
    
    floatBalance = float(balance)
    toChangeValue = float(rest)


    if firstChar == '+':
        new = floatBalance + toChangeValue
        value = str(new)
        db.execute(
            'UPDATE cards SET balance = ? WHERE id = ?',
            (value, card_id)
        )
    else:
        new = floatBalance - toChangeValue
        value = str(new)
        db.execute(
            'UPDATE cards SET balance = ? WHERE id = ?',
            (value, card_id)
        )

    db.commit()


#
# def getCards(user_id):
#     db = get_db()
#     return db.execute('SELECT cards.* FROM cards INNER JOIN users ON users.id = cards.user_id WHERE users.email = ?', (email,))
#

def getExpiration(user_id):
    db = get_db()
    result = db.execute('SELECT expiration FROM cards WHERE user_id = ?', (user_id,)).fetchone()

    return result['expiration'] if result else None

def getBalance(user_id):
    db = get_db()
    result = db.execute('SELECT balance FROM cards WHERE user_id = ?', (user_id,)).fetchone()

    return result['balance'] if result else None

def getCardNumber(user_id):
    db = get_db()
    result = db.execute('SELECT card_number FROM cards WHERE user_id = ?', (user_id,)).fetchone()

    return result['card_number'] if result else None

# HISTORY

def insertHistory(execution_date, execution_hour, destination, amount, card_id):
    db = get_db()
    db.execute('INSERT INTO history (execution_date, execution_hour, destination, amount, card_id) VALUES (?, ?, ?, ?, ?)', (execution_date, execution_hour, destination, amount, card_id))
    db.commit()

def getHistoryByCardId(card_id):
    db = get_db()
    return db.execute('SELECT * FROM history WHERE card_id = ?', (card_id,))



def getUserId(email, password):
    db = get_db()
    result = db.execute('SELECT id FROM users WHERE email = ? AND password = ?', (email, password,)).fetchone()

    return result['id'] if result else None

def getCardId(user_id):
    db = get_db()
    result = db.execute('SELECT id FROM cards WHERE user_id = ?', (user_id,)).fetchone()

    return result['id'] if result else None

def find(card_number):
    db = get_db()
    result = db.execute('SELECT id FROM cards WHERE card_number = ?', (card_number,)).fetchone()
        
    if result: 
        return result['id']
    else:
        return False

def updateBalanceTransfer(card_number, amount):
    db = get_db()
    
    result = db.execute('SELECT balance FROM cards WHERE card_number = ?', (card_number,)).fetchone()

    if result:
        current_balance = float(result[0])
        
        firstChar = amount[0]
        toChangeValue = float(amount[1:])
        
        if firstChar == '+':
            new_balance = current_balance + toChangeValue
        else:
            new_balance = current_balance - toChangeValue

        db.execute(
            'UPDATE cards SET balance = ? WHERE card_number = ?',
            (str(new_balance), card_number)
        )

        db.commit()
        return True
    else:
        return False  

