from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import qrcode
import os
import random
import string

# Flask app setup
app = Flask(__name__)
app.secret_key = "securekey"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    otp_key = db.Column(db.String(6), nullable=True)

# Helper functions
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        phone_number = request.form['phone_number']

        if User.query.filter_by(username=username).first():
            return "Username already exists!", 400

        new_user = User(username=username, password=password, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect(url_for('confirm_password'))
        return "Invalid username or password!", 401
    return render_template('login.html')

@app.route('/confirm_password', methods=['GET', 'POST'])
def confirm_password():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user = User.query.filter_by(username=session['user']).first()
        password = request.form['password']

        if bcrypt.check_password_hash(user.password, password):
            return redirect(url_for('generate_qr'))
        return "Password confirmation failed!", 401
    return render_template('confirm_password.html')

@app.route('/generate_qr', methods=['GET', 'POST'])
def generate_qr():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['user']).first()

    if request.method == 'POST':
        otp = generate_otp()
        user.otp_key = otp
        db.session.commit()

        # Generate QR Code with OTP
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(otp)
        qr_path = os.path.join('static', f"{user.username}_otp_qrcode.png")
        qr.make_image(fill='black', back_color='white').save(qr_path)

        return render_template('display_qr.html', qr_code=qr_path)
    return render_template('generate_qr.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['user']).first()
    otp = request.form['otp']

    if otp == user.otp_key:
        user.otp_key = None  # Invalidate OTP
        db.session.commit()
        return render_template('success.html', message="Authentication successful!")
    return render_template('error.html', message="Invalid OTP! Please try again.")

@app.route('/success')
def success():
    username = session.get('username')
    if not username:
        return redirect('/login')

    user = users_db.get(username)
    phone_number = user['phone_number']
    carrier = user['carrier']

    # Send SMS notification
    send_sms(phone_number, carrier, "You have logged in successfully!")

    # Render success page with message and image
    return render_template('success.html', message="Login successful! Welcome to your dashboard.", image_url="/static/images/success.png")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
