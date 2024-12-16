import os
from datetime import datetime
import random
import json
from flask import Flask, render_template, request, flash, redirect, url_for, session
from src.instance import db
from src.models.register import insertUser, getUserByEmail, checkIfUserAlreadyExists, finishAuth
from src.models.login import isUserRegistered
from src.models.home import getHistoryByCardId, insertCard, insertHistory, getUserId, getCardNumber, getBalance, getExpiration, getCardId, updateBalance, find, updateBalanceTransfer
from src.models.admin import getUserInfos, getUserInfosUid, getCardInfos

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite')
    )

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize database
    db.init_app(app)
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            db.init_db()
            print("Database initialized.")



    @app.route('/', methods=['GET', 'POST'])
    def auth():
        form_type = request.form.get('form_type')

        if form_type == 'sign_in':
            email = request.form.get('loginEmail')
            password = request.form.get('loginPassword')
            if email == "admin" and password == "admin":
                return redirect(url_for('admin'))
            isRegistered = isUserRegistered(email, password)
            if isRegistered == True:
                userId = getUserId(email, password)
                session['userId'] = userId

                return redirect(url_for('home'))

        elif form_type == 'sign_up':
            name = request.form.get('registerName')
            email = request.form.get('registerEmail')
            password = request.form.get('registerPassword')
            alreadyExists = checkIfUserAlreadyExists(name, email, password)

            if alreadyExists == True:
                flash('User with this email already exists', category='error')
                return render_template('pages/auth.html')
            insertUser(name, email, password)
            isInserted = getUserByEmail(email)
            userId = getUserId(email,password)

            card_number = " ".join(["".join([str(random.randint(0, 9)) for _ in range(4)]) for _ in range(4)])
            insertCard("11/2030", card_number, 2000, userId)
            if isInserted == True:
                session['userId'] = userId
                return redirect(url_for('home'))

        else:
            flash('Invalid form submission', category='error')
        
        return render_template('pages/auth.html')
    

    @app.route('/home', methods=['GET', 'POST'])
    def home():
        userId = session.get('userId')  # Get userId from session
        if userId is None:
            return redirect(url_for('auth'))
        
        user_info = getUserInfosUid(userId)
        cardNumber = getCardNumber(userId)
        expiration = getExpiration(userId)
        balance = getBalance(userId)
        cardId = getCardId(userId)


        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'transfer':
                transferName = request.form.get('name')
                transferCard = request.form.get('cardNumber')
                amounttr = request.form.get('amount')
                transferAmount = "-" + amounttr
                transferAmount2 = "+" + amounttr
                
                exists = find(transferCard)
                    
                if exists:
                    current_date = datetime.now().date()
                    current_time = datetime.now().strftime('%H:%M')
                    #from
                    insertHistory(current_date, current_time, transferName, transferAmount, cardId )
                    updateBalanceTransfer(transferCard, transferAmount2)
                    balance = updateBalance(cardId, transferAmount, balance)
                    #To
                    insertHistory(current_date, current_time, user_info['first_name'], transferAmount2, exists)


        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'transaction':
                name = request.form.get('name')
                date = request.form.get('date')
                time = request.form.get('time')
                amount = request.form.get('amount')

                # Validate required fields
                if not (name and date and time and amount):
                    flash("All fields are required for a transaction.", category="error")
                else:
                    insertHistory(date, time, name, amount, cardId)
                    balance = updateBalance(cardId, amount, balance)

        balance = getBalance(userId)
        history = getHistoryByCardId(cardId)
        transactions = history.fetchall()
        transactions_list = [dict(row) for row in transactions]
        return render_template(
            'pages/home.html',
            cardNumber=cardNumber,
            expiration=expiration,
            balance=balance,
            transactions=transactions_list,
            user=user_info
        )

    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        user_info = None

        if request.method == 'POST':
            form_type = request.form.get('form_type')

            firstName = request.form.get('firstName')
            lastName =  request.form.get('lastName')
            birth =  request.form.get('birth')
            uid =  request.form.get('uid')

            if form_type == 'search':
                if firstName and lastName and birth:
                    user_info = getUserInfos(firstName, lastName, birth)
                    user_id = getUserId(user_info['email'], user_info['password'])
                    cardId = getCardId(user_id)
                    card_info = getCardInfos(cardId)
                    history = getHistoryByCardId(cardId)
                    transactions = history.fetchall()

                    return render_template('pages/adminSearch.html', user=user_info, transactions=transactions, card=card_info )
                elif uid:
                    user_info = getUserInfosUid(uid)
                    cardId = getCardId(uid)
                    card_info = getCardInfos(cardId)
                    history = getHistoryByCardId(cardId)
                    transactions = history.fetchall()

                    return render_template('pages/adminSearch.html', user=user_info, transactions=transactions, card=card_info )

        return render_template('pages/admin.html', user=user_info)


    @app.route('/logout')
    def logout():
        session['userId'] = None
        return redirect(url_for('auth'))

    @app.route('/notEligible')
    def notEligible():
        return render_template('pages/notEligible.html')

    @app.route('/adminSearch',  methods=['GET', 'POST'])
    def adminSearch():
        return render_template('pages/adminSearch.html')


    @app.route('/notActivated', methods=['GET', 'POST'])
    def notActivated():
        userId = session.get('userId')

        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'auth':
                lastName = request.form.get('lastName')
                birth = request.form.get('birth')
                ctResidence = request.form.get('ctResidence')
                ct = request.form.get('ct')
                street = request.form.get('street')
                phone = request.form.get('phone')
                status = request.form.get('status')
                salary = request.form.get('salary')

                intSalary = int(salary)

                if intSalary < 36000:
                    return redirect(url_for('notEligible'))
                else:
                    finishAuth(lastName, birth, ctResidence, ct, street, phone, status, salary, userId)
                    return redirect(url_for('home'))

        return render_template('pages/notActivated.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)
