import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from secure_crypto import encrypt_file, decrypt_file
import os, jwt, datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# === JWT Decorator ===
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

# === Routes ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    if c.fetchone():
        conn.close()
        return render_template('message.html', message="⚠️ User already exists. Please log in.")

    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
    conn.commit()
    conn.close()
    return render_template('message.html', message="✅ Account created successfully. You can now log in.")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == '1234':
        token = jwt.encode({
            'user': data['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/encrypt', methods=['POST'])
@token_required
def encrypt():
    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'Missing file or password'}), 400
    file = request.files['file']
    password = request.form['password']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    encrypted_path = encrypt_file(filepath, password)
    return jsonify({'message': 'File encrypted', 'file': encrypted_path})

@app.route('/decrypt', methods=['POST'])
@token_required
def decrypt():
    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'Missing file or password'}), 400
    file = request.files['file']
    password = request.form['password']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    decrypted_path = decrypt_file(filepath, password)
    return jsonify({'message': 'File decrypted', 'file': decrypted_path})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
