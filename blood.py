from flask import Blueprint, request, jsonify
from db import get_db_connection

blood_bp = Blueprint('blood', __name__)

@blood_bp.route('/find_blood_banks', methods=['POST'])
def find_blood_banks():
    data = request.json
    blood_type = data.get('blood_type')

    if not blood_type:
        return jsonify({"error": "Blood type is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetching BloodBankID from BloodStock where quantity is greater than 0
        cursor.execute('SELECT BloodBankID FROM BloodStock WHERE Blood_Type = %s AND QuantityAvailable > 0', (blood_type,))
        blood_bank_ids = cursor.fetchall()
        
        if not blood_bank_ids:
            return jsonify({"message": "No blood banks found for the specified blood type."}), 404
        
        blood_bank_ids = [bank['BloodBankID'] for bank in blood_bank_ids]

        placeholders = ', '.join(['%s'] * len(blood_bank_ids))

        # Fetch blood banks with Latitude and Longitude
        cursor.execute(f'SELECT Blood_Bank_ID AS id, Name, Latitude, Longitude FROM BloodBank WHERE Blood_Bank_ID IN ({placeholders})', tuple(blood_bank_ids))
        blood_banks = cursor.fetchall()

        if not blood_banks:
            return jsonify({"message": "No blood banks found."}), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(blood_banks), 200
