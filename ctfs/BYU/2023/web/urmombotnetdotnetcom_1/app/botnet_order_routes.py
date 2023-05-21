# imports
from __main__ import app, token_required, BOT_MONTHLY_PRICE, mysql
from flask import jsonify, request
from datetime import datetime


# GET botnet order information
@app.route('/api/botnet-orders/<int:order_id>', methods=['GET'])
@token_required
def get_botnet_order(session_data, order_id):
    # get user_id from order_id
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, number_of_bots, time_of_use, price, approved, time_stamp FROM Botnet_Order WHERE order_id=%s", (order_id,))
    response = cur.fetchone()
    cur.close()

    if not response:
        return jsonify({'message': 'You do not have permission to access this information'}), 403

    user_id = response[0]

    # ensure user is authorized to access the information
    if (not session_data['is_staff']) and (session_data['user_id'] != user_id):
        return jsonify({'message': 'You do not have permission to access this information'}), 403
    
    # return botnet order information
    response = {"number_of_bots": response[1], "order_id": order_id, "time_of_use": response[2], "price": response[3], "approved": response[4]==0, "time_stamp": response[5], "user_id": user_id}

    return jsonify(response), 200 


# POST create a botnet order
@app.route('/api/botnet-orders', methods=['POST'])
@token_required
def post_create_botnet_order(session_data):
    # ensure needed parameters are present
    if (request.json is None) or ('number_of_bots' not in request.json) or ('time_of_use' not in request.json):
        return jsonify({'message': 'Missing required parameters'}), 400
    
    number_of_bots = request.json['number_of_bots']
    time_of_use = request.json['time_of_use']
    timestamp = datetime.utcnow().isoformat()
    user_id = session_data["user_id"]

    # ensure parameters are integers
    if type(number_of_bots) is not int or type(time_of_use) is not int:
        return jsonify({'message': 'Invalid parameter data'}), 400
    
    # ensure number of bots is positive
    if number_of_bots <= 0:
        return jsonify({'message': 'Invalid number of bots'}), 400
    
    # ensure time of use is positive and less than or equal to 12 months
    if time_of_use <= 0 or time_of_use > 12:
        return jsonify({'message': 'Invalid time of use'}), 400
    
    # calculate price
    price = number_of_bots * time_of_use * BOT_MONTHLY_PRICE

    # insert botnet order into database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Botnet_Order (number_of_bots, time_of_use, price, time_stamp, user_id) VALUES (%s, %s, %s, %s, %s)", (number_of_bots, time_of_use, price, timestamp, user_id))
    mysql.connection.commit()
    order_id = cur.lastrowid
    cur.execute("SELECT * FROM Botnet_Order WHERE order_id=%s", (order_id,))
    response = cur.fetchone()
    cur.close()
    
    response = {"order_id": order_id, "timestamp": timestamp, "price": price}

    return jsonify(response), 200