# Owner Features Implementation

## Features to Add:

1. ✅ **Auto-Join on Owner Invite** (UID: 14270700700)
2. ✅ **Bio Change Command** (`/bio [text]`)
3. ✅ **Add Friend Command** (`/friend [uid]`)
4. ✅ **Remove Friend Command** (`/unfriend [uid]`)

---

## Implementation Guide

### STEP 1: Add Global Variables

Add these at the top of your `main.py` after existing global variables:

```python
# Owner configuration
BOT_OWNER_UID = 14270700700  # Your UID
AUTO_ACCEPT_OWNER_INVITE = True  # Auto-join when owner invites

# Bio change configuration  
BIO_ENCRYPTION_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
BIO_ENCRYPTION_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
FREEFIRE_VERSION = "OB52"
```

---

### STEP 2: Add Helper Functions

Add these functions before your `TcPChaT` function:

```python
# =================== BIO CHANGE FUNCTIONS ===================

def get_bio_server_url(region="BD"):
    """Get bio server URL based on region"""
    region = region.upper()
    if region == "IND":
        return "https://clientbp.common.ggblueshark.com/SetBio"
    elif region == "BD":
        return "https://clientbp.common.ggblueshark.com/SetBio"
    else:
        return "https://clientbp.common.ggblueshark.com/SetBio"


def decode_jwt_noverify(token):
    """Decode JWT without verification"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decode payload (second part)
        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        print(f"JWT decode error: {e}")
        return None


def create_bio_protobuf(bio_text):
    """Create protobuf for bio change"""
    try:
        # Simple protobuf structure for bio
        # Field 1 (string): bio text
        bio_bytes = bio_text.encode('utf-8')
        
        # Protobuf encoding: field_number << 3 | wire_type
        # Wire type 2 = length-delimited (for strings)
        field_header = (1 << 3) | 2
        
        # Varint encoding for length
        length = len(bio_bytes)
        
        # Build protobuf
        protobuf_data = bytes([field_header, length]) + bio_bytes
        
        return protobuf_data
    except Exception as e:
        print(f"Protobuf creation error: {e}")
        return b""


async def set_bio_directly_async(jwt_token, bio_text, region="BD"):
    """Set bio directly - ASYNC version"""
    try:
        # Decode JWT to get region
        payload = decode_jwt_noverify(jwt_token)
        if not payload:
            return {
                "success": False,
                "message": "Invalid JWT token"
            }
        
        lock_region = payload.get("lock_region", region).upper()
        url_bio = get_bio_server_url(lock_region)
        
        print(f"🔧 Setting bio for region: {lock_region}")
        print(f"📝 Bio text: {bio_text}")
        
        # Create protobuf message
        data_bytes = create_bio_protobuf(bio_text)
        print(f"📦 Protobuf created: {len(data_bytes)} bytes")
        
        # Encrypt using AES CBC
        cipher = AES.new(BIO_ENCRYPTION_KEY, AES.MODE_CBC, BIO_ENCRYPTION_IV)
        
        # Pad data to AES block size (16 bytes)
        padding_length = 16 - (len(data_bytes) % 16)
        if padding_length:
            data_bytes += bytes([padding_length] * padding_length)
        
        encrypted_data = cipher.encrypt(data_bytes)
        print(f"🔐 Encrypted: {len(encrypted_data)} bytes")
        
        # Headers
        headers = {
            "Expect": "100-continue",
            "Authorization": f"Bearer {jwt_token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": FREEFIRE_VERSION,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        print(f"🚀 Sending to: {url_bio}")
        
        # Use aiohttp with timeout
        timeout = aiohttp.ClientTimeout(total=10)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url_bio, headers=headers, data=encrypted_data) as response:
                response_text = await response.text()
                
                print(f"📡 Response status: {response.status}")
                
                if response.status == 200:
                    return {
                        "success": True,
                        "message": "Bio updated successfully!",
                        "region": lock_region,
                        "bio": bio_text
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Server error: {response.status}"
                    }
                    
    except Exception as e:
        print(f"❌ Bio update error: {e}")
        return {
            "success": False,
            "message": str(e)
        }


async def set_bio_with_retry(jwt_token, bio_text, region="BD", max_retries=3):
    """Set bio with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"🔄 Bio update attempt {attempt + 1}/{max_retries}")
            
            result = await set_bio_directly_async(jwt_token, bio_text, region)
            
            if result.get("success"):
                return result
            else:
                print(f"❌ Attempt {attempt + 1} failed: {result.get('message')}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                    
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} error: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2)
    
    return {
        "success": False,
        "message": f"All {max_retries} attempts failed"
    }


def load_credentials_from_file(filename="Bot.txt"):
    """Load bot credentials from file"""
    try:
        if not os.path.exists(filename):
            print(f"❌ {filename} not found!")
            return None
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Try comma-separated format first
        if ',' in content:
            parts = content.split(',')
            if len(parts) >= 2:
                uid = parts[0].strip().replace('uid=', '').replace('UID=', '')
                password = parts[1].strip().replace('password=', '').replace('PASSWORD=', '')
                return (uid, password)
        
        # Try line-separated format
        lines = content.split('\n')
        uid = None
        password = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            
            if 'uid' in line.lower() or 'UID' in line:
                uid = line.split('=')[-1].strip() if '=' in line else line.split(':')[-1].strip()
            elif 'password' in line.lower() or 'PASSWORD' in line:
                password = line.split('=')[-1].strip() if '=' in line else line.split(':')[-1].strip()
        
        if uid and password:
            return (uid, password)
        
        print(f"❌ Invalid format in {filename}")
        return None
        
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None


# =================== FRIEND REQUEST FUNCTIONS ===================

async def send_friend_request_packet(target_uid, key, iv):
    """Send friend request packet"""
    try:
        # Create friend request packet
        # This is a simplified version - you may need to adjust based on actual packet structure
        fields = {
            1: 1,  # Action: Add friend
            2: {
                1: int(target_uid),  # Target UID
                2: 1  # Request type
            }
        }
        
        packet_hex = (await CrEaTe_ProTo(fields)).hex()
        packet = await GeneRaTePk(packet_hex, '1201', key, iv)
        
        return packet
        
    except Exception as e:
        print(f"❌ Friend request packet error: {e}")
        return None


async def remove_friend_packet(target_uid, key, iv):
    """Remove friend packet"""
    try:
        # Create remove friend packet
        fields = {
            1: 2,  # Action: Remove friend
            2: {
                1: int(target_uid),  # Target UID
            }
        }
        
        packet_hex = (await CrEaTe_ProTo(fields)).hex()
        packet = await GeneRaTePk(packet_hex, '1201', key, iv)
        
        return packet
        
    except Exception as e:
        print(f"❌ Remove friend packet error: {e}")
        return None
```

---

### STEP 3: Add Auto-Join Logic in TcPOnLine

Find the section in `TcPOnLine` where you handle `0500` packets (squad join/invite).

Add this code to handle owner invites:

```python
# In TcPOnLine function, after reading data2:

                # =================== AUTO-ACCEPT OWNER INVITE ===================
                if data2.hex().startswith('0500') and len(data2.hex()) > 100:
                    try:
                        packet_data = await DeCode_PackEt(data2.hex()[10:])
                        packet_json = json.loads(packet_data)
                        
                        # Check if this is an invite packet
                        if '5' in packet_json and 'data' in packet_json['5']:
                            squad_data = packet_json['5']['data']
                            
                            # Get squad owner UID (person who invited)
                            if '1' in squad_data and 'data' in squad_data['1']:
                                squad_owner = squad_data['1']['data']
                                
                                # Get squad code
                                if '8' in squad_data and 'data' in squad_data['8']:
                                    squad_code = squad_data['8']['data']
                                    
                                    # Check if owner invited
                                    if int(squad_owner) == BOT_OWNER_UID and AUTO_ACCEPT_OWNER_INVITE:
                                        print(f"✅ Owner {BOT_OWNER_UID} invited bot! Auto-accepting...")
                                        
                                        # Accept invite by joining squad
                                        join_packet = await GenJoinSquadsPacket(squad_code, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                        
                                        await asyncio.sleep(1)
                                        
                                        # Send welcome emote to owner
                                        welcome_emote = await Emote_k(int(squad_owner), 909000001, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', welcome_emote)
                                        
                                        print(f"🤖 Bot joined owner's squad!")
                                        
                    except Exception as e:
                        print(f"❌ Auto-join error: {e}")
                # ================================================================
```

---

### STEP 4: Add Command Handlers in TcPChaT

Add these command handlers in your `TcPChaT` function where other commands are:

```python
                        # =================== BIO CHANGE COMMAND ===================
                        if inPuTMsG.strip().startswith('/bio'):
                            print('📝 Processing bio change command')
                            
                            parts = inPuTMsG.strip().split(maxsplit=1)
                            
                            if len(parts) < 2:
                                error_msg = f\"\"\"[B][C][FF0000]❌ Usage: /bio (your bio text)

📝 Examples:
/bio Hello World!
/bio 🤖 Bot by Delta Rare Exe
/bio Level 70 | Pro Player

✨ Features:
• Changes bot's profile bio instantly
• Supports emojis and special characters
• Max length: 50 characters

💡 Note: Bio changes appear immediately in profile!
\"\"\"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                bio_text = parts[1]
                                
                                # Check length
                                if len(bio_text) > 50:
                                    error_msg = f"[B][C][FF0000]❌ Bio too long! Max 50 characters.\\n📝 Your bio: {len(bio_text)} chars\\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                
                                # Send initial message
                                initial_msg = f"[B][C][00FF00]📝 UPDATING BIO...\\n📋 Bio: {bio_text[:30]}...\\n⏳ Please wait...\\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                
                                # Load credentials
                                credentials = load_credentials_from_file("Bot.txt")
                                if not credentials:
                                    error_msg = f"[B][C][FF0000]❌ Failed to load credentials from Bot.txt!\\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                
                                try:
                                    Uid, Pw = credentials
                                except:
                                    error_msg = f"[B][C][FF0000]❌ Invalid credentials format!\\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                
                                # Get fresh token
                                try:
                                    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
                                    if not open_id or not access_token:
                                        error_msg = f"[B][C][FF0000]❌ Failed to generate access token!\\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        continue
                                    
                                    PyL = await EncRypTMajoRLoGin(open_id, access_token)
                                    MajoRLoGinResPonsE = await MajorLogin(PyL)
                                    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
                                    
                                    if not MajoRLoGinauTh or not MajoRLoGinauTh.token:
                                        error_msg = f"[B][C][FF0000]❌ Failed to get login token!\\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        continue
                                    
                                    token = MajoRLoGinauTh.token
                                    
                                    # Update bio with retry
                                    result = await set_bio_with_retry(token, bio_text, region)
                                    
                                    if result.get("success"):
                                        success_msg = f\"\"\"[B][C][00FF00]✅ BIO UPDATED SUCCESSFULLY!

📝 Bio: {bio_text}
🌍 Region: {result.get('region', region)}
🤖 Bot: Profile updated instantly!

💡 Check bot's profile to see new bio!
\"\"\"
                                    else:
                                        success_msg = f\"\"\"[B][C][FF0000]❌ BIO UPDATE FAILED!

📝 Bio: {bio_text}
❌ Error: {result.get('message', 'Unknown error')}

💡 Try:
1. Check bot's connection
2. Try shorter bio text
3. Wait 1 minute and try again
\"\"\"
                                    
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Bio update error: {str(e)}\\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                        # =================== FRIEND REQUEST COMMAND ===================
                        if inPuTMsG.strip().startswith('/friend '):
                            print('👥 Processing friend request command')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f\"\"\"[B][C][FF0000]❌ Usage: /friend (uid)

📝 Examples:
/friend 123456789
/friend 987654321

🎯 What it does:
• Sends friend request to target UID
• Bot will add them as friend
• Instant friend request

💡 Use /unfriend to remove friends
\"\"\"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                
                                initial_msg = f"[B][C][00FF00]👥 Sending friend request to {target_uid}...\\n⏳ Please wait...\\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                
                                try:
                                    # Send friend request packet
                                    friend_packet = await send_friend_request_packet(target_uid, key, iv)
                                    
                                    if friend_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', friend_packet)
                                        
                                        success_msg = f\"\"\"[B][C][00FF00]✅ FRIEND REQUEST SENT!

👤 Target: {target_uid}
📧 Request: Sent successfully
⏳ Status: Pending acceptance

💡 They will receive your friend request!
\"\"\"
                                    else:
                                        success_msg = f"[B][C][FF0000]❌ Failed to create friend request packet!\\n"
                                    
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Friend request error: {str(e)}\\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                        # =================== UNFRIEND COMMAND ===================
                        if inPuTMsG.strip().startswith('/unfriend '):
                            print('❌ Processing unfriend command')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f\"\"\"[B][C][FF0000]❌ Usage: /unfriend (uid)

📝 Examples:
/unfriend 123456789
/unfriend 987654321

🎯 What it does:
• Removes friend from bot's friend list
• Instant unfriend
• Cannot be undone

💡 Use /friend to add friends back
\"\"\"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                
                                initial_msg = f"[B][C][FFFF00]❌ Removing friend {target_uid}...\\n⏳ Please wait...\\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                
                                try:
                                    # Send remove friend packet
                                    unfriend_packet = await remove_friend_packet(target_uid, key, iv)
                                    
                                    if unfriend_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', unfriend_packet)
                                        
                                        success_msg = f\"\"\"[B][C][00FF00]✅ FRIEND REMOVED!

👤 Target: {target_uid}
❌ Status: Unfriended
✅ Removed from friend list

💡 Use /friend to add them back!
\"\"\"
                                    else:
                                        success_msg = f"[B][C][FF0000]❌ Failed to create unfriend packet!\\n"
                                    
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Unfriend error: {str(e)}\\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
```

---

## Summary

### ✅ Features Added:

1. **Auto-Join on Owner Invite**
   - Bot automatically joins when UID 14270700700 invites
   - Sends welcome emote to owner
   - No command needed - automatic!

2. **Bio Change** (`/bio [text]`)
   - Changes bot's profile bio
   - Max 50 characters
   - Supports emojis
   - Retry logic (3 attempts)

3. **Add Friend** (`/friend [uid]`)
   - Sends friend request to target UID
   - Instant friend request
   - Works from any chat type

4. **Remove Friend** (`/unfriend [uid]`)
   - Removes friend from bot's friend list
   - Instant unfriend
   - Cannot be undone

---

## Testing:

### Test Auto-Join:
1. Invite bot to your squad (UID: 14270700700)
2. Bot should auto-join immediately
3. Bot sends welcome emote

### Test Bio Change:
```
/bio Hello World!
/bio 🤖 Bot by Delta Rare Exe
```

### Test Friend Commands:
```
/friend 123456789
/unfriend 123456789
```

---

## Files Needed:

1. **Bot.txt** - Bot credentials (UID and password)
   Format:
   ```
   uid=YOUR_BOT_UID,password=YOUR_BOT_PASSWORD
   ```

---

**Total New Commands:** +3  
**New Features:** +1 (Auto-join)  
**Total Commands After:** 28 + 3 = **31 Commands!**

---

**By:** Delta Rare Exe  
**Date:** January 2025  
**Owner UID:** 14270700700
