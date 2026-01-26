from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from datetime import timedelta
import time
import json
import os
import re
from emote_shortcuts import BASE_EMOTES
from command_queue import command_queue
from simple_auth import SimpleAuth

def get_client_ip():
    """Get client IP address, respecting X-Forwarded-For header"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def normalize_emote_shortcut(shortcut):
    """
    Normalize emote shortcut by removing spaces, special characters, 
    and converting to lowercase to match BASE_EMOTES keys.
    Examples:
    - "boss energy" -> "bossenergy"
    - "p90 surfer" -> "p90surfer"
    - "fire style: fireball jutsu" -> "firestylefireballjutsu"
    - "can't stop laughing" -> "cantstoplaughing"
    """
    normalized = shortcut.lower()
    normalized = re.sub(r'[^a-z0-9]', '', normalized)
    return normalized

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'delta-rage-exe-secret-key-2024')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)  # 1 year session
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if using HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
CORS(app, supports_credentials=True)

# Admin Password (Set this as environment variable or secret)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'jihadAdmin')

# SimpleAuth Configuration
simple_auth = SimpleAuth(db_file='auth_users.json', sessions_file='auth_sessions.json', license_file='license_keys.json')

@app.route('/')
def index():
    # Check if user is authenticated
    if not session.get('authenticated'):
        return render_template('login.html')
    return render_template('index.html')

@app.route('/admin')
def admin_panel():
    # Check if user is admin
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return render_template('login.html')
    return render_template('admin.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/keyauth/login', methods=['POST'])
def keyauth_login():
    """SimpleAuth login endpoint"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        hwid = data.get('hwid', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password required!'
            })
        
        if not hwid:
            return jsonify({
                'success': False,
                'message': 'Device ID required!'
            })
        
        print(f"[SimpleAuth] Login attempt - User: {username}, HWID: {hwid[:20]}...")
        
        client_ip = get_client_ip()
        success, result = simple_auth.login(username, password, hwid, ip_address=client_ip)
        
        if success:
            session.permanent = True  # Make session permanent (persist after browser close)
            session.modified = True  # Force session save
            session['authenticated'] = True
            session['username'] = result['username']
            session['subscription'] = result['subscription']
            session['session_id'] = result.get('session_id')
            session['hwid'] = hwid
            
            print(f"[SimpleAuth] ✅ Login successful - User: {username}")
            
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'user': result
            })
        else:
            print(f"[SimpleAuth] ❌ Login failed - User: {username}, Reason: {result}")
            return jsonify({
                'success': False,
                'message': result
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/keyauth/register', methods=['POST'])
def keyauth_register():
    """SimpleAuth register endpoint - requires valid license key"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        hwid = data.get('hwid', '').strip()
        license_key = data.get('license_key', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password required!'
            })
        
        if not hwid:
            return jsonify({
                'success': False,
                'message': 'Device ID required!'
            })
        
        if not license_key:
            return jsonify({
                'success': False,
                'message': 'License key required! Please get a license key from admin.'
            })
        
        valid, msg = simple_auth.validate_license_key(license_key)
        if not valid:
            return jsonify({
                'success': False,
                'message': msg
            })
        
        client_ip = get_client_ip()
        print(f"[SimpleAuth] Register attempt - User: {username}, HWID: {hwid[:20]}..., IP: {client_ip}")
        
        success, result = simple_auth.register(username, password, hwid, license_key=license_key, ip_address=client_ip)
        
        if success:
            simple_auth.use_license_key(license_key, username, client_ip)
            print(f"[SimpleAuth] Registration successful - User: {username}")
            return jsonify({
                'success': True,
                'message': 'Registration successful! You can now login.'
            })
        else:
            print(f"[SimpleAuth] Registration failed - User: {username}, Reason: {result}")
            return jsonify({
                'success': False,
                'message': result
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })



@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin password login endpoint - bypass KeyAuth"""
    try:
        data = request.json
        password = data.get('password', '').strip()
        
        if not password:
            return jsonify({
                'success': False,
                'message': 'Password required!'
            })
        
        if password == ADMIN_PASSWORD:
            session.permanent = True  # Make session permanent
            session.modified = True  # Force session save
            session['authenticated'] = True
            session['username'] = 'Admin'
            session['subscription'] = 'admin'
            
            print(f"[Admin] Successful admin login")
            
            return jsonify({
                'success': True,
                'message': 'Admin login successful!',
                'user': {'username': 'Admin', 'subscription': 'admin'}
            })
        else:
            print(f"[Admin] Failed admin login attempt")
            return jsonify({
                'success': False,
                'message': 'Invalid admin password!'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/create_user', methods=['POST'])
def admin_create_user():
    """Admin endpoint to create new users (HWID auto-detected on first login)"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password required!'
            })
        
        client_ip = get_client_ip()
        success, result = simple_auth.register(username, password, hwid=None, license_key='ADMIN-CREATED', ip_address=client_ip)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'User {username} created successfully! Device will be registered on first login.'
            })
        else:
            return jsonify({
                'success': False,
                'message': result
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/list_users', methods=['GET'])
def admin_list_users():
    """Admin endpoint to list all users with detailed info"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        users_list = simple_auth.get_all_users_detailed()
        return jsonify({
            'success': True,
            'users': users_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/user_details/<username>', methods=['GET'])
def admin_user_details(username):
    """Admin endpoint to get detailed user info including login history"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        user_info = simple_auth.get_user_info(username)
        if user_info:
            return jsonify({
                'success': True,
                'user': user_info
            })
        else:
            return jsonify({
                'success': False,
                'message': 'User not found!'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/reset_device', methods=['POST'])
def admin_reset_device():
    """Admin endpoint to reset user's device ID"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        data = request.json
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({
                'success': False,
                'message': 'Username required!'
            })
        
        success, msg = simple_auth.reset_user_device(username)
        return jsonify({
            'success': success,
            'message': msg
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/license/create', methods=['POST'])
def admin_create_license():
    """Admin endpoint to create license keys"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        data = request.json
        max_uses = int(data.get('max_uses', 1))
        expiry_days = data.get('expiry_days')
        note = data.get('note', '').strip()
        
        if expiry_days:
            expiry_days = int(expiry_days)
        
        key = simple_auth.generate_license_key(max_uses=max_uses, expiry_days=expiry_days, note=note)
        
        return jsonify({
            'success': True,
            'message': 'License key created successfully!',
            'license_key': key
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/license/list', methods=['GET'])
def admin_list_licenses():
    """Admin endpoint to list all license keys"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        licenses = simple_auth.get_all_license_keys()
        return jsonify({
            'success': True,
            'licenses': licenses
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/license/revoke', methods=['POST'])
def admin_revoke_license():
    """Admin endpoint to revoke a license key"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        data = request.json
        key = data.get('key', '').strip()
        
        if not key:
            return jsonify({
                'success': False,
                'message': 'License key required!'
            })
        
        success, msg = simple_auth.revoke_license_key(key)
        return jsonify({
            'success': success,
            'message': msg
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/license/delete', methods=['POST'])
def admin_delete_license():
    """Admin endpoint to delete a license key"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        data = request.json
        key = data.get('key', '').strip()
        
        if not key:
            return jsonify({
                'success': False,
                'message': 'License key required!'
            })
        
        success, msg = simple_auth.delete_license_key(key)
        return jsonify({
            'success': success,
            'message': msg
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/admin/delete_user', methods=['POST'])
def admin_delete_user():
    """Admin endpoint to delete users"""
    if not session.get('authenticated') or session.get('subscription') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized! Admin access required.'
        })
    
    try:
        data = request.json
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({
                'success': False,
                'message': 'Username required!'
            })
        
        username = username.lower()
        
        if username not in simple_auth.users:
            return jsonify({
                'success': False,
                'message': 'User not found!'
            })
        
        del simple_auth.users[username]
        simple_auth.save_users()
        
        return jsonify({
            'success': True,
            'message': f'User {username} deleted successfully!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/keyauth/logout', methods=['POST'])
def keyauth_logout():
    """Logout endpoint - clears session and removes from database"""
    session_id = session.get('session_id')
    
    # Delete session from database
    if session_id:
        simple_auth.delete_session(session_id)
        print(f"[SimpleAuth] Session deleted: {session_id[:20]}...")
    
    # Clear Flask session
    session.clear()
    
    return jsonify({
        'success': True,
        'message': 'Logged out successfully!'
    })

@app.route('/keyauth/check_session', methods=['GET'])
def check_session():
    """Check if user is authenticated"""
    if session.get('authenticated'):
        return jsonify({
            'success': True,
            'authenticated': True,
            'username': session.get('username'),
            'subscription': session.get('subscription')
        })
    else:
        return jsonify({
            'success': True,
            'authenticated': False
        })

@app.route('/emotes.json', methods=['GET'])
def get_emotes():
    try:
        with open('emotes.json', 'r') as f:
            emotes = json.load(f)
        return jsonify(emotes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_emote', methods=['POST'])
def send_emote():
    try:
        data = request.json
        print(f"[WEB] Received data: {data}")
        
        teamcode = data.get('teamcode', '').strip()
        uids_raw = data.get('uids', '')
        auto_leave = data.get('auto_leave', True)
        
        # Handle both single emote and multiple emotes
        emotes_raw = data.get('emotes', [])  # New: array of emotes
        single_emote = data.get('emote', '')  # Old: single emote (backward compatibility)
        
        # Build emotes list
        emote_shortcuts = []
        if emotes_raw and isinstance(emotes_raw, list):
            emote_shortcuts = [e.strip() for e in emotes_raw if e.strip()]
        elif single_emote:
            emote_shortcuts = [single_emote.strip()]
        
        # Parse UIDs - can be comma-separated string or array
        uids = []
        if isinstance(uids_raw, str):
            uids = [uid.strip() for uid in uids_raw.split(',') if uid.strip()]
        elif isinstance(uids_raw, list):
            uids = [str(uid).strip() for uid in uids_raw if str(uid).strip()]
        
        print(f"[WEB] Parsed UIDs: {uids}")
        print(f"[WEB] Emotes to send: {emote_shortcuts}")
        
        if not teamcode:
            return jsonify({
                'success': False,
                'message': 'Team code is required!'
            })
        
        if not uids or len(uids) == 0:
            return jsonify({
                'success': False,
                'message': 'At least one UID is required!'
            })
        
        if not emote_shortcuts:
            return jsonify({
                'success': False,
                'message': 'At least one emote is required!'
            })
        
        if not teamcode.isdigit():
            return jsonify({
                'success': False,
                'message': 'Team code must be numeric!'
            })
        
        # Convert UIDs to integers
        uid_ints = []
        for uid in uids:
            try:
                uid_int = int(uid)
                uid_ints.append(uid_int)
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': f'Invalid UID: {uid} (must be numeric)'
                })
        
        # Validate and normalize all emotes
        valid_emotes = []
        for emote_shortcut in emote_shortcuts:
            normalized_shortcut = normalize_emote_shortcut(emote_shortcut)
            print(f"[WEB] Original emote: '{emote_shortcut}' -> Normalized: '{normalized_shortcut}'")
            
            if normalized_shortcut not in BASE_EMOTES:
                return jsonify({
                    'success': False,
                    'message': f'Invalid emote shortcut: {emote_shortcut}'
                })
            
            emote_id = BASE_EMOTES[normalized_shortcut]
            valid_emotes.append({
                'shortcut': normalized_shortcut,
                'id': emote_id
            })
        
        # Send all emotes at once
        command_data = {
            'source': 'web',
            'type': 'multi_emote',
            'teamcode': teamcode,
            'uids': uid_ints,
            'emotes': valid_emotes,
            'auto_leave': auto_leave
        }
        
        print(f"[WEB] Sending multi-emote command: {command_data}")
        command_id = command_queue.add_command(command_data)
        
        max_wait = 10  # Increased timeout for multiple emotes
        start_time = time.time()
        response = None
        
        while (time.time() - start_time) < max_wait:
            response = command_queue.get_response(command_id)
            if response:
                break
            time.sleep(0.1)
        
        if response:
            leave_msg = " and left squad" if auto_leave else " (staying in squad)"
            emote_names = ', '.join([e['shortcut'].upper() for e in valid_emotes[:3]])
            if len(valid_emotes) > 3:
                emote_names += f' +{len(valid_emotes) - 3} more'
            return jsonify({
                'success': True,
                'message': f'Successfully sent {len(valid_emotes)} emotes ({emote_names}) to {len(uid_ints)} player(s){leave_msg}!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Request timeout. Please ensure the bot is running (python main.py)'
            })
        
    except Exception as e:
        print(f"[WEB] Error in send_emote: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        })

@app.route('/leave_squad', methods=['POST'])
def leave_squad():
    try:
        command_data = {
            'source': 'web',
            'type': 'leave'
        }
        
        command_id = command_queue.add_command(command_data)
        
        max_wait = 5
        start_time = time.time()
        response = None
        
        while (time.time() - start_time) < max_wait:
            response = command_queue.get_response(command_id)
            if response:
                break
            time.sleep(0.3)
        
        if response:
            return jsonify({
                'success': True,
                'message': 'Successfully left squad!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Request timeout or bot offline'
            })
        
    except Exception as e:
        print(f"[WEB] Error in leave_squad: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/send_group_invite', methods=['POST'])
def send_group_invite():
    """Send group invite to a UID - creates 4, 5, or 6 player group"""
    try:
        data = request.json
        print(f"[WEB] Group Invite - Received data: {data}")
        
        uid_raw = data.get('uid', '')
        uid = str(uid_raw).strip() if uid_raw is not None else ''
        group_size = int(data.get('group_size', 4))
        
        if not uid:
            return jsonify({
                'success': False,
                'message': 'UID is required!'
            })
        
        try:
            uid_int = int(uid)
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'UID must be numeric!'
            })
        
        if group_size not in [4, 5, 6]:
            return jsonify({
                'success': False,
                'message': 'Group size must be 4, 5, or 6!'
            })
        
        command_data = {
            'source': 'web',
            'type': 'group_invite',
            'uid': uid_int,
            'group_size': group_size
        }
        
        print(f"[WEB] Sending group invite command: {command_data}")
        command_id = command_queue.add_command(command_data)
        
        max_wait = 10
        start_time = time.time()
        response = None
        
        while (time.time() - start_time) < max_wait:
            response = command_queue.get_response(command_id)
            if response:
                break
            time.sleep(0.5)
        
        if response:
            resp_data = response.get('response', response)
            if resp_data.get('status') == 'success':
                return jsonify({
                    'success': True,
                    'message': resp_data.get('message', f'Successfully sent {group_size}-player group invite to UID: {uid}!')
                })
            else:
                return jsonify({
                    'success': False,
                    'message': resp_data.get('message', 'Failed to send group invite')
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Request timeout. Please ensure the bot is running (python main.py)'
            })
        
    except Exception as e:
        print(f"[WEB] Error in send_group_invite: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        })

@app.route('/bot_status', methods=['GET'])
def bot_status():
    try:
        command_data = {
            'source': 'web',
            'type': 'status'
        }
        
        command_id = command_queue.add_command(command_data)
        
        max_wait = 3
        start_time = time.time()
        response = None
        
        while (time.time() - start_time) < max_wait:
            response = command_queue.get_response(command_id)
            if response:
                break
            time.sleep(0.2)
        
        if response:
            return jsonify({
                'success': True,
                'online': True,
                'message': 'Bot is online and ready'
            })
        else:
            return jsonify({
                'success': False,
                'online': False,
                'message': 'Bot is offline'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'online': False,
            'message': f'Error: {str(e)}'
        })

if __name__ == '__main__':
    print("[WEB] ==========================================")
    print("[WEB] Delta Rage Exe - Web Control Panel")
    print("[WEB] Starting web server on http://0.0.0.0:5000")
    print("[WEB] Make sure main bot is running: python main.py")
    print("[WEB] ==========================================")
    app.run(host='0.0.0.0', port=5000, debug=False)
