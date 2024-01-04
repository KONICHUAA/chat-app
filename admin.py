import requests
import  time
# URL of your Flask application's /add route
url = 'http://127.0.0.1:5000/add'
def add():
    # Room data to be sent in the request body
    roomName = input("Enter your Room name: ")
    room_data = {
        "roomName": roomName
    }

    # Make a POST request
    response = requests.post(url, json=room_data)

    # Print the response
    print(response.json())
def delete():

    # URL of your Flask application's /delete route
    url = 'http://127.0.0.1:5000/delete/'

    # Room key to be used in the URL
    room_key = input("Enter the room key to delete: ")

    # Make a DELETE request
    response = requests.delete(url + room_key)

    # Print the response
    print(response.json())


def get_messages():
    url = 'http://127.0.0.1:5000/get_messages/'

    # Room key to be used in the URL
    room_key = str(input("Enter the room key to get messages: "))

    last_index = 0  # Initialize the last processed message index

    while True:
        # Make a GET request
        response = requests.get(url + room_key)

        try:
            # Try to parse the response as JSON
            json_content = response.json()

            # If the JSON content is a list of strings, iterate through each string
            if isinstance(json_content, list) and all(isinstance(item, str) for item in json_content):
                for index, message in enumerate(json_content, start=1):
                    if index > last_index:
                        print(f"New Message {index}: {message}")
                        last_index = index
            else:
                print("Response JSON:", json_content)
        except requests.exceptions.JSONDecodeError:
            # If JSON decoding fails, print the raw text content
            print("Response Text:", response.text)

        time.sleep(0.2)
import requests

def send_message():
    # URL of your Flask application's /add_message route
    url = 'http://127.0.0.1:5000/add_message/'

    # Room key to be used in the URL
    room_key = input("Enter the room key to add a message: ")

    while True:
        # Message data to be sent in the request body
        message_content = input("Enter the message content: ")
        message_data = {
            "messageContent": message_content
        }

        # Make a POST request
        response = requests.post(url + room_key, json=message_data)

        try:
            # Try to parse the response as JSON
            json_content = response.json()
            print("Response JSON:", json_content)
        except requests.exceptions.JSONDecodeError:
            # If JSON decoding fails, print the raw text content
            print("Response Text:", response.text)
