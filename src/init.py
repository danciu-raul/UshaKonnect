import os
from flask import Flask, render_template, request, flash
from src.instance import db
from src.models.register import insertUser, getUserByEmail, checkIfUserAlreadyExists
from src.models.login import isUserRegistered
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

    # Define routes
    @app.route('/', methods=['GET', 'POST'])
    def auth():
        
        form_type = request.form.get('form_type')  # Check which form was submitted

        if form_type == 'sign_in':  # Handle login form
            email = request.form.get('loginEmail')
            password = request.form.get('loginPassword')
            isRegistered = isUserRegistered(email, password)
            if isRegistered:
                return render_template('pages/home.html')

        elif form_type == 'sign_up':  # Handle registration form
            name = request.form.get('registerName')
            email = request.form.get('registerEmail')
            password = request.form.get('registerPassword')
            alreadyExists = checkIfUserAlreadyExists(name, email, password)
            if alreadyExists == True:
                flash('User with this email already exists', category='error')
                return render_template('pages/auth.html')
            insertUser(name, email, password)
            isInserted = getUserByEmail(email)
            print(isInserted)
            if isInserted == True:
                return render_template('pages/home.html')
        else:
            flash('Invalid form submission', category='error')
        
        return render_template('pages/auth.html')

    @app.route('/home')
    def home():
        return render_template('pages/home.html')

    @app.route('/admin')
    def admin():
        return render_template('pages/admin.html')

    @app.route('/notActivated')
    def notActivated():
        return render_template('pages/notActivated.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)
