from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
import bcrypt
from db import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone_num = data.get('phone_num')
    location_latitude = data.get('LocationLatitude')
    longitude = data.get('Longitude')
    user_type = data.get('User_Type')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (Name, Email, Phone_num, LocationLatitude, Longitude, User_Type, Password)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                   (name, email, phone_num, location_latitude, longitude, user_type, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE Email = %s', (email,))
    user = cursor.fetchone()

    if user:
        stored_password = user['Password']
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            session['user_id'] = user['User_Id']  # Store user ID in session
            session['user_name'] = user['Name']  # Store user name in session
            return jsonify({
                'message': 'Login successful',
                'user_name': user['Name'],  # Include user name in the response
                'redirect': url_for('auth.details')
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/details', methods=['GET'])
def details():
    user_name = session.get('user_name')  # Get user name from session
    user_id = session.get('user_id')
    return render_template('details.html', user_name=user_name)  # Pass user name to template