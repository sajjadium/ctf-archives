# imports
from __main__ import app, token_required, BOT_PRICE_LINUX_WINDOWS, BOT_PRICE_MACOS, mysql
from flask import jsonify, request
import ipaddress


# GET user information
@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(session_data, user_id):
    # ensure user is authorized to access the information
    if (not session_data['is_staff']) and (session_data['user_id'] != user_id):
        return jsonify({'message': 'You do not have permission to access this information'}), 403
    
    # get user information
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, email, username, blocked, bitcoin_wallet FROM User WHERE user_id=%s", (user_id,))
    user_data = cur.fetchone()
    cur.close()

    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({"user_id": user_data[0], "email": user_data[1], "username": user_data[2], "blocked": bool(user_data[3]), "bitcoin_wallet": user_data[4]}), 200


# GET affiliate information
@app.route('/api/affiliates/<int:affiliate_id>', methods=['GET'])
@token_required
def get_affiliate(session_data, affiliate_id):
    # get user_id from affiliate_id
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, total_bots_added, money_received FROM Affiliates WHERE affiliate_id=%s", (affiliate_id,))
    response = cur.fetchone()
    cur.close()

    if (not response) and session_data['is_staff']:
        return jsonify({'message': 'Affiliate not found'}), 404
    
    if (not response) or (session_data['user_id'] != response[0]):
        return jsonify({'message': 'You do not have permission to access this information'}), 403

    affiliate_data = {"affiliate_id": affiliate_id, "user_id": response[0], "total_bots_added": response[1], "money_received": response[2]}

    return jsonify(affiliate_data), 200
    

# POST add a bot as an affiliate
@app.route('/api/bots', methods=['POST'])
@token_required
def post_add_bot(session_data):
    # ensure needed parameters are present
    if (request.json is None) or ('os' not in request.json) or ('ip_address' not in request.json):
        return jsonify({'message': 'Missing required parameters'}), 400
    
    os = request.json['os']
    ip_address = request.json['ip_address']
    user_id = session_data["user_id"]

    # ensure parameters are strings
    if type(os) is not str or type(ip_address) is not str:
        return jsonify({'message': 'Invalid parameter data'}), 400
    
    # validate os
    if os not in ['Windows', 'Linux', 'MacOS']:
        return jsonify({'message': 'Invalid OS'}), 400
    
    # validate ip_address
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        return jsonify({'message': 'Invalid IP address'}), 400
    
    # see if IP address is already added
    cur = mysql.connection.cursor()
    cur.execute("SELECT bot_id FROM Bots WHERE ip_address=%s", (ip_address,))
    response = cur.fetchone()
    if response:
        return jsonify({'message': 'IP address already added'}), 400

    
    # select affiliate id from user id
    cur.execute("SELECT affiliate_id, Total_bots_added, money_received FROM Affiliates WHERE user_id=%s", (user_id,))
    result = cur.fetchone()
    affiliate_id = result[0]
    old_total_bots_added = result[1]
    old_money_received = result[2]
    # byuctf{fakeflag5}
    # add bot to database
    cur.execute("INSERT INTO Bots (os, ip_address) VALUES (%s, %s)", (os, ip_address))
    mysql.connection.commit()
    bot_id = cur.lastrowid
    cur.execute("INSERT INTO Adds VALUES (%s, %s)", (bot_id, affiliate_id))

    # update affiliate information
    cur.execute("UPDATE Affiliates SET total_bots_added=%s, money_received=%s WHERE affiliate_id=%s", (old_total_bots_added+1, old_money_received+(BOT_PRICE_LINUX_WINDOWS if os!='MacOS' else BOT_PRICE_MACOS), affiliate_id))
    mysql.connection.commit()
    cur.close()

    response = {"bot_id": bot_id, "payment": BOT_PRICE_LINUX_WINDOWS if os!='MacOS' else BOT_PRICE_MACOS}
    
    return jsonify(response), 200


# POST send a command to a botnet
@app.route('/api/bots/command', methods=['POST'])
@token_required
def post_send_command(session_data):
    # ensure needed parameters are present
    if (request.json is None) or ('bot_id' not in request.json) or ('command' not in request.json):
        return jsonify({'message': 'Missing required parameters'}), 400
    
    bot_id = request.json['bot_id']
    command = request.json['command']

    # ensure parameters are correct
    if type(bot_id) is not int or type(command) is not str:
        return jsonify({'message': 'Invalid parameter data'}), 400
    
    # ensure user is authorized to access the information because they are the owner of the bot
    user_id = session_data["user_id"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT bot_id FROM User_Bots WHERE User_ID=%s AND bot_id=%s", (user_id, bot_id))
    response = cur.fetchone()
    cur.close()

    authorized = False
    if response and response[0] == bot_id:
        authorized = True

    if not authorized:
        return jsonify({'message': 'You do not have permission to access this information'}), 403
    
    # send command to bot
    "lol"
    response = {"output": "root"}

    return jsonify(response), 200