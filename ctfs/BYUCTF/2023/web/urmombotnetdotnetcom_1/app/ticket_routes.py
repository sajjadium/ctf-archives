# imports
from __main__ import app, token_required, mysql
from flask import jsonify, request
from datetime import datetime


# GET ticket information
@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
@token_required
def get_ticket(session_data, ticket_id):
    # get user_id from ticket_id
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, description, messages FROM Support_Tickets WHERE ticket_id=%s", (ticket_id,))
    response = cur.fetchone()
    cur.close()

    if not response and session_data['is_staff']:
        return jsonify({'message': 'Ticket not found'}), 404
    
    if not response or session_data['user_id'] != response[0]:
        return jsonify({'message': 'You do not have permission to access this information'}), 403

    response = {"ticket_id": ticket_id, "user_id": response[0], "description": response[1], "messages":response[2]}
    
    return jsonify(response), 200


# POST create a ticket
@app.route('/api/tickets', methods=['POST'])
@token_required
def post_create_ticket(session_data):
    # ensure needed parameters are present
    if (request.json is None) or ('description' not in request.json):
        return jsonify({'message': 'Missing required parameters'}), 400
    
    user_id = session_data["user_id"]
    description = request.json['description']
    timestamp = datetime.utcnow().isoformat()

    # ensure parameters are integers
    if type(description) is not str:
        return jsonify({'message': 'Invalid parameter data'}), 400
    # byuctf{fakeflag2}
    # insert ticket into database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Support_Tickets (description, messages, time_stamp, user_id) VALUES (%s, %s, %s, %s)", (description, "", timestamp, user_id))
    mysql.connection.commit()
    ticket_id = cur.lastrowid
    cur.close()

    response = {"ticket_id": ticket_id, "description": description, "time_stamp": timestamp}

    return jsonify(response), 200


# POST add a message to a ticket
@app.route('/api/tickets/<int:ticket_id>', methods=['POST'])
@token_required
def post_add_message(session_data, ticket_id):
    # get user_id from ticket_id
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, message FROM support_tickets WHERE ticket_id=%s", (ticket_id,))
    response = cur.fetchone()
    cur.close()

    if not response and session_data['is_staff']:
        return jsonify({'message': 'Ticket not found'}), 404
    
    if not response or session_data['user_id'] != response[0]:
        return jsonify({'message': 'You do not have permission to access this information'}), 403

    # ensure needed parameters are present
    if (request.json is None) or ('message' not in request.json):
        return jsonify({'message': 'Missing required parameters'}), 400
    
    message = request.json['message']

    # ensure parameters are integers
    if type(message) is not str:
        return jsonify({'message': 'Invalid parameter data'}), 400
    # byuctf{fakeflag3}
    # insert message into database
    cur = mysql.connection.cursor()
    new_message = response[1] + "\n" + message
    cur.execute("UPDATE Support_Tickets SET message=%s WHERE ticket_id=%s", (new_message, ticket_id))
    mysql.connection.commit()
    cur.close()
    
    response = {"ticket_id": ticket_id, "message": message}

    return jsonify(response), 200