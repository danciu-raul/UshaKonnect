from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
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

if __name__ == '__main__':
    app.run(debug=True)
