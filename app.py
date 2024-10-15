from flask import Flask, render_template, redirect, url_for
from auth.auth import auth_bp
from blood.blood import blood_bp
from stock.stock import stock_bp
from reservations.reservations import reservation_bp

app = Flask(__name__)
app.config.from_object('config.Config')

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(blood_bp, url_prefix='/blood')
app.register_blueprint(stock_bp, url_prefix='/stock')
app.register_blueprint(reservation_bp, url_prefix='/reservations')

# Route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for register page
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/blood_banks')
def blood_banks():
    return render_template('blood_banks.html')


if __name__ == '__main__':
    app.run(debug=True)
