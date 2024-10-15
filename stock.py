from flask import Blueprint, request, jsonify
from db import get_db_connection

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/bloodstock', methods=['GET'])
def get_blood_stock():
    blood_bank_id = request.args.get('blood_bank_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT Blood_Type, QuantityAvailable FROM bloodstock WHERE BloodBankID = %s', (blood_bank_id,))
        blood_stock = cursor.fetchall()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

    conn.close()
    return jsonify(blood_stock), 200
