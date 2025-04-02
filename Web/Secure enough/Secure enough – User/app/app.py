from flask import Flask, session, redirect, url_for, request, render_template
import sqlite3
import os
from uuid import uuid4
import requests

app = Flask(__name__)
app.secret_key = str(uuid4())

TWO_FA_SERVICE = "http://2fa:8080"

if os.path.exists('database.db'):
    os.system('rm database.db')

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, 
                username TEXT UNIQUE, 
                password TEXT,
                email TEXT,
                otp_secret TEXT,    
                is_admin INTEGER DEFAULT 0,
                two_fa_enabled INTEGER DEFAULT 0)''')

    users = [
        ('admin', 'admin', 'admin@company.com', 'REDACTED', 1, 1),
        ('sasha_gendir', 'sasha_gendir', 'sasha_gendir@example.com', 'REDACTED', 0, 0)
    ]
    
    for user in users:
        try:
            c.execute("INSERT INTO users (username, password, email, otp_secret, is_admin, two_fa_enabled) VALUES (?, ?, ?, ?, ?, ?)", user)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()


init_db()

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def verify_otp(secret, token):
    data = {"secret": secret, "token": token}
    response = requests.post(f"{TWO_FA_SERVICE}/verify-otp", json=data)
    return response.status_code == 200

@app.route('/')
def index():
    return render_template('login.html', error_message="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            if user['two_fa_enabled']:
                session['otp_required'] = True
                return redirect(url_for('verify_2fa'))
            else:
                session['authenticated']= True
                return redirect(url_for('my_profile'))
        return render_template('login.html', error_message="Invalid credentials")
    return render_template('login.html', error_message="")

@app.route('/forgot', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        conn = get_db()
        user = conn.execute ("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user:
            response = requests.get(f"{TWO_FA_SERVICE}/generate-secret")
            if response.status_code == 200:
                secret_data = response.json()
                otp_secret = secret_data['secret']

            conn = get_db()
            conn.execute("UPDATE users SET otp_secret = ? WHERE username = ?", (otp_secret, username))
            conn.commit()
            conn.close()

            session['user_id'] = user['id']
            session['otp_required'] = True
            return redirect(url_for('link_sent'))
        return render_template('forget_pass.html', error_message="User not found", success_message="")
    return render_template('forget_pass.html')


@app.route('/link_sent')
def link_sent():
    success_message = 'Password reset link has been sent'
    session.clear()
    return render_template('forget_pass.html', success_message=success_message)


@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'user_id' not in session or not session.get('otp_required'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        otp_secret = request.form['otp_secret']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        if user and verify_otp(user['otp_secret'], otp_secret):
            session['authenticated'] = True
            session['otp_required'] = False
            return redirect(url_for('my_profile'))
        else:
            return render_template('verify.html', error_message="Invalid OTP code")
    
    return render_template('verify.html', error_message="")

@app.route('/my_profile')
def my_profile():
    if 'user_id' in session and session.get('authenticated'):
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        
        if user:
            if user['is_admin'] == 1:
                flag = os.getenv('FLAG', 'No flag found')
                return render_template('profile.html', username=user['username'], flag=flag)
            else:
                return render_template('profile.html', username=user['username'])
    
    return render_template('login.html',success_message="", error_message="Access denied")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
