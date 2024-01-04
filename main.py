import requests
from flask import Flask, jsonify,request
import json
import random
import string

app = Flask(__name__)
def generate_random_code():
    return ''.join(random.choices(string.digits, k=4))
# Load data from the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

@app.route('/rooms')
def get_json_data():
    return jsonify(data)

@app.route('/add', methods=['POST'])
def add_room():
    # Parse JSON data from the request body
    request_data = request.get_json()

    # Extract room name from the request data
    room_name = request_data.get('roomName')

    if not room_name:
        return jsonify({"error": "Room name is required"}), 400

    # Generate a random 4-digit code
    room_key = generate_random_code()

    # Create a new room with an empty list of messages
    new_room = {
        "Name": room_name,
        "messages": []
    }

    # Add the new room to the existing data using the generated room key
    data["rooms"][room_key] = new_room

    # Write the updated data back to the JSON file (assuming 'data.json')
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print(f"Done making Room {room_name} by Key {room_key}")

    return jsonify({"message": f"Key = {room_key}", "data": new_room}), 200


@app.route('/delete/<room_key>', methods=['DELETE'])
def delete_room(room_key):
    try:
        # Attempt to delete the room with the specified key
        deleted_room = data["rooms"].pop(room_key)

        # Write the updated data back to the JSON file
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)

        return jsonify({"message": f"Room with key {room_key} deleted successfully", "data": deleted_room}), 200
    except KeyError:
        return jsonify({"error": f"Room with key {room_key} not found"}), 404
@app.route('/get_messages/<room_key>', methods=['GET'])
def get_messages(room_key):
    try:
        # Retrieve messages for the specified room key
        room_messages = data["rooms"][room_key]["messages"]
        return room_messages
    except KeyError:
        return jsonify({"error": f"Room not found"}), 404
@app.route('/add_message/<room_key>', methods=['POST'])
def add_message(room_key):
    try:
        if not data["rooms"][room_key]:
            print("Key is wrong")
        print(f"Received POST request for room key: {room_key}")

        # Parse JSON data from the request body
        request_data = request.get_json()

        # Extract message content from the request data
        message_content = request_data.get('messageContent')

        if not message_content:
            return jsonify({"error": "Message content is required"}), 400

        # Add the new message to the specified room key
        data["rooms"][room_key]["messages"].append(message_content)

        # Write the updated data back to the JSON file
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)

        return jsonify({"message": "Message added successfully", "data": {"roomKey": room_key, "messageContent": message_content}}), 200
    except KeyError:
        print(f"Room with key {room_key} not found")
        return jsonify({"error": f"Room with key {room_key} not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
