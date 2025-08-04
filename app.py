from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
import sqlite3
# Flask app  setup
app = Flask(__name__)
app.secret_key = 'neha_secret_key'  

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users = []

#  User dhundne ka kaam 
def get_user_by_username(username):
    for u in users:
        if u['username'] == username:
            return u
    return None

#  Home Route 
@app.route('/')
def home():
    return render_template('home.html')

# Signup Route 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_type = request.form['user_type']
        line1 = request.form['address_line1']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']

        # pic upload scene
        pic = request.files['profile_picture']
        filename = secure_filename(pic.filename)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # password match check
        if password != confirm_password:
            flash("Password and Confirm Password don't match", "danger")
            return redirect(url_for('signup'))

        # user already exist error
        if get_user_by_username(username):
            flash("Username already exists", "warning")
            return redirect(url_for('signup'))

        user_data = {
            'first_name': fname,
            'last_name': lname,
            'username': username,
            'email': email,
            'password': password,
            'user_type': user_type,
            'profile_picture': filename,
            'address_line1': line1,
            'city': city,
            'state': state,
            'pincode': pincode
        }

        users.append(user_data)
        flash("Signup successful! Please login now", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login Route 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        user = get_user_by_username(uname)

        if user and user['password'] == pwd:
            session['username'] = uname
            if user['user_type'] == 'Patient':
                return redirect(url_for('patient_dashboard'))
            elif user['user_type'] == 'Doctor':
                return redirect(url_for('doctor_dashboard'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

#  Patient Dashboard 
@app.route('/patient/dashboard')
def patient_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user_by_username(session['username'])
    return render_template('patients_dashboard.html', user=user)

#  Doctor Dashboard 
@app.route('/doctor/dashboard')
def doctor_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user_by_username(session['username'])
    return render_template('doctors_dashboard.html', user=user)


#  Logout 
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

#  Run app 
if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')  
    app.run(debug=True)