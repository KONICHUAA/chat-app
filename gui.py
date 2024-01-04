import tkinter as tk
from tkinter import ttk, messagebox
import requests

class ChatAppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat Application")

        # Create variables to store user input
        self.room_key_var = tk.StringVar()
        self.room_name_var = tk.StringVar()
        self.message_var = tk.StringVar()

        # Store a reference to the chat text widget using an instance variable
        self.chat_text_widget = None

        self.create_main_screen()

    def create_main_screen(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack()

        # Room Key Entry
        label_key = tk.Label(main_frame, text="Room Key:")
        entry_key = tk.Entry(main_frame, textvariable=self.room_key_var)

        # Room Name Entry
        label_name = tk.Label(main_frame, text="Room Name:")
        entry_name = tk.Entry(main_frame, textvariable=self.room_name_var)

        # Make and Join Buttons
        make_button = tk.Button(main_frame, text="Make", command=self.make_room)
        join_button = tk.Button(main_frame, text="Join", command=self.join_room)

        show_button = ttk.Button(main_frame, text="Show Active Rooms", command=self.show_active_rooms)
        show_button.grid(row=3, column=1, pady=10, sticky=(tk.W, tk.E))

        # Additional buttons
        delete_button = ttk.Button(main_frame, text="Delete Room", command=self.delete_room)
        delete_button.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))

        label_key.grid(row=0, column=0, sticky="w")
        entry_key.grid(row=0, column=1, padx=10, pady=5)
        label_name.grid(row=1, column=0, sticky="w")
        entry_name.grid(row=1, column=1, padx=10, pady=5)
        make_button.grid(row=2, column=0, pady=10)
        join_button.grid(row=2, column=1, pady=10)

    def create_chat_screen(self):
        chat_frame = tk.Frame(self.root, padx=20, pady=20)
        chat_frame.pack()

        # Text widget for displaying messages
        chat_text = tk.Text(chat_frame, state=tk.DISABLED, height=10, width=50)
        chat_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Entry for typing messages
        entry_message = tk.Entry(chat_frame, textvariable=self.message_var, width=40)
        entry_message.grid(row=1, column=0, padx=10, pady=5)

        # Button to send messages
        send_button = tk.Button(chat_frame, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, pady=5)

        # Store the reference to the chat text widget using an instance variable
        self.chat_text_widget = chat_text

        # Bind the Return key event to the send_message method
        entry_message.bind("<Return>", lambda event: self.send_message())

    def make_room(self):
        room_name = self.room_name_var.get()
        if not room_name:
            messagebox.showerror("Error", "Room name is required")
            return

        url = 'http://127.0.0.1:5000/add'
        room_data = {"roomName": room_name}
        response = requests.post(url, json=room_data)
        messagebox.showinfo("Room Created", response.json())

    def join_room(self):
        room_key = self.room_key_var.get()
        if not room_key:
            messagebox.showerror("Error", "Room key is required")
            return

        # Destroy the current chat screen if it exists
        if self.chat_text_widget:
            self.chat_text_widget.destroy()

        self.create_chat_screen()

        # Clear the message entry and chat text widget
        self.message_var.set("")  # Clear the entry
        self.chat_text_widget.configure(state=tk.NORMAL)
        self.chat_text_widget.delete(1.0, tk.END)  # Clear existing messages
        self.chat_text_widget.configure(state=tk.DISABLED)

        self.fetch_and_display_messages_periodic(room_key)

    def send_message(self):
        room_key = self.room_key_var.get()
        message_content = self.message_var.get()

        if not room_key or not message_content:
            messagebox.showerror("Error", "Room key and message content are required")
            return

        url = 'http://127.0.0.1:5000/add_message/'
        message_data = {"messageContent": message_content}
        response = requests.post(url + room_key, json=message_data)
        self.message_var.set("")  # Clear the entry after sending the message
        self.fetch_and_display_messages(room_key)

    def fetch_and_display_messages(self, room_key):
        url = f'http://127.0.0.1:5000/get_messages/{room_key}'
        response = requests.get(url)

        try:
            json_content = response.json()
            if isinstance(json_content, list) and all(isinstance(item, str) for item in json_content):
                self.chat_text_widget.configure(state=tk.NORMAL)
                self.chat_text_widget.delete(1.0, tk.END)
                for message in json_content:
                    self.chat_text_widget.insert(tk.END, f"{message}\n")
                self.chat_text_widget.configure(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", f"Invalid response format: {json_content}")
        except requests.exceptions.JSONDecodeError:
            messagebox.showerror("Error", f"Invalid response format: {response.text}")

        # Schedule the fetch_and_display_messages to run again after 100 milliseconds
        self.root.after(100, self.fetch_and_display_messages_periodic, room_key)

    def fetch_and_display_messages_periodic(self, room_key):
        # Fetch and display messages periodically
        self.fetch_and_display_messages(room_key)

    def run(self):
        self.root.mainloop()

    def show_active_rooms(self):
        url = 'http://127.0.0.1:5000/rooms'
        response = requests.get(url)
        active_rooms = response.json().get("rooms", [])

        if not active_rooms:
            messagebox.showinfo("Active Rooms", "No active rooms.")
        else:
            messagebox.showinfo("Active Rooms", "\n".join(active_rooms))

    def delete_room(self):
        room_key = self.room_key_var.get()
        if not room_key:
            messagebox.showerror("Error", "Room key is required")
            return

        url = 'http://127.0.0.1:5000/delete/'
        response = requests.delete(url + room_key)
        messagebox.showinfo("Room Deleted", response.json())

if __name__ == "__main__":
    app = ChatAppGUI()
    app.run()
