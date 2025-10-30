import json
import hashlib
import streamlit as st
import os

class AuthSystem:
    def __init__(self, users_file=None):
        if users_file is None:
            users_file = os.path.join(os.path.dirname(__file__), 'data', 'users.json')
        self.users_file = users_file
        self.load_users()
    
    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
            self.save_users()
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def _hash_password(self, password):
        """Simple password hashing using SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def register_user(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        
        hashed_password = self._hash_password(password)
        self.users[username] = {
            'password': hashed_password,
            'voted': False
        }
        self.save_users()
        return True, "Registration successful"
    
    def login_user(self, username, password):
        if username not in self.users:
            return False, "User not found"
        
        hashed_password = self._hash_password(password)
        if self.users[username]['password'] == hashed_password:
            return True, "Login successful"
        return False, "Invalid password"
    
    def has_voted(self, username):
        return self.users.get(username, {}).get('voted', False)
    
    def mark_voted(self, username):
        if username in self.users:
            self.users[username]['voted'] = True
            self.save_users()
