from flask import Blueprint, request, jsonify, session, render_template
from db import get_db_connection
from datetime import datetime

reservation_bp = Blueprint('reservations', __name__)

@reservation_bp.route('/create', methods=['POST'])
def create_reservation():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get the current time for Reservation_start_time
    current_time = datetime.now()
    
    # Extract the user_id from the session
    user_id = session.get('user_id')  # Assuming user_id is stored in the session during login
    if not user_id:
        return jsonify({"error": "User is not logged in"}), 401  # Return an error if the user is not logged in
    
    # Extract other required fields from the request
    blood_bank_id = data.get('blood_bank_id')
    blood_type = data.get('blood_type')
    quantity_reserved = data.get('Quantity_Reserved')
    eta = data.get('ReservationsExpiryTime')
    status = data.get('status')
    
    # Validate ETA
    if not eta:
        return jsonify({"error": "ETA is required"}), 400

    # Subtract Quantity_Reserved from QuantityAvailable in BloodStock
    cursor.execute('''UPDATE BloodStock SET QuantityAvailable = QuantityAvailable - %s 
                      WHERE BloodBankID = %s AND Blood_Type = %s AND QuantityAvailable >= %s
                   ''', (quantity_reserved, blood_bank_id, blood_type, quantity_reserved))

    if cursor.rowcount == 0:
        conn.rollback()  # Rollback if quantity is not sufficient
        conn.close()
        return jsonify({"error": "Insufficient quantity available"}), 400

    # Insert into Reservations table
    cursor.execute('''INSERT INTO Reservations (User_ID, Blood_Bank_ID, Blood_Type, Quantity_Reserved, 
                                                  Reservations_start_time, ReservationsExpiryTime, 
                                                  StatusReservedCompletedCancelled) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ''', (user_id, blood_bank_id, blood_type, quantity_reserved, 
                         current_time, eta, status))

    conn.commit()
    conn.close()

    return jsonify({"message": "Reservation created successfully"}), 201

@reservation_bp.route('/history', methods=['GET'])
def reservation_history():
    # Extract the user_id from the session
    user_id = session.get('user_id')  # Assuming user_id is stored in the session during login
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON-like structure

    try:
        # Query to fetch all reservations for the given user_id
        cursor.execute('''SELECT Blood_Bank_ID, Blood_Type, Quantity_Reserved, Reservations_start_time, StatusReservedCompletedCancelled FROM Reservations WHERE User_ID = %s ORDER BY Reservations_start_time DESC''', (user_id,))
        reservations = cursor.fetchall()

        # Check if there are reservations and render accordingly
        if not reservations:
            return render_template('history.html', reservations=[], message="No reservations found for this user")

        return render_template('history.html', reservations=reservations)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        conn.close()
