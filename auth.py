import json
import bcrypt
import streamlit as st

class AuthSystem:
    def __init__(self, users_file='data/users.json'):
        self.users_file = users_file
        self.load_users()
    
    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def register_user(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = {
            'password': hashed_password.decode('utf-8'),
            'voted': False
        }
        self.save_users()
        return True, "Registration successful"
    
    def login_user(self, username, password):
        if username not in self.users:
            return False, "User not found"
        
        stored_hash = self.users[username]['password'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True, "Login successful"
        return False, "Invalid password"
    
    def has_voted(self, username):
        return self.users[username].get('voted', False)
    
    def mark_voted(self, username):
        self.users[username]['voted'] = True
        self.save_users()