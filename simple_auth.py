
import json
import os
import hashlib
import time
import secrets
import string
from datetime import datetime, timedelta

class SimpleAuth:
    def __init__(self, db_file='auth_users.json', sessions_file='auth_sessions.json', license_file='license_keys.json'):
        self.db_file = db_file
        self.sessions_file = sessions_file
        self.license_file = license_file
        self.users = self.load_users()
        self.sessions = self.load_sessions()
        self.license_keys = self.load_license_keys()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def load_sessions(self):
        """Load sessions from JSON file"""
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_sessions(self):
        """Save sessions to JSON file"""
        with open(self.sessions_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    def load_license_keys(self):
        """Load license keys from JSON file"""
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_license_keys(self):
        """Save license keys to JSON file"""
        with open(self.license_file, 'w') as f:
            json.dump(self.license_keys, f, indent=2)
    
    def generate_license_key(self, max_uses=1, expiry_days=None, note=''):
        """Generate a new license key"""
        key = 'DELTA-' + '-'.join([''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4)) for _ in range(4)])
        
        expiry_date = None
        if expiry_days:
            expiry_date = (datetime.now() + timedelta(days=expiry_days)).isoformat()
        
        self.license_keys[key] = {
            'created_at': datetime.now().isoformat(),
            'max_uses': max_uses,
            'used_count': 0,
            'used_by': [],
            'expiry_date': expiry_date,
            'status': 'active',
            'note': note
        }
        
        self.save_license_keys()
        return key
    
    def validate_license_key(self, key):
        """Check if license key is valid"""
        if key not in self.license_keys:
            return False, "Invalid license key!"
        
        license_data = self.license_keys[key]
        
        if license_data['status'] != 'active':
            return False, "License key is revoked!"
        
        if license_data['expiry_date']:
            expiry = datetime.fromisoformat(license_data['expiry_date'])
            if datetime.now() > expiry:
                return False, "License key has expired!"
        
        if license_data['used_count'] >= license_data['max_uses']:
            return False, "License key has reached maximum uses!"
        
        return True, "Valid"
    
    def use_license_key(self, key, username, ip_address):
        """Mark license key as used"""
        if key not in self.license_keys:
            return False
        
        self.license_keys[key]['used_count'] += 1
        self.license_keys[key]['used_by'].append({
            'username': username,
            'used_at': datetime.now().isoformat(),
            'ip_address': ip_address
        })
        
        self.save_license_keys()
        return True
    
    def revoke_license_key(self, key):
        """Revoke a license key"""
        if key not in self.license_keys:
            return False, "License key not found!"
        
        self.license_keys[key]['status'] = 'revoked'
        self.save_license_keys()
        return True, "License key revoked!"
    
    def delete_license_key(self, key):
        """Delete a license key"""
        if key not in self.license_keys:
            return False, "License key not found!"
        
        del self.license_keys[key]
        self.save_license_keys()
        return True, "License key deleted!"
    
    def get_all_license_keys(self):
        """Get all license keys with details"""
        keys_list = []
        for key, data in self.license_keys.items():
            keys_list.append({
                'key': key,
                'created_at': data['created_at'],
                'max_uses': data['max_uses'],
                'used_count': data['used_count'],
                'used_by': data['used_by'],
                'expiry_date': data['expiry_date'],
                'status': data['status'],
                'note': data.get('note', '')
            })
        return keys_list
    
    def create_session(self, username, hwid):
        """Create persistent session for user - never expires unless manually logged out"""
        session_id = hashlib.sha256(f"{username}:{hwid}:{time.time()}".encode()).hexdigest()
        self.sessions[session_id] = {
            'username': username,
            'hwid': hwid,
            'created_at': datetime.now().isoformat(),
            'never_expires': True
        }
        self.save_sessions()
        return session_id
    
    def validate_session(self, session_id):
        """Validate if session is still valid - sessions never expire unless manually deleted"""
        if session_id not in self.sessions:
            return False, None
        
        session = self.sessions[session_id]
        return True, session['username']
    
    def delete_session(self, session_id):
        """Delete a session (for logout)"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.save_sessions()
            return True
        return False
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password, hwid=None, license_key=None, ip_address=None):
        """Register new user with license key and tracking"""
        username = username.lower().strip()
        
        if username in self.users:
            return False, "Username already exists!"
        
        self.users[username] = {
            'password': self.hash_password(password),
            'device_id': hwid if hwid else None,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'login_count': 0,
            'license_key': license_key,
            'register_ip': ip_address,
            'login_history': []
        }
        
        self.save_users()
        return True, "Registration successful!"
    
    def login(self, username, password, hwid, ip_address=None):
        """Login user - auto-register device on first login, then lock to that device"""
        username = username.lower().strip()
        
        if username not in self.users:
            return False, "Invalid username or password!"
        
        user = self.users[username]
        
        if user['password'] != self.hash_password(password):
            return False, "Invalid username or password!"
        
        if user['device_id'] is None:
            user['device_id'] = hwid
            self.save_users()
            print(f"[SimpleAuth] Device ID auto-registered for user: {username}")
        elif user['device_id'] != hwid:
            return False, f"This account is registered on another device! You can only login from your registered device."
        
        user['last_login'] = datetime.now().isoformat()
        user['login_count'] = user.get('login_count', 0) + 1
        
        if 'login_history' not in user:
            user['login_history'] = []
        
        user['login_history'].append({
            'timestamp': datetime.now().isoformat(),
            'ip_address': ip_address,
            'device_id': hwid[:20] + '...' if hwid else None
        })
        
        if len(user['login_history']) > 50:
            user['login_history'] = user['login_history'][-50:]
        
        self.save_users()
        
        session_id = self.create_session(username, hwid)
        
        return True, {
            'username': username,
            'subscription': 'active',
            'login_count': user['login_count'],
            'device_id': hwid[:20] + '...',
            'session_id': session_id
        }
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        username = username.lower().strip()
        
        if username not in self.users:
            return False, "User not found!"
        
        user = self.users[username]
        
        if user['password'] != self.hash_password(old_password):
            return False, "Invalid old password!"
        
        user['password'] = self.hash_password(new_password)
        self.save_users()
        
        return True, "Password changed successfully!"
    
    def delete_user(self, username, password=None, admin_delete=False):
        """Delete user account"""
        username = username.lower().strip()
        
        if username not in self.users:
            return False, "User not found!"
        
        if not admin_delete:
            user = self.users[username]
            if user['password'] != self.hash_password(password):
                return False, "Invalid password!"
        
        del self.users[username]
        self.save_users()
        
        return True, "Account deleted successfully!"
    
    def get_user_info(self, username):
        """Get user information"""
        username = username.lower().strip()
        
        if username not in self.users:
            return None
        
        user = self.users[username]
        device_id = user.get('device_id')
        device_display = device_id[:20] + '...' if device_id else None
        
        return {
            'username': username,
            'created_at': user.get('created_at'),
            'last_login': user.get('last_login'),
            'login_count': user.get('login_count', 0),
            'device_id': device_display,
            'license_key': user.get('license_key'),
            'register_ip': user.get('register_ip'),
            'login_history': user.get('login_history', [])[-10:]
        }
    
    def get_all_users_detailed(self):
        """Get all users with detailed information for admin"""
        users_list = []
        for username, user_data in self.users.items():
            device_id = user_data.get('device_id')
            device_display = device_id[:20] + '...' if device_id else None
            
            users_list.append({
                'username': username,
                'created_at': user_data.get('created_at'),
                'last_login': user_data.get('last_login'),
                'login_count': user_data.get('login_count', 0),
                'device_id': device_display,
                'full_device_id': device_id,
                'license_key': user_data.get('license_key'),
                'register_ip': user_data.get('register_ip'),
                'login_history': user_data.get('login_history', [])[-10:]
            })
        
        return users_list
    
    def reset_user_device(self, username):
        """Reset user's device ID so they can register a new device"""
        username = username.lower().strip()
        
        if username not in self.users:
            return False, "User not found!"
        
        self.users[username]['device_id'] = None
        self.save_users()
        
        return True, f"Device reset for user {username}. They can now login from a new device."
