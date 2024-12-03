import os
from flask import Flask, render_template
from src.instance import db

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
    def main():
        #login = LoginForm()
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
    app.run(debug=True)
