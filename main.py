import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *
from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2, kyro_title_pb2, room_join_pb2, spam_request_pb2
from cfonts import render, say
import asyncio
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from command_queue import command_queue
from emote_shortcuts import BASE_EMOTES, DEFAULT_PLAYER_UIDS, VARIANT_UIDS, SHORTCUT_EMOTES
from connection_pool import connection_pool
from commands import (
    BotContext,
    EMOTE_MAP,
    GENERAL_EMOTES_MAP,
    r_command_operation,
    flash_ghost_emote,
    lag_team_loop,
    general_emote_spam,
    random_evo_emote_spam_sender,
    dance_group_emotes,
    process_web_command,
    encrypt_packet,
    nmnmmmmn,
    ghost_join_packet,
    bundle_command_operation,
)

#EMOTES BY PARAHEX X CODEX
# FIXED BY Delta Rare Exe ❄️

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# VariabLes dyli
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
spam_request_running = False
spam_request_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
lag_running = False
lag_task = None

# NEW: Store current group members
current_group_members = []
bot_uid = None

# =================== OWNER FEATURES (NEW) ===================
BOT_OWNER_UID = 14270700700  # Your owner UID
AUTO_ACCEPT_OWNER_INVITE = True  # Auto-join when owner invites

# Freeze command variables
freeze_running = False
freeze_task = None
FREEZE_EMOTES = [909052010, 909052010, 909052010]  # Ice emotes
FREEZE_DURATION = 10  # seconds

# Bio change configuration
BIO_ENCRYPTION_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
BIO_ENCRYPTION_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
FREEFIRE_VERSION = "OB52"

# =================== WHITELIST SYSTEM (NEW FROM BBUND) ===================
WHITELISTED_UIDS = set()  # Set of whitelisted UIDs
WHITELIST_ONLY = False  # If True, only whitelisted users can use bot
WHITELIST_FILE = "whitelist.json"  # File to store whitelist
WHITELIST_DATA = {}  # Dict to store UID -> {note, added_at}

# =================== ROOM SYSTEM (NEW FROM BBUND) ===================
current_room_id = None
room_info_cache = {}

# =================== ADVANCED SPAM (NEW FROM BBUND) ===================
reject_spam_running = False
reject_spam_task = None
evo_cycle_running = False
evo_cycle_task = None
msg_spam_running = False
msg_spam_task = None

# =================== MATCH FEATURES (NEW FROM BBUND) ===================
START_SPAM_DURATION = 18  # Spam for 18 seconds on match start
WAIT_AFTER_MATCH_SECONDS = 20  # Wait 20 seconds after match
START_SPAM_DELAY = 0.2  # Delay between spam emotes
match_spam_running = False
match_spam_task = None

# =================== AUTO BUNDLE SYSTEM (NEW) ===================
AUTO_BUNDLE_ENABLED = True  # Enable/disable auto bundle
AUTO_BUNDLE_MODE = "random"  # "random" or "fixed"
AUTO_BUNDLE_ID = "914047001"  # Default: Naruto bundle

# All available bundles
AVAILABLE_BUNDLES = {
    "rampage": "914000002",
    "cannibal": "914000003",
    "devil": "914038001",
    "scorpio": "914039001",
    "frostfire": "914042001",
    "paradox": "914044001",
    "naruto": "914047001",
    "aurora": "914047002",
    "midnight": "914048001",
    "itachi": "914050001",
    "dreamspace": "914051001"
}

# =================== AUTO RANK/BANNER/AVATAR SYSTEM (NEW) ===================
AUTO_RANK_ENABLED = True  # Enable/disable auto rank
AUTO_RANK_MODE = "random"  # "random" or "fixed"
AUTO_RANK_ID = 21  # Default rank

AUTO_BANNER_ENABLED = True  # Enable/disable auto banner
AUTO_BANNER_MODE = "random"  # "random" or "fixed"
AUTO_BANNER_ID = 902000306  # Default banner

AUTO_AVATAR_ENABLED = True  # Enable/disable auto avatar
AUTO_AVATAR_MODE = "random"  # "random" or "fixed"
AUTO_AVATAR_ID = 909034009  # Default avatar

# Available ranks (1-30)
AVAILABLE_RANKS = list(range(1, 31))

# Available banners
AVAILABLE_BANNERS = [
    902000306, 902000307, 902000308, 902000309, 902000310,
    902000311, 902000312, 902000313, 902000314, 902000315,
    902039016, 902047010, 902047011, 902049015, 902049020,
    902050001, 902050002, 902050003, 902050004, 902050006
]

# Available avatars
AVAILABLE_AVATARS = [
    909034009, 909000063, 909000068, 909000075, 909040010,
    909000081, 909039011, 909000085, 909000090, 909000098,
    909035007, 909042008, 909041005, 909033001, 909038010,
    909038012, 909045001, 909049010, 909051003, 909051012
]
#------------------------------------------#


#Clan-info-by-clan-id
def Get_clan_info(clan_id):
    try:
        url = f"https://get-clan-info.vercel.app/get_clan_info?clan_id={clan_id}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            msg = f""" 
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
▶▶▶▶GUILD DETAILS◀◀◀◀
Achievements: {data['achievements']}\n\n
Balance : {fix_num(data['balance'])}\n\n
Clan Name : {data['clan_name']}\n\n
Expire Time : {fix_num(data['guild_details']['expire_time'])}\n\n
Members Online : {fix_num(data['guild_details']['members_online'])}\n\n
Regional : {data['guild_details']['regional']}\n\n
Reward Time : {fix_num(data['guild_details']['reward_time'])}\n\n
Total Members : {fix_num(data['guild_details']['total_members'])}\n\n
ID : {fix_num(data['id'])}\n\n
Last Active : {fix_num(data['last_active'])}\n\n
Level : {fix_num(data['level'])}\n\n
Rank : {fix_num(data['rank'])}\n\n
Region : {data['region']}\n\n
Score : {fix_num(data['score'])}\n\n
Timestamp1 : {fix_num(data['timestamp1'])}\n\n
Timestamp2 : {fix_num(data['timestamp2'])}\n\n
Welcome Message: {data['welcome_message']}\n\n
XP: {fix_num(data['xp'])}\n\n
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
[FFB300][b][c]MADE BY Delta Rare Exe
            """
            return msg
        else:
            msg = """
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
Failed to get info, please try again later!!

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
[FFB300][b][c]MADE BY Delta Rare Exe
            """
            return msg
    except:
        pass


#GET INFO BY PLAYER ID
def get_player_info(player_id):
    url = f"https://like2.vercel.app/player-info?uid={player_id}&server={server2}&key={key2}"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        try:
            r = response.json()
            return {
                "Account Booyah Pass": f"{r.get('booyah_pass_level', 'N/A')}",
                "Account Create": f"{r.get('createAt', 'N/A')}",
                "Account Level": f"{r.get('level', 'N/A')}",
                "Account Likes": f" {r.get('likes', 'N/A')}",
                "Name": f"{r.get('nickname', 'N/A')}",
                "UID": f" {r.get('accountId', 'N/A')}",
                "Account Region": f"{r.get('region', 'N/A')}",
            }
        except ValueError as e:
            pass
            return {"error": "Invalid JSON response"}
    else:
        pass
        return {"error": f"Failed to fetch data: {response.status_code}"}


#CHAT WITH AI
def talk_with_ai(question):
    url = f"https://gemini-api-api-v2.vercel.app/prince/api/v1/ask?key=prince&ask={question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        msg = data["message"]["content"]
        return msg
    else:
        return "An error occurred while connecting to the server."


#SPAM REQUESTS
def spam_requests(player_id):
    # This URL now correctly points to the Flask app you provided
    url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
    try:
        res = requests.get(url, timeout=20)  # Added a timeout
        if res.status_code == 200:
            data = res.json()
            # Return a more descriptive message based on the API's JSON response
            return f"API Status: Success [{data.get('success_count', 0)}] Failed [{data.get('failed_count', 0)}]"
        else:
            # Return the error status from the API
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle cases where the API isn't running or is unreachable
        print(f"Could not connect to spam API: {e}")
        return "Failed to connect to spam API."


####################################


# ** NEW INFO FUNCTION using the new API **
def newinfo(uid):
    # Base URL without parameters
    url = "https://like2.vercel.app/player-info"
    # Parameters dictionary - this is the robust way to do it
    params = {
        'uid': uid,
        'server': server2,  # Hardcoded to bd as requested
        'key': key2
    }
    try:
        # Pass the parameters to requests.get()
        response = requests.get(url, params=params, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the expected data structure is in the response
            if "basicInfo" in data:
                return {"status": "ok", "data": data}
            else:
                # The API returned 200, but the data is not what we expect (e.g., error message in JSON)
                return {
                    "status": "error",
                    "message": data.get("error",
                                        "Invalid ID or data not found.")
                }
        else:
            # The API returned an error status code (e.g., 404, 500)
            try:
                # Try to get a specific error message from the API's response
                error_msg = response.json().get(
                    'error', f"API returned status {response.status_code}")
                return {"status": "error", "message": error_msg}
            except ValueError:
                # If the error response is not JSON
                return {
                    "status": "error",
                    "message": f"API returned status {response.status_code}"
                }

    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., timeout, no connection)
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except ValueError:
        # Handle cases where the response is not valid JSON
        return {
            "status": "error",
            "message": "Invalid JSON response from API."
        }


#ADDING-100-LIKES-IN-24H
def send_likes(uid):
    try:
        likes_api_response = requests.get(
            f"https://freefirebd.up.railway.app/like?uid={uid}&server_name={bd}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS_TOKEN}",
            timeout=15)

        if likes_api_response.status_code != 200:
            return f"""
[C][B][FF0000]━━━━━
[FFFFFF]Like API Error!
Status Code: {likes_api_response.status_code}
Please check if the uid is correct.
━━━━━
"""

        api_json_response = likes_api_response.json()

        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # ✅ Success
            return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Likes Status:

[00FF00]Likes Sent Successfully!

[FFFFFF]Player Name : [00FF00]{player_name}  
[FFFFFF]Likes Added : [00FF00]{likes_added}  
[FFFFFF]Likes Before : [00FF00]{likes_before}  
[FFFFFF]Likes After : [00FF00]{likes_after}  
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Subscribe: [FFFFFF]SPIDEERIO YT [00FF00]!!
"""
        elif status == 2 or likes_before == likes_after:
            # 🚫 Already claimed / Maxed
            return f"""
[C][B][FF0000]━━━━━━━━━━━━

[FFFFFF]No Likes Sent!

[FF0000]You have already taken likes with this UID.
Try again after 24 hours.

[FFFFFF]Player Name : [FF0000]{player_name}  
[FFFFFF]Likes Before : [FF0000]{likes_before}  
[FFFFFF]Likes After : [FF0000]{likes_after}  
[C][B][FF0000]━━━━━━━━━━━━
"""
        else:
            # ❓ Unexpected case
            return f"""
[C][B][FF0000]━━━━━━━━━━━━
[FFFFFF]Unexpected Response!
Something went wrong.

Please try again or contact support.
━━━━━━━━━━━━
"""

    except requests.exceptions.RequestException:
        return """
[C][B][FF0000]━━━━━
[FFFFFF]Like API Connection Failed!
Is the API server (app.py) running?
━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]An unexpected error occurred:
[FF0000]{str(e)}
━━━━━
"""


####################################
# =================== WHITELIST SYSTEM FUNCTIONS (NEW FROM BBUND) ===================

def load_whitelist():
    """Load whitelist from JSON file"""
    global WHITELISTED_UIDS, WHITELIST_DATA
    try:
        if os.path.exists(WHITELIST_FILE):
            with open(WHITELIST_FILE, 'r') as f:
                WHITELIST_DATA = json.load(f)
                WHITELISTED_UIDS = set(WHITELIST_DATA.keys())
                print(f"✅ Loaded {len(WHITELISTED_UIDS)} whitelisted UIDs")
        else:
            WHITELIST_DATA = {}
            WHITELISTED_UIDS = set()
            print("📝 No whitelist file found, starting fresh")
    except Exception as e:
        print(f"❌ Error loading whitelist: {e}")
        WHITELIST_DATA = {}
        WHITELISTED_UIDS = set()


def save_whitelist():
    """Save whitelist to JSON file"""
    try:
        with open(WHITELIST_FILE, 'w') as f:
            json.dump(WHITELIST_DATA, f, indent=2)
        print(f"✅ Saved whitelist ({len(WHITELISTED_UIDS)} UIDs)")
        return True
    except Exception as e:
        print(f"❌ Error saving whitelist: {e}")
        return False


def is_whitelisted(uid):
    """Check if UID is whitelisted"""
    return str(uid) in WHITELISTED_UIDS


def add_to_whitelist(uid, note=""):
    """Add UID to whitelist"""
    global WHITELISTED_UIDS, WHITELIST_DATA
    uid_str = str(uid)
    WHITELISTED_UIDS.add(uid_str)
    WHITELIST_DATA[uid_str] = {
        "note": note,
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_whitelist()
    return True


def remove_from_whitelist(uid):
    """Remove UID from whitelist"""
    global WHITELISTED_UIDS, WHITELIST_DATA
    uid_str = str(uid)
    if uid_str in WHITELISTED_UIDS:
        WHITELISTED_UIDS.remove(uid_str)
        del WHITELIST_DATA[uid_str]
        save_whitelist()
        return True
    return False


def get_whitelist_info():
    """Get formatted whitelist information"""
    if not WHITELISTED_UIDS:
        return "No whitelisted UIDs"
    
    info = []
    for uid, data in WHITELIST_DATA.items():
        note = data.get('note', 'No note')
        added = data.get('added_at', 'Unknown')
        info.append(f"• {uid} - {note} (Added: {added})")
    
    return "\n".join(info)


# =================== ROOM FUNCTIONS (FROM BBUND) ===================

async def join_custom_room(room_id, room_password, key, iv, region):
    """Join custom room with proper Free Fire packet structure"""
    fields = {
        1: 61,  # Room join packet type
        2: {
            1: int(room_id),
            2: {
                1: int(room_id),
                2: int(time.time()),
                3: "BOT",
                5: 12,
                6: 9999999,
                7: 1,
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,
            },
            3: str(room_password),
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)


async def Room_Spam(Uid, Rm, Nm, K, V):
    """Create room spam packet"""
    fields = {
        1: 78,
        2: {
            1: int(Rm),  
            2: "iG:[C][B][FF0000]Black_Apis",  
            3: {
                2: 1,
                3: 1
            },
            4: 330,      
            5: 6000,     
            6: 201,      
            10: int(await xBunnEr()),  
            11: int(Uid),
            12: 1,       
            15: {
                1: 1,
                2: 32768
            },
            16: 32768,    
            18: {
                1: 11481904755,  
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            31: {
                1: 1,
                2: 32768
            },
            32: 32768,    
            34: {
                1: int(Uid),   
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        }
    }
    
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)


def get_random_sticker():
    """Randomly select one sticker from available packs"""
    sticker_packs = [
        ("1200000001", 1, 24),
        ("1200000002", 1, 15),
        ("1200000004", 1, 13),
    ]
    pack_id, start, end = random.choice(sticker_packs)
    sticker_no = random.randint(start, end)
    return f"[1={pack_id}-{sticker_no}]"


async def send_msg_in_room_async(Msg, room_id, key, iv):
    """Send message in custom room"""
    sticker_value = get_random_sticker()
    
    fields = {
        1: 1,
        2: {
            1: int(room_id),
            2: int(room_id),
            3: 3,
            4: f"{Msg}",
            5: int(datetime.now().timestamp()),
            7: 2,
            8: f'{{"StickerStr" : "{sticker_value}", "type":"Sticker"}}',
            9: {
                1: "byte bot",
                2: int(await xBunnEr()),
                4: 329,
                7: 1,
            },
            10: "en",
            13: {2: 1, 3: 1},
        },
    }

    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex() + "7200"
    encrypted_packet = await encrypt_packet(packet_hex, key, iv)
    
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)

    if len(header_length_final) == 2:
        final_packet = "1215000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "121500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "12150000" + header_length_final + encrypted_packet
    else:
        final_packet = "12150000" + header_length_final + encrypted_packet
        
    return bytes.fromhex(final_packet)


# =================== TITLE FUNCTIONS (FROM BBUND) ===================

def titles():
    """Return all titles"""
    return [905090075, 904990072, 904990069, 905190079]


async def convert_kyro_to_your_system(target_uid, chat_id, key, iv, nickname="RIJEXX", title_id=None):
    """Send title packet with customizable title ID"""
    try:
        if title_id is None:
            available_titles = [905090075, 904990072, 904990069, 905190079]
            title_id = random.choice(available_titles)
        
        fields = {
            1: 1,
            2: {
                1: int(target_uid),
                2: int(chat_id),
                5: int(datetime.now().timestamp()),
                8: f'{{"TitleID":{title_id},"type":"Title"}}',
                9: {
                    1: f"[C][B][FF0000]{nickname}",
                    2: int(await xBunnEr()),
                    4: 330,
                    5: 102000015,
                    8: "BOT TEAM",
                    10: 1,
                    11: 1,
                    13: {1: 2},
                    14: {
                        1: 1158053040,
                        2: 8,
                        3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {2: 2, 3: 1},
                14: {}
            }
        }
        
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"
        
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)
        
        print(f"✅ Created packet with Title ID: {title_id}")
        return final_packet
        
    except Exception as e:
        print(f"❌ Title conversion error: {e}")
        return None


async def send_all_titles_sequentially(uid, chat_id, key, iv, region, chat_type):
    """Send all titles one by one with 2-second delay"""
    all_titles = [905090075, 904990072, 904990069, 905190079]
    total_titles = len(all_titles)
    
    start_msg = f"""[B][C][00FF00]🎖️ STARTING TITLE SEQUENCE!

📊 Total Titles: {total_titles}
⏱️ Delay: 2 seconds between titles
🎯 Target: {xMsGFixinG(uid)}

⏳ Sending titles now...
"""
    await safe_send_message(chat_type, start_msg, uid, chat_id, key, iv)
    
    try:
        for index, title_id in enumerate(all_titles):
            title_number = index + 1
            
            progress_msg = f"""[B][C][FFFF00]📤 SENDING TITLE {title_number}/{total_titles}

🎖️ Title ID: {title_id}
📊 Progress: {title_number}/{total_titles}
"""
            await safe_send_message(chat_type, progress_msg, uid, chat_id, key, iv)
            
            title_packet = await convert_kyro_to_your_system(uid, chat_id, key, iv, nickname="XAHAF_LEGACY", title_id=title_id)
            
            if title_packet and whisper_writer:
                whisper_writer.write(title_packet)
                await whisper_writer.drain()
                print(f"✅ Sent title {title_number}/{total_titles}: {title_id}")
            
            if title_number < total_titles:
                await asyncio.sleep(2)
        
        completion_msg = f"""[B][C][00FF00]✅ ALL TITLES SENT!

🎊 Total: {total_titles} titles
🎯 Target: {xMsGFixinG(uid)}
✅ Status: Complete!
"""
        await safe_send_message(chat_type, completion_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)


# =================== SPAM FUNCTIONS (FROM BBUND) ===================

async def reject_spam_loop(target_uid, key, iv):
    """Send reject spam packets to target"""
    global reject_spam_running
    
    count = 0
    max_spam = 150
    
    while reject_spam_running and count < max_spam:
        try:
            packet1 = await banecipher1(target_uid, key, iv)
            packet2 = await banecipher(target_uid, key, iv)
            
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet1)
            await asyncio.sleep(0.1)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet2)
            
            count += 1
            print(f"Sent reject spam #{count} to {xMsGFixinG(target_uid)}")
            await asyncio.sleep(0.2)
            
        except Exception as e:
            print(f"Error in reject spam: {e}")
            break
    
    return count


async def banecipher(target_uid, key, iv):
    """Create reject spam packet 1"""
    banner_text = """
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
"""        
    fields = {
        1: 5,
        2: {
            1: int(target_uid),
            2: 1,
            3: int(target_uid),
            4: banner_text
        }
    }
    
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)


async def banecipher1(target_uid, key, iv):
    """Create reject spam packet 2"""
    gay_text = """
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
"""        
    fields = {
        1: int(target_uid),
        2: 5,
        4: 50,
        5: {
            1: int(target_uid),
            2: gay_text,
        }
    }
    
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)


async def evo_cycle_spam(uids, key, iv, region, LoGinDaTaUncRypTinG):
    """Cycle through all evolution emotes"""
    global evo_cycle_running
    
    try:
        bot_uid = LoGinDaTaUncRypTinG.AccountUID
        print(f"🤖 Using bot UID: {bot_uid}")
    except:
        bot_uid = 13777711848
        print(f"🤖 Using fallback bot UID: {bot_uid}")
    
    evo_emotes = {
        "1": "909000063", "2": "909000068", "3": "909000075", "4": "909040010",
        "5": "909000081", "6": "909039011", "7": "909000085", "8": "909000090",
        "9": "909000098", "10": "909035007", "11": "909042008", "12": "909041005",
        "13": "909033001", "14": "909038010", "15": "909038012", "16": "909045001",
        "17": "909049010", "18": "909051003"
    }
    
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        print(f"Starting evolution emote cycle #{cycle_count}")
        
        emote_list = list(evo_emotes.items())
        total_emotes = len(emote_list)
        
        for index, (emote_number, emote_id) in enumerate(emote_list):
            if not evo_cycle_running:
                break
                
            for uid in uids:
                try:
                    uid_int = int(uid)
                    user_emote = await Emote_k(uid_int, int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', user_emote)
                    print(f"👤 User emote #{emote_number}")
                except Exception as e:
                    print(f"Error: {e}")
            
            await asyncio.sleep(0.5)
            
            opposite_index = total_emotes - 1 - index
            opposite_number, opposite_id = emote_list[opposite_index]
            
            try:
                bot_self_emote = await Emote_k(int(bot_uid), int(opposite_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_self_emote)
                
                await asyncio.sleep(0.3)
                if uids:
                    first_uid = int(uids[0])
                    bot_to_user = await Emote_k(first_uid, int(opposite_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_to_user)
                
                print(f"🤖 Bot OPPOSITE emote #{opposite_number}")
            except Exception as e:
                print(f"Bot error: {e}")
            
            if evo_cycle_running:
                wait_time = 5
                for i in range(wait_time):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
    
    print("Cycle stopped")


async def get_colorful_message(message_text, message_number):
    """Generate message with different colors"""
    color_palette = ["FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", 
                     "00FFFF", "FFA500", "FF1493", "00FF7F", "7B68EE",
                     "FFD700", "00CED1", "FF69B4", "32CD32", "9370DB",
                     "FF4500", "1E90FF", "ADFF2F", "FF6347", "8A2BE2"]
    
    color_index = (message_number - 1) % len(color_palette)
    return f"[C][B][{color_palette[color_index]}]{message_text}"


def get_random_avatar():
    """Get random avatar ID"""
    avatar_list = [
        '902050001', '902050002', '902050003', '902039016', '902050004', 
        '902047011', '902047010', '902049015', '902050006', '902049020'
    ]
    return random.choice(avatar_list)


async def xSEndMsgsQQ(Msg, id, K, V):
    """Send message to squad chat"""
    fields = {
        1: id, 2: id, 4: Msg, 5: 1756580149, 7: 2, 8: 904990072,
        9: {
            1: "xBe4!sTo - C4", 2: int(get_random_avatar()), 4: 330, 5: 1001000001,
            8: "xBe4!sTo - C4", 10: 1, 11: 1, 13: {1: 2},
            14: {1: 1158053040, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}
        },
        10: "en", 13: {2: 2, 3: 1}
    }
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)


async def msg_spam_loop(message_text, times, chat_id, key, iv, region):
    """Send message multiple times in team chat"""
    global msg_spam_running
    
    count = 0
    
    while msg_spam_running and count < times:
        try:
            colorful_message = await get_colorful_message(message_text, count + 1)
            msg_packet = await xSEndMsgsQQ(colorful_message, int(chat_id), key, iv)
            
            if not msg_packet:
                print("❌ Failed to create message packet")
                break
                
            if whisper_writer:
                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', msg_packet)
                count += 1
                print(f"✅ Sent message #{count}/{times}")
                await asyncio.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Error in msg spam loop: {e}")
            break
    
    return count


####################################
#CHECK ACCOUNT IS BANNED

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB52"
}


# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]",
        "[FFFFFF]", "[FFA500]", "[A52A2A]", "[800080]", "[000000]", "[808080]",
        "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]", "[90EE90]", "[D2691E]",
        "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]",
        "[4682B4]", "[6495ED]", "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]",
        "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]", "[6B8E23]", "[808000]",
        "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]",
        "[1E90FF]", "[191970]", "[00008B]", "[000080]", "[008080]", "[008B8B]",
        "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]", "[FAEBD7]"
    ]
    return random.choice(colors)


# ---- Auto Bundle Helper ----
def get_auto_bundle_id():
    """Get bundle ID based on AUTO_BUNDLE_MODE"""
    global AUTO_BUNDLE_MODE, AUTO_BUNDLE_ID, AVAILABLE_BUNDLES
    
    if AUTO_BUNDLE_MODE == "random":
        # Return random bundle ID
        bundle_ids = list(AVAILABLE_BUNDLES.values())
        return random.choice(bundle_ids)
    else:
        # Return fixed bundle ID
        return AUTO_BUNDLE_ID


# ---- Auto Rank/Banner/Avatar Helpers ----
def get_auto_rank():
    """Get rank based on AUTO_RANK_MODE"""
    global AUTO_RANK_MODE, AUTO_RANK_ID, AVAILABLE_RANKS
    
    if AUTO_RANK_MODE == "random":
        return random.choice(AVAILABLE_RANKS)
    else:
        return AUTO_RANK_ID


def get_auto_banner():
    """Get banner ID based on AUTO_BANNER_MODE"""
    global AUTO_BANNER_MODE, AUTO_BANNER_ID, AVAILABLE_BANNERS
    
    if AUTO_BANNER_MODE == "random":
        return random.choice(AVAILABLE_BANNERS)
    else:
        return AUTO_BANNER_ID


def get_auto_avatar():
    """Get avatar ID based on AUTO_AVATAR_MODE"""
    global AUTO_AVATAR_MODE, AUTO_AVATAR_ID, AVAILABLE_AVATARS
    
    if AUTO_AVATAR_MODE == "random":
        return random.choice(AVAILABLE_AVATARS)
    else:
        return AUTO_AVATAR_ID


# =================== NEW HELPER FUNCTIONS (FROM BBUND) ===================

# Bio change functions
def get_bio_server_url(region="BD"):
    """Get bio server URL based on region"""
    return "https://clientbp.common.ggblueshark.com/SetBio"


def decode_jwt_noverify(token):
    """Decode JWT without verification"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload = parts[1]
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
        bio_bytes = bio_text.encode('utf-8')
        field_header = (1 << 3) | 2
        length = len(bio_bytes)
        protobuf_data = bytes([field_header, length]) + bio_bytes
        return protobuf_data
    except Exception as e:
        print(f"Protobuf creation error: {e}")
        return b""


async def set_bio_directly_async(jwt_token, bio_text, region="BD"):
    """Set bio directly"""
    try:
        payload = decode_jwt_noverify(jwt_token)
        if not payload:
            return {"success": False, "message": "Invalid JWT token"}
        
        lock_region = payload.get("lock_region", region).upper()
        url_bio = get_bio_server_url(lock_region)
        
        data_bytes = create_bio_protobuf(bio_text)
        cipher = AES.new(BIO_ENCRYPTION_KEY, AES.MODE_CBC, BIO_ENCRYPTION_IV)
        
        padding_length = 16 - (len(data_bytes) % 16)
        if padding_length:
            data_bytes += bytes([padding_length] * padding_length)
        
        encrypted_data = cipher.encrypt(data_bytes)
        
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": FREEFIRE_VERSION,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
        }
        
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url_bio, headers=headers, data=encrypted_data) as response:
                if response.status == 200:
                    return {"success": True, "message": "Bio updated!", "region": lock_region, "bio": bio_text}
                else:
                    return {"success": False, "message": f"Server error: {response.status}"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def load_credentials_from_file(filename="Bot.txt"):
    """Load bot credentials from file"""
    try:
        if not os.path.exists(filename):
            return None
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if ',' in content:
            parts = content.split(',')
            if len(parts) >= 2:
                uid = parts[0].strip().replace('uid=', '').replace('UID=', '')
                password = parts[1].strip().replace('password=', '').replace('PASSWORD=', '')
                return (uid, password)
        return None
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None


# Freeze emote spam function
async def freeze_emote_spam(uid, key, iv, region):
    """Send 3 freeze emotes in 1-second cycles for 10 seconds"""
    global freeze_running
    try:
        cycles = 0
        max_cycles = FREEZE_DURATION
        while freeze_running and cycles < max_cycles:
            for i, emote_id in enumerate(FREEZE_EMOTES):
                if not freeze_running:
                    break
                try:
                    emote_packet = await Emote_k(int(uid), emote_id, key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"Error sending freeze emote: {e}")
            cycles += 1
            remaining_time = 1.0 - (0.3 * len(FREEZE_EMOTES))
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
        return cycles
    except Exception as e:
        print(f"Freeze function error: {e}")
        return 0


async def handle_freeze_completion(freeze_task, uid, sender_uid, chat_id, chat_type, key, iv):
    """Handle freeze command completion"""
    try:
        cycles_completed = await freeze_task
        completion_msg = f"""[B][C][00FFFF]❄️ FREEZE COMPLETED!
🎯 Target: {uid}
⏱️ Duration: {cycles_completed} seconds
✅ Status: Complete!"""
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
    except asyncio.CancelledError:
        print("Freeze cancelled")
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Freeze error: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)


# Friend request functions (HTTP API based - like BBUND)
async def send_friend_request_http(target_uid, jwt_token, region="BD"):
    """Send friend request via HTTP API (BBUND style)"""
    try:
        # Create protobuf packet
        fields = {1: 1, 2: {1: int(target_uid), 2: 1}}
        packet_hex = (await CrEaTe_ProTo(fields)).hex()
        
        # Encrypt packet
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        packet_bytes = bytes.fromhex(packet_hex)
        padded_packet = pad(packet_bytes, AES.block_size)
        encrypted_payload = cipher.encrypt(padded_packet).hex()
        
        # Determine URL based on region
        if region.upper() == "BD":
            url = "https://client.bd.freefiremobile.com/RequestAddingFriend"
        elif region.upper() == "IND":
            url = "https://client.ind.freefiremobile.com/RequestAddingFriend"
        else:
            url = "https://client.bd.freefiremobile.com/RequestAddingFriend"
        
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": "OB52"
        }
        
        # Send HTTP request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=10, ssl=False) as response:
                if response.status == 200:
                    return True, "Friend request sent!"
                else:
                    return False, f"Server error: {response.status}"
    except Exception as e:
        print(f"Friend request HTTP error: {e}")
        return False, str(e)


async def remove_friend_http(target_uid, jwt_token, region="BD"):
    """Remove friend via HTTP API"""
    try:
        # Create protobuf packet for remove friend
        fields = {1: 2, 2: {1: int(target_uid)}}
        packet_hex = (await CrEaTe_ProTo(fields)).hex()
        
        # Encrypt packet
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        packet_bytes = bytes.fromhex(packet_hex)
        padded_packet = pad(packet_bytes, AES.block_size)
        encrypted_payload = cipher.encrypt(padded_packet).hex()
        
        # Determine URL based on region
        if region.upper() == "BD":
            url = "https://client.bd.freefiremobile.com/RequestAddingFriend"
        elif region.upper() == "IND":
            url = "https://client.ind.freefiremobile.com/RequestAddingFriend"
        else:
            url = "https://client.bd.freefiremobile.com/RequestAddingFriend"
        
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": "OB52"
        }
        
        # Send HTTP request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=10, ssl=False) as response:
                if response.status == 200:
                    return True, "Friend removed!"
                else:
                    return False, f"Server error: {response.status}"
    except Exception as e:
        print(f"Remove friend HTTP error: {e}")
        return False, str(e)

# =================== END NEW HELPER FUNCTIONS ===================


async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload


async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret":
        "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return (None, None)
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)


async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.120.2"  # UPDATED from 1.20.1 to 1.120.2 (BBUND version)
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)


async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr,
                                ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None


async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr,
                                ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None


async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto


async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto


async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto


async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto


async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else:
        print('Unexpected length')
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"


async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'


async def SEndMsG(H, message, Uid, chat_id, key, iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid':
        msg_packet = await xSEndMsgsQ(message, chat_id, key, iv)
    elif TypE == 'CLan':
        msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    elif TypE == 'PrivaTe':
        msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
    return msg_packet


async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT:
        whisper_writer.write(PacKeT)
        await whisper_writer.drain()
    elif TypE == 'OnLine':
        online_writer.write(PacKeT)
        await online_writer.drain()
    else:
        return 'UnsoPorTed TypE ! >> ErrrroR (:():)'


async def safe_send_message(chat_type,
                            message,
                            target_uid,
                            chat_id,
                            key,
                            iv,
                            max_retries=3):
    """Safely send message with retry mechanism"""
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            print(f"Message sent successfully on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)  # Wait before retry
    return False


async def fast_emote_spam(uids, emote_id, key, iv, region):
    """Fast emote spam function that sends emotes rapidly"""
    global fast_spam_running
    count = 0
    max_count = 25  # Spam 25 times

    while fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in fast_emote_spam for uid {uid}: {e}")

        count += 1
        await asyncio.sleep(0.1)  # 0.1 seconds interval between spam cycles


# NEW FUNCTION: Custom emote spam with specified times
async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    """Custom emote spam function that sends emotes specified number of times"""
    global custom_spam_running
    count = 0

    while custom_spam_running and count < times:
        try:
            uid_int = int(uid)
            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.1)  # 0.1 seconds interval between emotes
        except Exception as e:
            print(f"Error in custom_emote_spam for uid {uid}: {e}")
            break


# ENHANCED FUNCTION: Multi-account spam request loop with Badge/Rank support
# Uses ALL 34 SPM accounts from spm_inv_accounts.py for mass spam
async def spam_request_loop(target_uid, main_key, main_iv, main_region):
    """Enhanced spam request function using ALL 34 SPM accounts with Badge/Rank support"""
    global spam_request_running, online_writer, whisper_writer
    
    from xC4 import SEnd_InV_Enhanced, OpEnSq_Enhanced
    from spm_inv_accounts import SPM_INV_BOT_SETTINGS
    
    settings = SPM_INV_BOT_SETTINGS
    total_sent = 0
    
    # First, connect SPM accounts
    print(f"[SPM_INV] Connecting SPM accounts for mass spam to {target_uid}...")
    connected_count = await connection_pool.connect_spm_accounts(count=34)
    
    if connected_count == 0:
        print(f"[SPM_INV] No SPM accounts connected, using MAIN BOT as fallback!")
        # Fallback to main bot
        if not online_writer:
            print(f"[SPM_INV] Main bot not connected!")
            return
        
        try:
            for i in range(30):
                if not spam_request_running:
                    break
                    
                PAc = await OpEnSq(main_key, main_iv, main_region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                await asyncio.sleep(0.2)
                
                V = await SEnd_InV(5, int(target_uid), main_key, main_iv, main_region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                await asyncio.sleep(0.2)
                
                E = await ExiT(None, main_key, main_iv)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                
                total_sent += 1
                print(f"[SPM_INV] MAIN BOT Sent #{total_sent} to {target_uid}")
                await asyncio.sleep(0.5)
                
            print(f"[SPM_INV] Completed! Sent {total_sent} requests to {target_uid}")
        except Exception as e:
            print(f"[SPM_INV] Error: {e}")
        return
    
    # Get all connected SPM bots
    spm_bots = connection_pool.get_all_connected_spm_bots()
    print(f"[SPM_INV] ✅ {len(spm_bots)} SPM accounts connected! Starting MASS SPAM with Badge/Rank!")
    
    try:
        # Send invites from ALL connected accounts simultaneously
        rounds = 3  # Each account sends 3 invites
        
        for round_num in range(rounds):
            if not spam_request_running:
                break
                
            print(f"[SPM_INV] Round {round_num + 1}/{rounds} - Sending from {len(spm_bots)} accounts...")
            
            # Create tasks for all bots to send simultaneously
            async def send_invite_from_bot(bot):
                try:
                    # Open squad with enhanced settings
                    PAc = await OpEnSq_Enhanced(
                        bot.key, bot.iv, bot.region,
                        name=settings['name'],
                        badge=settings['badge'],
                        level=settings['level']
                    )
                    await bot.send_packet(PAc)
                    await asyncio.sleep(0.1)
                    
                    # Send enhanced invite with Badge/Rank
                    V = await SEnd_InV_Enhanced(
                        target_uid=int(target_uid),
                        bot_uid=int(bot.uid),
                        K=bot.key,
                        V=bot.iv,
                        region=bot.region,
                        name=settings['name'],
                        badge=settings['badge'],
                        level=settings['level'],
                        rank=settings['rank'],
                        banner_id=settings['banner_id'],
                        avatar_id=settings['avatar_id']
                    )
                    await bot.send_packet(V)
                    await asyncio.sleep(0.1)
                    
                    # Exit squad
                    E = await ExiT(None, bot.key, bot.iv)
                    await bot.send_packet(E)
                    
                    return True
                except Exception as e:
                    print(f"[SPM_INV] Error from bot {bot.uid}: {e}")
                    return False
            
            # Execute all bots simultaneously
            tasks = [send_invite_from_bot(bot) for bot in spm_bots if bot.connected]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            success_count = sum(1 for r in results if r is True)
            total_sent += success_count
            
            print(f"[SPM_INV] Round {round_num + 1} completed: {success_count}/{len(tasks)} successful")
            
            if round_num < rounds - 1:
                await asyncio.sleep(0.5)
        
        print(f"[SPM_INV] ✅ MASS SPAM COMPLETED! Total {total_sent} invites sent to {target_uid} with Badge/Rank!")
        
    except Exception as e:
        print(f"[SPM_INV] Error: {e}")


# NEW FUNCTION: Evolution emote spam with mapping
async def evo_emote_spam(uids, number, key, iv, region):
    """Send evolution emotes based on number mapping"""
    try:
        emote_id = EMOTE_MAP.get(int(number))
        if not emote_id:
            return False, f"Invalid number! Use 1-21 only."

        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error sending evo emote to {uid}: {e}")

        return True, f"Sent evolution emote {number} (ID: {emote_id}) to {success_count} player(s)"

    except Exception as e:
        return False, f"Error in evo_emote_spam: {str(e)}"


# NEW FUNCTION: Fast evolution emote spam
async def evo_fast_emote_spam(uids, number, key, iv, region):
    """Fast evolution emote spam function"""
    global evo_fast_spam_running
    count = 0
    max_count = 25  # Spam 25 times

    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."

    while evo_fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_fast_emote_spam for uid {uid}: {e}")

        count += 1
        await asyncio.sleep(0.1)  # CHANGED: 0.5 seconds to 0.1 seconds

    return True, f"Completed fast evolution emote spam {count} times"


# NEW FUNCTION: Custom evolution emote spam with specified times
async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    """Custom evolution emote spam with specified repeat times"""
    global evo_custom_spam_running
    count = 0

    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."

    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_custom_emote_spam for uid {uid}: {e}")

        count += 1
        await asyncio.sleep(0.1)  # CHANGED: 0.5 seconds to 0.1 seconds

    return True, f"Completed custom evolution emote spam {count} times"


async def TcPOnLine(ip, port, key, iv, AutHToKen, region, reconnect_delay=0.5):
    global online_writer, spam_room, whisper_writer, spammer_uid, spam_chat_id, spam_uid, XX, uid, Spy, data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, current_group_members, AUTO_BUNDLE_ENABLED, AUTO_BUNDLE_MODE, AUTO_BUNDLE_ID, AUTO_RANK_ENABLED, AUTO_RANK_MODE, AUTO_RANK_ID, AUTO_BANNER_ENABLED, AUTO_BANNER_MODE, AUTO_BANNER_ID, AUTO_AVATAR_ENABLED, AUTO_AVATAR_MODE, AUTO_AVATAR_ID

    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            
            # =================== AUTO NARUTO BUNDLE ON CONNECT ===================
            try:
                if AUTO_BUNDLE_ENABLED:
                    from xC4 import bundle_packet_async
                    bundle_id = get_auto_bundle_id()
                    bundle_packet = await bundle_packet_async(bundle_id, key, iv, region)
                    if bundle_packet and online_writer:
                        online_writer.write(bundle_packet)
                        await online_writer.drain()
                        print(f"✅ AUTO BUNDLE sent on connect! (ID: {bundle_id}, Mode: {AUTO_BUNDLE_MODE})")
                
                # Auto Rank
                if AUTO_RANK_ENABLED:
                    from xC4 import rank_packet_async
                    rank_id = get_auto_rank()
                    rank_packet = await rank_packet_async(rank_id, key, iv, region)
                    if rank_packet and online_writer:
                        online_writer.write(rank_packet)
                        await online_writer.drain()
                        print(f"✅ AUTO RANK sent on connect! (ID: {rank_id}, Mode: {AUTO_RANK_MODE})")
                
                # Auto Banner
                if AUTO_BANNER_ENABLED:
                    from xC4 import banner_packet_async
                    banner_id = get_auto_banner()
                    banner_packet = await banner_packet_async(banner_id, key, iv, region)
                    if banner_packet and online_writer:
                        online_writer.write(banner_packet)
                        await online_writer.drain()
                        print(f"✅ AUTO BANNER sent on connect! (ID: {banner_id}, Mode: {AUTO_BANNER_MODE})")
                
                # Auto Avatar
                if AUTO_AVATAR_ENABLED:
                    from xC4 import avatar_packet_async
                    avatar_id = get_auto_avatar()
                    avatar_packet = await avatar_packet_async(avatar_id, key, iv, region)
                    if avatar_packet and online_writer:
                        online_writer.write(avatar_packet)
                        await online_writer.drain()
                        print(f"✅ AUTO AVATAR sent on connect! (ID: {avatar_id}, Mode: {AUTO_AVATAR_MODE})")
                        
            except Exception as e:
                print(f"❌ Auto send error on connect: {e}")
            # ====================================================================
            
            while True:
                data2 = await reader.read(9999)
                if not data2: break

                # =================== SQUAD MESSAGE HANDLING (0501) ===================
                # Handle squad/team chat messages
                if data2.hex().startswith('0501'):
                    try:
                        # =================== AUTO NARUTO BUNDLE ON SQUAD MESSAGE ===================
                        try:
                            if AUTO_BUNDLE_ENABLED:
                                from xC4 import bundle_packet_async
                                bundle_id = get_auto_bundle_id()
                                bundle_packet = await bundle_packet_async(bundle_id, key, iv, region)
                                if bundle_packet and online_writer:
                                    online_writer.write(bundle_packet)
                                    await online_writer.drain()
                                    print(f"✅ AUTO BUNDLE sent on squad message! (ID: {bundle_id}, Mode: {AUTO_BUNDLE_MODE})")
                            
                            # Auto Rank
                            if AUTO_RANK_ENABLED:
                                from xC4 import rank_packet_async
                                rank_id = get_auto_rank()
                                rank_packet = await rank_packet_async(rank_id, key, iv, region)
                                if rank_packet and online_writer:
                                    online_writer.write(rank_packet)
                                    await online_writer.drain()
                                    print(f"✅ AUTO RANK sent on squad message! (ID: {rank_id})")
                            
                            # Auto Banner
                            if AUTO_BANNER_ENABLED:
                                from xC4 import banner_packet_async
                                banner_id = get_auto_banner()
                                banner_packet = await banner_packet_async(banner_id, key, iv, region)
                                if banner_packet and online_writer:
                                    online_writer.write(banner_packet)
                                    await online_writer.drain()
                                    print(f"✅ AUTO BANNER sent on squad message! (ID: {banner_id})")
                            
                            # Auto Avatar
                            if AUTO_AVATAR_ENABLED:
                                from xC4 import avatar_packet_async
                                avatar_id = get_auto_avatar()
                                avatar_packet = await avatar_packet_async(avatar_id, key, iv, region)
                                if avatar_packet and online_writer:
                                    online_writer.write(avatar_packet)
                                    await online_writer.drain()
                                    print(f"✅ AUTO AVATAR sent on squad message! (ID: {avatar_id})")
                                    
                        except Exception as e:
                            print(f"❌ Auto send error on squad message: {e}")
                        # ====================================================================
                        
                        # Decode squad message
                        squad_msg = await decode_team_packet(data2.hex()[10:])
                        
                        # Extract message details
                        sender_uid = squad_msg.details.player_uid
                        team_session = squad_msg.details.team_session
                        
                        # Get message text from packet
                        try:
                            packet_data = await DeCode_PackEt(data2.hex()[10:])
                            packet_json = json.loads(packet_data)
                            
                            # Extract message text (usually in field 4)
                            message_text = packet_json.get('4', {}).get('data', '')
                            
                            if message_text:
                                print(f"[SQUAD] Message from {sender_uid}: {message_text}")
                                
                                # Process command if it starts with /
                                if message_text.lower().startswith('/'):
                                    inPuTMsG = message_text.lower()
                                    
                                    # Create a response object similar to whisper messages
                                    class SquadResponse:
                                        class Data:
                                            uid = sender_uid
                                            Chat_ID = team_session
                                            chat_type = 0  # Squad chat type
                                            msg = message_text
                                    
                                    response = SquadResponse()
                                    
                                    # Process commands (same as TcPChaT)
                                    # Example: /help command
                                    if inPuTMsG.strip() == "/help":
                                        help_msg = f"""[B][C][00FF00]🔥 BOT COMMANDS 🔥
[FFFFFF]/bundle name - Send bundle
[FFFFFF]/dance uid - Dance party
[FFFFFF]/help - Show this menu
[FFB300]Delta Rare Exe"""
                                        await safe_send_message(0, help_msg, sender_uid, team_session, key, iv)
                                    
                                    # /bundle command
                                    elif inPuTMsG.strip().startswith('/bundle'):
                                        parts = inPuTMsG.strip().split()
                                        if len(parts) < 2:
                                            bundle_list = f"""[B][C][00FF00]📦 BUNDLES:
[FFFFFF]rampage, cannibal, devil
[FFFFFF]scorpio, frostfire, paradox
[FFFFFF]naruto, aurora, midnight
[FFFFFF]itachi, dreamspace"""
                                            await safe_send_message(0, bundle_list, sender_uid, team_session, key, iv)
                                        else:
                                            bundle_name = parts[1]
                                            ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                                            success, message = await bundle_command_operation(ctx, bundle_name)
                                            result_msg = f"[B][C][00FF00]{message}\n" if success else f"[B][C][FF0000]{message}\n"
                                            await safe_send_message(0, result_msg, sender_uid, team_session, key, iv)
                                    
                                    # Add more commands here as needed
                                    print(f"[SQUAD] Processed command: {inPuTMsG}")
                        
                        except Exception as e:
                            print(f"[SQUAD] Error processing message: {e}")
                    
                    except Exception as e:
                        print(f"[SQUAD] Error decoding squad packet: {e}")
                # ====================================================================

                # =================== AUTO-ACCEPT OWNER INVITE (NEW) ===================
                if data2.hex().startswith('0500') and len(data2.hex()) > 100:
                    try:
                        packet_data = await DeCode_PackEt(data2.hex()[10:])
                        packet_json = json.loads(packet_data)
                        
                        print(f"[AUTO-JOIN] Received 0500 packet, length: {len(data2.hex())}")
                        
                        # Check if this is an invite packet
                        if '5' in packet_json and 'data' in packet_json['5']:
                            squad_data = packet_json['5']['data']
                            
                            print(f"[AUTO-JOIN] Found squad data")
                            
                            # Get squad owner UID (person who invited)
                            if '1' in squad_data and 'data' in squad_data['1']:
                                squad_owner = squad_data['1']['data']
                                
                                print(f"[AUTO-JOIN] Squad owner: {squad_owner}, Expected owner: {BOT_OWNER_UID}")
                                
                                # Get squad code
                                if '8' in squad_data and 'data' in squad_data['8']:
                                    squad_code = squad_data['8']['data']
                                    
                                    print(f"[AUTO-JOIN] Squad code: {squad_code}")
                                    
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
                                    else:
                                        print(f"[AUTO-JOIN] Owner mismatch or auto-accept disabled")
                                else:
                                    print(f"[AUTO-JOIN] No squad code in packet")
                            else:
                                print(f"[AUTO-JOIN] No squad owner in packet")
                        else:
                            print(f"[AUTO-JOIN] Not an invite packet (no field 5)")
                        
                    except Exception as e:
                        print(f"❌ Auto-join error: {e}")
                        import traceback
                        traceback.print_exc()
                # ================================================================

                # NEW: Capture group members from squad data
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        # =================== AUTO NARUTO BUNDLE ON SQUAD JOIN ===================
                        try:
                            if AUTO_BUNDLE_ENABLED:
                                from xC4 import bundle_packet_async
                                bundle_id = get_auto_bundle_id()
                                bundle_packet = await bundle_packet_async(bundle_id, key, iv, region)
                                if bundle_packet and online_writer:
                                    online_writer.write(bundle_packet)
                                    await online_writer.drain()
                                    print(f"✅ AUTO BUNDLE sent on squad join! (ID: {bundle_id}, Mode: {AUTO_BUNDLE_MODE})")
                            
                            # Auto Rank
                            if AUTO_RANK_ENABLED:
                                from xC4 import rank_packet_async
                                rank_id = get_auto_rank()
                                rank_packet = await rank_packet_async(rank_id, key, iv, region)
                                if rank_packet and online_writer:
                                    online_writer.write(rank_packet)
                                    await online_writer.drain()
                                    print(f"✅ AUTO RANK sent on squad join! (ID: {rank_id})")
                            
                            # Auto Banner
                            if AUTO_BANNER_ENABLED:
                                from xC4 import banner_packet_async
                                banner_id = get_auto_banner()
                                banner_packet = await banner_packet_async(banner_id, key, iv, region)
                                if banner_packet and online_writer:
                                    online_writer.write(banner_packet)
                                    await online_writer.drain()
                                    print(f"✅ AUTO BANNER sent on squad join! (ID: {banner_id})")
                            
                            # Auto Avatar
                            if AUTO_AVATAR_ENABLED:
                                from xC4 import avatar_packet_async
                                avatar_id = get_auto_avatar()
                                avatar_packet = await avatar_packet_async(avatar_id, key, iv, region)
                                if avatar_packet and online_writer:
                                    online_writer.write(avatar_packet)
                                    await online_writer.drain()
                                    print(f"✅ AUTO AVATAR sent on squad join! (ID: {avatar_id})")
                                    
                        except Exception as e:
                            print(f"❌ Auto send error on squad join: {e}")
                        # ====================================================================
                        
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet = json.loads(packet)
                        OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(
                            packet)

                        # Extract group members from packet
                        try:
                            if isinstance(packet, dict):
                                # Try to find members in various packet structures
                                members_data = packet.get('members', [])
                                if members_data:
                                    current_group_members = []
                                    for member in members_data:
                                        if isinstance(member, dict) and 'uid' in member:
                                            member_uid = str(member['uid'])
                                            if member_uid != str(bot_uid):
                                                current_group_members.append(member_uid)
                                    if current_group_members:
                                        print(f"Group members updated: {current_group_members}")
                        except Exception as e:
                            print(f"Error updating group members: {e}")

                        JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe,
                                                   key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT',
                                         JoinCHaT)

                        message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot ! '
                        P = await SEndMsG(0, message, OwNer_UiD, OwNer_UiD,
                                          key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT',
                                         P)

                    except Exception as e:
                        print(f"Error processing group data: {e}")
                        if data2.hex().startswith('0500') and len(
                                data2.hex()) > 1000:
                            try:
                                print(data2.hex()[10:])
                                packet = await DeCode_PackEt(data2.hex()[10:])
                                print(packet)
                                packet = json.loads(packet)
                                OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(
                                    packet)

                                JoinCHaT = await AutH_Chat(
                                    3, OwNer_UiD, CHaT_CoDe, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer,
                                                 'ChaT', JoinCHaT)

                                message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot ! \n\n{get_random_color()}- Commands : @a {xMsGFixinG("player_uid")} {xMsGFixinG("909000001")}\n\n[00FF00]Dev : @{xMsGFixinG("Delta Rare Exe")}'
                                P = await SEndMsG(0, message, OwNer_UiD,
                                                  OwNer_UiD, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer,
                                                 'ChaT', P)
                            except:
                                pass

            online_writer.close()
            await online_writer.wait_closed()
            online_writer = None

        except Exception as e:
            print(f"- ErroR With {ip}:{port} - {e}")
            online_writer = None
        await asyncio.sleep(reconnect_delay)


async def TcPChaT(ip,
                  port,
                  AutHToKen,
                  key,
                  iv,
                  LoGinDaTaUncRypTinG,
                  ready_event,
                  region,
                  jwt_token,
                  reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room, whisper_writer, spammer_uid, spam_chat_id, spam_uid, online_writer, chat_id, XX, uid, Spy, data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, current_group_members, bot_uid, freeze_running, freeze_task, WHITELIST_ONLY, WHITELISTED_UIDS, WHITELIST_DATA, reject_spam_running, reject_spam_task, evo_cycle_running, evo_cycle_task, msg_spam_running, msg_spam_task, current_room_id, room_info_cache, AUTO_BUNDLE_ENABLED, AUTO_BUNDLE_MODE, AUTO_BUNDLE_ID, AVAILABLE_BUNDLES, AUTO_RANK_ENABLED, AUTO_RANK_MODE, AUTO_RANK_ID, AUTO_BANNER_ENABLED, AUTO_BANNER_MODE, AUTO_BANNER_ID, AUTO_AVATAR_ENABLED, AUTO_AVATAR_MODE, AUTO_AVATAR_ID  # ADD all new variables

    # NEW: Task tracking for concurrent command execution
    active_tasks = set()

    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            
            # =================== AUTO BUNDLE/RANK/BANNER/AVATAR (NEW) ===================
            print("🔥 AUTO-SENDING BUNDLE/RANK/BANNER/AVATAR...")
            try:
                # Auto Bundle
                if AUTO_BUNDLE_ENABLED:
                    from xC4 import bundle_packet_async
                    bundle_id = get_auto_bundle_id()
                    bundle_packet = await bundle_packet_async(bundle_id, key, iv, region)
                    if bundle_packet and online_writer:
                        online_writer.write(bundle_packet)
                        await online_writer.drain()
                        print(f"✅ AUTO BUNDLE SENT! (ID: {bundle_id})")
                
                # Auto Rank
                if AUTO_RANK_ENABLED:
                    from xC4 import rank_packet_async
                    rank_id = get_auto_rank()
                    rank_packet = await rank_packet_async(rank_id, key, iv, region)
                    if rank_packet and online_writer:
                        online_writer.write(rank_packet)
                        await online_writer.drain()
                        print(f"✅ AUTO RANK SENT! (ID: {rank_id})")
                
                # Auto Banner
                if AUTO_BANNER_ENABLED:
                    from xC4 import banner_packet_async
                    banner_id = get_auto_banner()
                    banner_packet = await banner_packet_async(banner_id, key, iv, region)
                    if banner_packet and online_writer:
                        online_writer.write(banner_packet)
                        await online_writer.drain()
                        print(f"✅ AUTO BANNER SENT! (ID: {banner_id})")
                
                # Auto Avatar
                if AUTO_AVATAR_ENABLED:
                    from xC4 import avatar_packet_async
                    avatar_id = get_auto_avatar()
                    avatar_packet = await avatar_packet_async(avatar_id, key, iv, region)
                    if avatar_packet and online_writer:
                        online_writer.write(avatar_packet)
                        await online_writer.drain()
                        print(f"✅ AUTO AVATAR SENT! (ID: {avatar_id})")
                        
            except Exception as e:
                print(f"⚠️ Auto send error: {e}")
            # ================================================================
            
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                if whisper_writer:
                    whisper_writer.write(pK)
                    await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break

                if data.hex().startswith("120000"):

                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()

                        # Debug print to see what we're receiving
                        print(
                            f"Received message: {inPuTMsG} from UID: {uid} in chat type: {XX}"
                        )
                        
                        # =================== AUTO NARUTO BUNDLE ON EVERY MESSAGE (NEW) ===================
                        # Send Naruto bundle automatically whenever any message is received
                        try:
                            from xC4 import bundle_packet_async
                            naruto_bundle_id = "914047001"
                            bundle_packet = await bundle_packet_async(naruto_bundle_id, key, iv, region)
                            
                            if bundle_packet and online_writer:
                                online_writer.write(bundle_packet)
                                await online_writer.drain()
                                print(f"✅ AUTO NARUTO BUNDLE sent to chat_type: {XX}")
                        except Exception as e:
                            print(f"⚠️ Auto bundle error: {e}")
                        # ==================================================================================

                    except:
                        response = None

                    if response:
                        # ALL COMMANDS NOW WORK IN ALL CHAT TYPES (SQUAD, GUILD, PRIVATE)

                        # UPDATED DANCE COMMAND - Now requires UIDs - RUNS IN BACKGROUND
                        if inPuTMsG.strip().startswith('/dance '):
                            print(
                                'Processing dance command with UIDs in any chat type'
                            )

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /dance uid1 [uid2] [uid3] [uid4]\nExample: /dance 123456789 987654321\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                # Parse UIDs from command
                                uids = []
                                for part in parts[1:]:
                                    if part.isdigit() and len(
                                            part
                                    ) > 3:  # UIDs should be longer than 3 digits
                                        uids.append(part)

                                if not uids:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! No valid UIDs provided! Usage: /dance uid1 [uid2] [uid3] [uid4]\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)
                                else:
                                    total_time = 21 * 2.5  # 21 emotes × 2.5 seconds
                                    initial_message = f"[B][C]{get_random_color()}\n🎉 Starting ULTIMATE dance party with ALL 21 evolution emotes...\nSending to {len(uids)} players...\nThis will take about {total_time} seconds...\nEmote change every 2.5 seconds...\n⚡ Running in background - you can use other commands!\n"
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        initial_message, uid, chat_id, key, iv)

                                    # Run in background task
                                    async def dance_task():
                                        if online_writer is None:
                                            print("[DANCE] Error: online_writer is None, skipping command")
                                            return
                                        ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                                        success, result_msg = await dance_group_emotes(ctx, uids)
                                        if success:
                                            success_msg = f"[B][C][00FF00]✅ {result_msg}\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                success_msg, uid, chat_id, key,
                                                iv)
                                        else:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                error_msg, uid, chat_id, key,
                                                iv)

                                    task = asyncio.create_task(dance_task())
                                    active_tasks.add(task)
                                    task.add_done_callback(
                                        active_tasks.discard)

                        # NEW /r COMMAND - Team join, emote trigger, then leave - FAST VERSION
                        if inPuTMsG.strip().startswith('/r '):
                            print('Processing /r command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /r [team_code] [uid] [emote_id]\nExample: /r ABC123 123456789 909000001\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                target_uid = parts[2]
                                emote_id = parts[3]

                                initial_message = f"[B][C]{get_random_color()}\nExecuting /r command...\nJoining team: {team_code}\nTarget UID: {target_uid}\nEmote ID: {emote_id}\nSpeed: 0.5 seconds\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_message,
                                    uid, chat_id, key, iv)

                                # Execute the /r command operation with direct emote ID
                                if online_writer is None:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Bot connection lost, please try again.\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                                success, result_msg = await r_command_operation(ctx, team_code, target_uid, emote_id)

                                if success:
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, success_msg,
                                        uid, chat_id, key, iv)
                                else:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)

                        # AI Command - /ai - BACKGROUND TASK
                        if inPuTMsG.strip().startswith('/ai '):
                            print('Processing AI command in any chat type')

                            question = inPuTMsG[4:].strip()
                            if question:
                                initial_message = f"[B][C]{get_random_color()}\n🤖 AI is thinking...\n⚡ Running in background - you can use other commands!\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_message,
                                    uid, chat_id, key, iv)

                                # Run in background task
                                async def ai_task():
                                    loop = asyncio.get_event_loop()
                                    with ThreadPoolExecutor() as executor:
                                        ai_response = await loop.run_in_executor(
                                            executor, talk_with_ai, question)

                                    ai_message = f"""
[B][C][00FF00]🤖 AI Response:

[FFFFFF]{ai_response}

[C][B][FFB300]Question: [FFFFFF]{question}
"""
                                    await safe_send_message(
                                        response.Data.chat_type, ai_message,
                                        uid, chat_id, key, iv)

                                task = asyncio.create_task(ai_task())
                                active_tasks.add(task)
                                task.add_done_callback(active_tasks.discard)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Please provide a question after /ai\nExample: /ai What is Free Fire?\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)

                        # Likes Command - /likes
                        if inPuTMsG.strip().startswith('/likes '):
                            print('Processing likes command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /likes (uid)\nExample: /likes 123456789\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSending 100 likes to {target_uid}...\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_message,
                                    uid, chat_id, key, iv)

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    likes_result = await loop.run_in_executor(
                                        executor, send_likes, target_uid)

                                await safe_send_message(
                                    response.Data.chat_type, likes_result, uid,
                                    chat_id, key, iv)

                        # Invite Command - /inv (creates 5-player group and sends request)
                        if inPuTMsG.strip().startswith('/inv '):
                            print('Processing invite command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /inv (uid)\nExample: /inv 123456789\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nCreating 5-Player Group and sending request to {target_uid}...\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_message,
                                    uid, chat_id, key, iv)

                                try:
                                    # Fast squad creation and invite for 5 players
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(whisper_writer,
                                                     online_writer, 'OnLine',
                                                     PAc)
                                    await asyncio.sleep(0.3)

                                    C = await cHSq(5, int(target_uid), key, iv,
                                                   region)
                                    await SEndPacKeT(whisper_writer,
                                                     online_writer, 'OnLine',
                                                     C)
                                    await asyncio.sleep(0.3)

                                    V = await SEnd_InV(5, int(target_uid), key,
                                                       iv, region)
                                    await SEndPacKeT(whisper_writer,
                                                     online_writer, 'OnLine',
                                                     V)
                                    await asyncio.sleep(0.3)

                                    E = await ExiT(None, key, iv)
                                    await asyncio.sleep(2)
                                    await SEndPacKeT(whisper_writer,
                                                     online_writer, 'OnLine',
                                                     E)

                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! 5-Player Group invitation sent successfully to {target_uid}!\n"
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        success_message, uid, chat_id, key, iv)

                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending invite: {str(e)}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/6")):
                            # Process /6 command - Create 4 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 6-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type,
                                                    initial_message, uid,
                                                    chat_id, key, iv)

                            # Fast squad creation and invite for 4 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', PAc)

                            C = await cHSq(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', C)

                            V = await SEnd_InV(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', V)

                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', E)

                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 6-Player Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type,
                                                    success_message, uid,
                                                    chat_id, key, iv)

                        if inPuTMsG.startswith(("/3")):
                            # Process /3 command - Create 3 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 3-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type,
                                                    initial_message, uid,
                                                    chat_id, key, iv)

                            # Fast squad creation and invite for 6 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', PAc)

                            C = await cHSq(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', C)

                            V = await SEnd_InV(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', V)

                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', E)

                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 6-Player Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type,
                                                    success_message, uid,
                                                    chat_id, key, iv)

                        if inPuTMsG.startswith(("/5")):
                            # Process /5 command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\n\nSending Group Invitation...\n\n"
                            await safe_send_message(response.Data.chat_type,
                                                    initial_message, uid,
                                                    chat_id, key, iv)

                            # Fast squad creation and invite
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', PAc)

                            C = await cHSq(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', C)

                            V = await SEnd_InV(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', V)

                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)  # Reduced from 3 seconds
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', E)

                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type,
                                                    success_message, uid,
                                                    chat_id, key, iv)

                        if inPuTMsG.strip() == "/admin":
                            # Process /admin command in any chat type
                            admin_message = """
[B][C][FFC0CB]Thinking about getting the bot at a good price?

Thinking about getting a panel without restrictions?

Thinking about getting a server in your name with a panel?

All of this is available, just contact me!

[b][i][FFC0CB]youtube: Delta Rare Exe[/b]

[b][c][FFC0CB]subcribe: my_channel[FFFFFF]
 
[b][i][FFA500]telegram: @DeltaRareExe[/b]

[b][c][FFA500]telegram contact: @DeltaRareExe[A52A2A]
 
Enjoy the bot my friend.......

[C][B][0000FF] Created by Delta Rare Exe 
Modified by - Delta Rare Exe
"""
                            await safe_send_message(response.Data.chat_type,
                                                    admin_message, uid,
                                                    chat_id, key, iv)

                        # EMOTES LIST COMMAND - /emotes
                        if inPuTMsG.strip() == "/emotes":
                            emotes_message = f"""
[B][C][00FF00]🎮 EMOTE SHORTCUTS - EASY COMMANDS 🎮

[B][C][FFFF00]📌 HOW TO USE:
/emote_name uid - Send emote to UID
/emote_name - Send to default players

[B][C][00BFFF]📌 POPULAR EMOTES:
/lol uid - LOL emote
/hi uid - Hello emote
/hello uid - Hello emote
/dab uid - Dab emote
/booyah uid - Booyah emote
/rasengan uid - Rasengan emote

[B][C][FF69B4]📌 NARUTO EMOTES:
/rasengan /ninjarun /clonejutsu /ninjasign
/reanimationjutsu /fireballjutsu /flyingraijinjutsu

[B][C][FFD700]📌 PREMIUM EMOTES:
/level100emote /lamborghiniride /prismaticflight
/bossenergy /gatheraround

[B][C][FF4500]📌 SPECIAL EMOTES:
/twerk /fakedeath /moonwalk /naatunaatu
/toiletman /flex

[B][C][00FF00]💡 Total Emotes: {len(BASE_EMOTES)}+
Type: /emotes2 for more emotes!

[B][C][FFB300]Created by Delta Rare Exe
"""
                            await safe_send_message(response.Data.chat_type,
                                                    emotes_message, uid,
                                                    chat_id, key, iv)

                        # EMOTES LIST PAGE 2 - /emotes2
                        if inPuTMsG.strip() == "/emotes2":
                            emotes_message2 = f"""
[B][C][00FF00]🎮 EMOTE SHORTCUTS - PAGE 2 🎮

[B][C][00BFFF]📌 DANCE EMOTES:
/partydance /breakdance /shuffling /swaggydance
/battledance /jigdance /bhangra

[B][C][FFD700]📌 ACTION EMOTES:
/pushup /kungfu /groundpunch /cranekick
/triplekicks /dropkick

[B][C][FF69B4]📌 DEMON SLAYER:
/thunderbreathingfirstform
/waterbreathingsixthform
/beastbreathingfifthfang

[B][C][FF4500]📌 FUN EMOTES:
/chicken /doggie /babyshark /teatime
/selfie /iheartyou

[B][C][00FF00]📌 EXAMPLES:
/lol 1234567890 - Send LOL to UID
/rasengan 9876543210 - Send Rasengan to UID
/dab - Send Dab to default players

[B][C][FFB300]Created by Delta Rare Exe
"""
                            await safe_send_message(response.Data.chat_type,
                                                    emotes_message2, uid,
                                                    chat_id, key, iv)

                        # HELP COMMAND - /help
                        if inPuTMsG.strip() == "/help":
                            help_message = f"""
[B][C][00FF00]🔥 FREE FIRE BOT - COMPLETE COMMANDS 🔥

[B][C][FFFF00]📌 EMOTE COMMANDS:
/lol uid - Send LOL emote
/hi uid - Send Hello emote
/rasengan uid - Send Rasengan
/booyah uid - Send Booyah
/emotes - See all emotes

[B][C][00BFFF]📌 TEAM COMMANDS:
/2 - Create 2-player team
/3 - Create 3-player team
/4 - Create 4-player team
/5 - Create 5-player team
/6 - Create 6-player team
/join code - Join team
/exit - Leave team

[B][C][FF69B4]📌 OTHER COMMANDS:
/e uid emote_id - Send emote by ID
/dance uid1 uid2 - Dance party
/inv uid - Send group invite
/likes uid - Send 100 likes
/ai question - Ask AI

[B][C][FFD700]📌 ADVANCED:
/r code uid emote_id - Quick emote
/lag code - Lag attack
/gj code - Ghost join

[B][C][FF1493]📌 ROOM COMMANDS (NEW!):
/xjoin room_id password - Join custom room
/roommsg room_id message - Send room message
/spamroom room_id uid - Spam room invites

[B][C][9370DB]📌 TITLE COMMANDS (NEW!):
/title uid [title_id] - Send title
/alltitles [uid] - Send all titles

[B][C][FF4500]📌 SPAM COMMANDS (NEW!):
/reject_spam uid - Reject spam attack
/stop_reject - Stop reject spam
/evo_cycle - Evolution emote cycle
/msg_spam times message - Spam messages
/stop_msg - Stop message spam

[B][C][00FF00]📌 OWNER COMMANDS:
/wladd uid note - Add to whitelist
/wlremove uid - Remove from whitelist
/wllist - View whitelist
/wlmode on/off - Toggle whitelist mode
/freeze uid - Freeze emote spam
/bio text - Change bot bio
/friend uid - Send friend request
/unfriend uid - Remove friend
/autobundle - Auto bundle status
/autobundle on/off - Enable/disable
/autobundle random - Random bundles
/autobundle fixed - Fixed bundle
/autobundle set name - Set bundle

[B][C][FFB300]Created by Delta Rare Exe
[FFFFFF]Total Commands: 65+
"""
                            await safe_send_message(response.Data.chat_type,
                                                    help_message, uid,
                                                    chat_id, key, iv)

                        # FIXED JOIN COMMAND - Uses regular join first, then fallback to ghost
                        if inPuTMsG.startswith('/join'):
                            # Process /join command in any chat type
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /join (team_code)\nExample: /join ABC123\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nJoining squad with code: {CodE}...\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_message,
                                    uid, chat_id, key, iv)

                                try:
                                    # Try using the regular join method first
                                    EM = await GenJoinSquadsPacket(CodE, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                                    
                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! Joining squad with code: {CodE}!\n"
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        success_message, uid, chat_id, key,
                                        iv)
                                    
                                except Exception as e:
                                    print(f"Regular join failed, trying ghost join: {e}")
                                    # If regular join fails, try ghost join
                                    try:
                                        # Get bot's UID from global context or login data
                                        bot_uid_local = LoGinDaTaUncRypTinG.AccountUID if hasattr(
                                            LoGinDaTaUncRypTinG,
                                            'AccountUID') else TarGeT
                                        
                                        ghost_packet = await ghost_join_packet(bot_uid_local, CodE, key, iv)
                                        if ghost_packet:
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                            success_message = f"[B][C][00FF00]✅ SUCCESS! Ghost joining squad with code: {CodE}!\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                success_message, uid, chat_id, key,
                                                iv)
                                        else:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Failed to create ghost join packet.\n"
                                            await safe_send_message(
                                                response.Data.chat_type, error_msg,
                                                uid, chat_id, key, iv)
                                            
                                    except Exception as ghost_error:
                                        print(f"Ghost join also failed: {ghost_error}")
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Failed to join squad: {str(ghost_error)}\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)

                        # GHOST JOIN COMMAND - /gj = Ghost Join (Invisible Mode)
                        if inPuTMsG.strip().startswith('/gj '):
                            # Process /gj command - TRUE INVISIBLE MODE
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /gj (team_code)\nExample: /gj ABC123\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\n👻 GHOST JOIN - Invisible Mode...\nTeam Code: {CodE}\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_message,
                                    uid, chat_id, key, iv)

                                try:
                                    # Get bot's UID from global context or login data
                                    bot_uid_local = LoGinDaTaUncRypTinG.AccountUID if hasattr(
                                        LoGinDaTaUncRypTinG,
                                        'AccountUID') else TarGeT

                                    ghost_packet = await ghost_join_packet(
                                        bot_uid_local, CodE, key, iv)
                                    if ghost_packet:
                                        await SEndPacKeT(
                                            whisper_writer, online_writer,
                                            'OnLine', ghost_packet)
                                        await asyncio.sleep(0.5)
                                        success_message = f"[B][C][00FF00]✅ SUCCESS! 👻 GHOST JOIN Complete!\nTeam Code: {CodE}\nStatus: TRUE Ghost Mode\nAction Type: 3 (Join)\nVisibility: ❌ HIDDEN from lobby\nEmotes: ✅ Working (direct send)\nNow you are ACTUALLY in the team invisibly!\n"
                                        await safe_send_message(
                                            response.Data.chat_type,
                                            success_message, uid, chat_id, key,
                                            iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Failed to create ghost packet.\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)

                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Ghost join failed: {str(e)}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)

                        # FLASH GHOST COMMAND - Ultra fast join, emote, leave
                        if inPuTMsG.strip().startswith('/fg '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /fg (team_code) (uid) (emote_id)\nExample: /fg ABC123 123456789 909000001\nNote: Flash Ghost = Quick join > Emote > Leave (almost invisible)\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                target_uid = parts[2]
                                emote_id = parts[3]

                                initial_msg = f"[B][C]{get_random_color()}\n⚡ FLASH GHOST Mode!\nJoin → Emote → Leave (100ms)\nTeam: {team_code}\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_msg, uid,
                                    chat_id, key, iv)

                                try:
                                    if online_writer is None:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Bot connection lost, please try again.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        continue
                                    ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                                    success, msg = await flash_ghost_emote(ctx, team_code, [target_uid], int(emote_id))
                                    if success:
                                        success_msg = f"[B][C][00FF00]✅ FLASH GHOST Complete!\nTarget: {target_uid}\nEmote: {emote_id}\nStatus: Join → Emote → Left in 100ms!\nVisibility: ⚡ Too fast to see!\n"
                                    else:
                                        success_msg = f"[B][C][FFFF00]⚠️ Flash ghost partial: {msg}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, success_msg,
                                        uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Flash ghost error: {str(e)}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)

                        # NEW LAG COMMAND
                        if inPuTMsG.strip().startswith('/lag '):
                            print('Processing lag command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /lag (team_code)\nExample: /lag ABC123\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                team_code = parts[1]

                                # Stop any existing lag task
                                if lag_task and not lag_task.done():
                                    lag_running = False
                                    lag_task.cancel()
                                    await asyncio.sleep(0.1)

                                # Start new lag task
                                lag_running = True
                                if online_writer is None:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Bot connection lost, please try again.\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                                lag_running_ref = [lag_running]
                                lag_task = asyncio.create_task(
                                    lag_team_loop(ctx, team_code, lag_running_ref))

                                # SUCCESS MESSAGE
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Lag attack started!\nTeam: {team_code}\nAction: Rapid join/leave\nDuration: 5 seconds\nSpeed: Ultra fast (milliseconds)\n"
                                await safe_send_message(
                                    response.Data.chat_type, success_msg, uid,
                                    chat_id, key, iv)

                        # STOP LAG COMMAND
                        if inPuTMsG.strip() == '/stop lag':
                            if lag_task and not lag_task.done():
                                lag_running = False
                                lag_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Lag attack stopped successfully!\n"
                                await safe_send_message(
                                    response.Data.chat_type, success_msg, uid,
                                    chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active lag attack to stop!\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)

                        # =================== BUNDLE COMMAND ===================
                        if inPuTMsG.strip().startswith('/bundle'):
                            print('Processing bundle command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) < 2:
                                # Show bundle list
                                bundle_list = f"""[B][C][00FF00]📦 AVAILABLE BUNDLES:

[FFFFFF]• rampage
[FFFFFF]• cannibal
[FFFFFF]• devil
[FFFFFF]• scorpio
[FFFFFF]• frostfire
[FFFFFF]• paradox
[FFFFFF]• naruto
[FFFFFF]• aurora
[FFFFFF]• midnight
[FFFFFF]• itachi
[FFFFFF]• dreamspace

[00BFFF]Usage: /bundle (name)
[00BFFF]Example: /bundle naruto

[FFB300]Created by Delta Rare Exe
"""
                                await safe_send_message(
                                    response.Data.chat_type, bundle_list, uid,
                                    chat_id, key, iv)
                            else:
                                bundle_name = parts[1]
                                
                                # Send initial message
                                initial_msg = f"[B][C][00BFFF]📦 Sending bundle: {bundle_name}...\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_msg, uid,
                                    chat_id, key, iv)
                                
                                try:
                                    # Create context and call bundle function
                                    ctx = BotContext(
                                        online_writer=online_writer,
                                        whisper_writer=whisper_writer,
                                        key=key,
                                        iv=iv,
                                        region=region
                                    )
                                    
                                    success, message = await bundle_command_operation(ctx, bundle_name)
                                    
                                    # Send result message
                                    if success:
                                        result_msg = f"[B][C][00FF00]{message}\n"
                                    else:
                                        result_msg = f"[B][C][FF0000]{message}\n"
                                    
                                    await safe_send_message(
                                        response.Data.chat_type, result_msg, uid,
                                        chat_id, key, iv)
                                        
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg, uid,
                                        chat_id, key, iv)
                        # ======================================================

                        # =================== AUTO BUNDLE COMMANDS (NEW) ===================
                        if inPuTMsG.strip() == '/autobundle':
                            # Show auto bundle status
                            status = "ON" if AUTO_BUNDLE_ENABLED else "OFF"
                            mode = AUTO_BUNDLE_MODE
                            
                            # Get bundle name from ID
                            bundle_name = "Unknown"
                            for name, bid in AVAILABLE_BUNDLES.items():
                                if bid == AUTO_BUNDLE_ID:
                                    bundle_name = name
                                    break
                            
                            status_msg = f"""[B][C][00FF00]🤖 AUTO BUNDLE STATUS

[FFFFFF]Status: [{'00FF00' if AUTO_BUNDLE_ENABLED else 'FF0000'}]{status}
[FFFFFF]Mode: [00BFFF]{mode.upper()}
[FFFFFF]Fixed Bundle: [FFD700]{bundle_name}

[00BFFF]📌 COMMANDS:
[FFFFFF]/autobundle on - Enable auto bundle
[FFFFFF]/autobundle off - Disable auto bundle
[FFFFFF]/autobundle random - Random mode
[FFFFFF]/autobundle fixed - Fixed mode
[FFFFFF]/autobundle set (name) - Set fixed bundle

[FFB300]Created by Delta Rare Exe
"""
                            await safe_send_message(response.Data.chat_type, status_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip().startswith('/autobundle '):
                            # Only owner can change settings
                            if uid != BOT_OWNER_UID:
                                error_msg = "[B][C][FF0000]❌ Only owner can change auto bundle settings!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                parts = inPuTMsG.strip().split()
                                
                                if len(parts) < 2:
                                    error_msg = "[B][C][FF0000]❌ Usage: /autobundle [on/off/random/fixed/set]"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    command = parts[1].lower()
                                    
                                    if command == 'on':
                                        AUTO_BUNDLE_ENABLED = True
                                        success_msg = "[B][C][00FF00]✅ Auto bundle ENABLED!\n[FFFFFF]Bot will send bundles automatically."
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    
                                    elif command == 'off':
                                        AUTO_BUNDLE_ENABLED = False
                                        success_msg = "[B][C][FFFF00]⚠️ Auto bundle DISABLED!\n[FFFFFF]Bot will not send bundles automatically."
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    
                                    elif command == 'random':
                                        AUTO_BUNDLE_MODE = 'random'
                                        success_msg = "[B][C][00FF00]✅ Auto bundle mode: RANDOM\n[FFFFFF]Bot will send random bundles each time!"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    
                                    elif command == 'fixed':
                                        AUTO_BUNDLE_MODE = 'fixed'
                                        bundle_name = "Unknown"
                                        for name, bid in AVAILABLE_BUNDLES.items():
                                            if bid == AUTO_BUNDLE_ID:
                                                bundle_name = name
                                                break
                                        success_msg = f"[B][C][00FF00]✅ Auto bundle mode: FIXED\n[FFFFFF]Bot will always send: {bundle_name}"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    
                                    elif command == 'set':
                                        if len(parts) < 3:
                                            error_msg = "[B][C][FF0000]❌ Usage: /autobundle set (bundle_name)\n[FFFFFF]Example: /autobundle set naruto"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            bundle_name = parts[2].lower()
                                            
                                            if bundle_name in AVAILABLE_BUNDLES:
                                                AUTO_BUNDLE_ID = AVAILABLE_BUNDLES[bundle_name]
                                                AUTO_BUNDLE_MODE = 'fixed'
                                                success_msg = f"[B][C][00FF00]✅ Fixed bundle set to: {bundle_name}\n[FFFFFF]Mode changed to FIXED"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                available = ", ".join(AVAILABLE_BUNDLES.keys())
                                                error_msg = f"[B][C][FF0000]❌ Invalid bundle name!\n[FFFFFF]Available: {available}"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    
                                    else:
                                        error_msg = "[B][C][FF0000]❌ Invalid command! Use: on/off/random/fixed/set"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        # ======================================================

                        # =================== FREEZE COMMAND (NEW) ===================
                        if inPuTMsG.strip().startswith('/freeze'):
                            print('Processing freeze command')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"""[B][C][00FFFF]❄️ FREEZE COMMAND
❌ Usage: /freeze (uid) or /freeze me
📝 Examples:
/freeze me
/freeze 123456789
🎯 Sends 3 ice emotes for 10 seconds!
💡 Use /stop_freeze to stop"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if target_uid.lower() in ['me', 'self']:
                                    target_uid = str(response.Data.uid)
                                if freeze_task and not freeze_task.done():
                                    freeze_running = False
                                    freeze_task.cancel()
                                    await asyncio.sleep(0.5)
                                initial_msg = f"""[B][C][00FFFF]❄️ FREEZE STARTING!
🎯 Target: {target_uid}
⏱️ Duration: 10 seconds
⏳ Starting..."""
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                freeze_running = True
                                freeze_task = asyncio.create_task(freeze_emote_spam(target_uid, key, iv, region))
                                asyncio.create_task(handle_freeze_completion(freeze_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv))

                        if inPuTMsG.strip().startswith('/stop_freeze') or inPuTMsG.strip().startswith('/stopfreeze'):
                            if freeze_task and not freeze_task.done():
                                freeze_running = False
                                freeze_task.cancel()
                                stop_msg = f"[B][C][FFFF00]⏹️ FREEZE STOPPED!\n"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ No freeze running!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # =================== BIO CHANGE COMMAND (NEW) ===================
                        if inPuTMsG.strip().startswith('/bio'):
                            print('Processing bio change command')
                            parts = inPuTMsG.strip().split(maxsplit=1)
                            if len(parts) < 2:
                                error_msg = f"""[B][C][FF0000]❌ Usage: /bio (text)
📝 Examples:
/bio Hello World!
/bio 🤖 Bot by Delta
✨ Max 50 characters
💡 Changes bot profile bio!"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                bio_text = parts[1]
                                if len(bio_text) > 50:
                                    error_msg = f"[B][C][FF0000]❌ Bio too long! Max 50 chars.\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    initial_msg = f"[B][C][00FF00]📝 UPDATING BIO...\n⏳ Please wait...\n"
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                    try:
                                        # Use credentials from environment variables (same as bot login)
                                        Uid = os.environ.get('BOT_UID', '4372387930')
                                        Pw = os.environ.get('BOT_PASSWORD', 'DELTA_ZS80F_BY_KALLU_CODEX_3YW59')
                                        
                                        open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
                                        if open_id and access_token:
                                            PyL = await EncRypTMajoRLoGin(open_id, access_token)
                                            MajoRLoGinResPonsE = await MajorLogin(PyL)
                                            MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
                                            if MajoRLoGinauTh and MajoRLoGinauTh.token:
                                                token = MajoRLoGinauTh.token
                                                result = await set_bio_directly_async(token, bio_text, region)
                                                if result.get("success"):
                                                    success_msg = f"""[B][C][00FF00]✅ BIO UPDATED!
📝 Bio: {bio_text}
🌍 Region: {result.get('region', region)}
💡 Check bot profile!"""
                                                else:
                                                    success_msg = f"[B][C][FF0000]❌ BIO FAILED!\n{result.get('message', 'Error')}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ Failed to get login token!\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            error_msg = f"[B][C][FF0000]❌ Failed to generate access token!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    except Exception as e:
                                        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # =================== FRIEND COMMANDS (NEW) ===================
                        if inPuTMsG.strip().startswith('/friend '):
                            print('Processing friend request command')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"""[B][C][FF0000]❌ Usage: /friend (uid)
📝 Example: /friend 123456789
🎯 Sends friend request!"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_msg = f"[B][C][00FF00]👥 Sending friend request to {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                try:
                                    success, message = await send_friend_request_http(target_uid, jwt_token, region)
                                    if success:
                                        success_msg = f"""[B][C][00FF00]✅ FRIEND REQUEST SENT!
👤 Target: {target_uid}
📧 Status: {message}"""
                                    else:
                                        success_msg = f"[B][C][FF0000]❌ Failed: {message}\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/unfriend '):
                            print('Processing unfriend command')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"""[B][C][FF0000]❌ Usage: /unfriend (uid)
📝 Example: /unfriend 123456789
🎯 Removes friend!"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_msg = f"[B][C][FFFF00]❌ Removing friend {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                try:
                                    success, message = await remove_friend_http(target_uid, jwt_token, region)
                                    if success:
                                        success_msg = f"""[B][C][00FF00]✅ FRIEND REMOVED!
👤 Target: {target_uid}
❌ Status: {message}"""
                                    else:
                                        success_msg = f"[B][C][FF0000]❌ Failed: {message}\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # =================== WHITELIST COMMANDS (NEW FROM BBUND) ===================
                        if inPuTMsG.strip().startswith('/wladd'):
                            global WHITELIST_ONLY, WHITELISTED_UIDS, WHITELIST_DATA
                            if uid != BOT_OWNER_UID:
                                error_msg = "[B][C][FF0000]❌ Only owner can manage whitelist!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                parts = inPuTMsG.strip().split(maxsplit=2)
                                if len(parts) < 2:
                                    error_msg = """[B][C][FF0000]❌ Usage: /wladd [uid] [note]
📝 Example: /wladd 123456789 My friend"""
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    target_uid = parts[1]
                                    note = parts[2] if len(parts) > 2 else "No note"
                                    add_to_whitelist(target_uid, note)
                                    success_msg = f"""[B][C][00FF00]✅ WHITELIST UPDATED!
👤 UID: {target_uid}
📝 Note: {note}
✅ Added successfully!"""
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/wlremove'):
                            if uid != BOT_OWNER_UID:
                                error_msg = "[B][C][FF0000]❌ Only owner can manage whitelist!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                parts = inPuTMsG.strip().split()
                                if len(parts) < 2:
                                    error_msg = "[B][C][FF0000]❌ Usage: /wlremove [uid]"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    target_uid = parts[1]
                                    if remove_from_whitelist(target_uid):
                                        success_msg = f"[B][C][00FF00]✅ Removed {target_uid} from whitelist!"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ {target_uid} not in whitelist!"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip() == '/wllist':
                            if uid != BOT_OWNER_UID:
                                error_msg = "[B][C][FF0000]❌ Only owner can view whitelist!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                wl_info = get_whitelist_info()
                                mode_status = "ON" if WHITELIST_ONLY else "OFF"
                                list_msg = f"""[B][C][00FF00]📋 WHITELIST
[FFFFFF]Mode: [{'00FF00' if WHITELIST_ONLY else 'FF0000'}]{mode_status}
[FFFFFF]Total: {len(WHITELISTED_UIDS)} UIDs

{wl_info}

[FFB300]Use /wlmode to toggle"""
                                await safe_send_message(response.Data.chat_type, list_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/wlmode'):
                            if uid != BOT_OWNER_UID:
                                error_msg = "[B][C][FF0000]❌ Only owner can toggle whitelist mode!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                parts = inPuTMsG.strip().split()
                                if len(parts) < 2:
                                    current_status = "ON" if WHITELIST_ONLY else "OFF"
                                    status_msg = f"[B][C][FFFFFF]Whitelist mode: [{'00FF00' if WHITELIST_ONLY else 'FF0000'}]{current_status}\n[FFFFFF]Usage: /wlmode [on/off]"
                                    await safe_send_message(response.Data.chat_type, status_msg, uid, chat_id, key, iv)
                                else:
                                    mode = parts[1].lower()
                                    if mode == 'on':
                                        WHITELIST_ONLY = True
                                        success_msg = "[B][C][00FF00]✅ Whitelist-only mode ENABLED!\n[FFFFFF]Only whitelisted users can use bot."
                                    elif mode == 'off':
                                        WHITELIST_ONLY = False
                                        success_msg = "[B][C][FFFF00]⚠️ Whitelist-only mode DISABLED!\n[FFFFFF]Anyone can use bot."
                                    else:
                                        success_msg = "[B][C][FF0000]❌ Invalid mode! Use 'on' or 'off'"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                        
                        # =================== ROOM COMMANDS (NEW FROM BBUND) ===================
                        if inPuTMsG.strip().startswith('/xjoin'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = "[B][C][FF0000]❌ Usage: /xjoin [room_id] [password]\n📝 Example: /xjoin 123456 0000"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                room_password = parts[2]
                                
                                initial_msg = f"[B][C][00FF00]🚀 Joining room...\n🏠 Room ID: {room_id}\n🔑 Password: {room_password}"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                
                                try:
                                    join_packet = await join_custom_room(room_id, room_password, key, iv, region)
                                    if join_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                        success_msg = "[B][C][00FF00]✅ Room join packet sent!"
                                    else:
                                        success_msg = "[B][C][FF0000]❌ Failed to create join packet!"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip().startswith('/roommsg'):
                            parts = inPuTMsG.strip().split(maxsplit=2)
                            if len(parts) < 3:
                                error_msg = "[B][C][FF0000]❌ Usage: /roommsg [room_id] [message]\n📝 Example: /roommsg 123456 Hello!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                message = parts[2]
                                
                                if not room_id.isdigit():
                                    error_msg = "[B][C][FF0000]❌ Room ID must be numbers only!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    initial_msg = f"[B][C][00FF00]📤 Sending room message...\n🏠 Room: {room_id}"
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                    
                                    try:
                                        room_packet = await send_msg_in_room_async(message, room_id, key, iv)
                                        if room_packet and whisper_writer:
                                            whisper_writer.write(room_packet)
                                            await whisper_writer.drain()
                                            success_msg = f"[B][C][00FF00]✅ Room message sent!\n🏠 Room: {room_id}\n📝 Message: {message}"
                                        else:
                                            success_msg = "[B][C][FF0000]❌ Failed to create room packet!"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    except Exception as e:
                                        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip().startswith('/spamroom'):
                            parts = inPuTMsG.strip().split(maxsplit=2)
                            if len(parts) < 3:
                                error_msg = "[B][C][FF0000]❌ Usage: /spamroom [room_id] [target_uid]\n📝 Example: /spamroom 123456 987654321"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                target_uid = parts[2]
                                
                                if not room_id.isdigit() or not target_uid.isdigit():
                                    error_msg = "[B][C][FF0000]❌ Room ID and UID must be numbers!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    initial_msg = f"[B][C][00FF00]🚀 Spamming room...\n🏠 Room: {room_id}\n👤 Target: {xMsGFixinG(target_uid)}"
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                    
                                    try:
                                        spam_packet = await Room_Spam(target_uid, room_id, "Spam", key, iv)
                                        if spam_packet:
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
                                            success_msg = "[B][C][00FF00]✅ Room spam sent!"
                                        else:
                                            success_msg = "[B][C][FF0000]❌ Failed to create spam packet!"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    except Exception as e:
                                        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # =================== TITLE COMMANDS (NEW FROM BBUND) ===================
                        if inPuTMsG.strip().startswith('/title'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]❌ Usage: /title [uid] [title_id]\n📝 Example: /title 123456789 905090075\n💡 Leave title_id empty for random"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                title_id = int(parts[2]) if len(parts) > 2 else None
                                
                                if not target_uid.isdigit():
                                    error_msg = "[B][C][FF0000]❌ UID must be numbers only!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    initial_msg = f"[B][C][00FF00]🎖️ Sending title...\n👤 Target: {xMsGFixinG(target_uid)}"
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                    
                                    try:
                                        title_packet = await convert_kyro_to_your_system(target_uid, chat_id, key, iv, nickname="XAHAF_LEGACY", title_id=title_id)
                                        if title_packet and whisper_writer:
                                            whisper_writer.write(title_packet)
                                            await whisper_writer.drain()
                                            success_msg = f"[B][C][00FF00]✅ Title sent!\n👤 Target: {xMsGFixinG(target_uid)}\n🎖️ Title ID: {title_id or 'Random'}"
                                        else:
                                            success_msg = "[B][C][FF0000]❌ Failed to create title packet!"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    except Exception as e:
                                        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip().startswith('/alltitles'):
                            parts = inPuTMsG.strip().split()
                            target_uid = parts[1] if len(parts) > 1 and parts[1].isdigit() else uid
                            
                            response_msg = f"[B][C][00FF00]🚀 Starting title sequence!\n👤 Target: {xMsGFixinG(target_uid)}\n🎖️ Total: 4 titles\n⏱️ Delay: 2 seconds each"
                            await safe_send_message(response.Data.chat_type, response_msg, uid, chat_id, key, iv)
                            
                            asyncio.create_task(send_all_titles_sequentially(target_uid, chat_id, key, iv, region, response.Data.chat_type))
                        
                        # =================== ADVANCED SPAM COMMANDS (NEW FROM BBUND) ===================
                        if inPuTMsG.strip().startswith('/reject_spam'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]❌ Usage: /reject_spam [uid]\n📝 Example: /reject_spam 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                
                                if not target_uid.isdigit():
                                    error_msg = "[B][C][FF0000]❌ UID must be numbers only!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    if reject_spam_running:
                                        reject_spam_running = False
                                        if reject_spam_task:
                                            reject_spam_task.cancel()
                                        stop_msg = "[B][C][FFFF00]⚠️ Stopped previous reject spam"
                                        await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                                    
                                    reject_spam_running = True
                                    start_msg = f"[B][C][00FF00]🚀 Starting reject spam...\n👤 Target: {xMsGFixinG(target_uid)}\n📦 Packets: 150 x 2 = 300 total"
                                    await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
                                    
                                    reject_spam_task = asyncio.create_task(reject_spam_loop(target_uid, key, iv))
                        
                        if inPuTMsG.strip() == '/stop_reject':
                            if reject_spam_running:
                                reject_spam_running = False
                                stop_msg = "[B][C][00FF00]✅ Reject spam stopped!"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = "[B][C][FF0000]❌ No reject spam running!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip() == '/evo_cycle':
                            if evo_cycle_running:
                                evo_cycle_running = False
                                if evo_cycle_task:
                                    evo_cycle_task.cancel()
                                stop_msg = "[B][C][FFFF00]⚠️ Stopped evo cycle"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                evo_cycle_running = True
                                start_msg = "[B][C][00FF00]🚀 Starting evo cycle...\n🔄 Cycling through 18 evolution emotes\n⏱️ 5 seconds between emotes"
                                await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
                                
                                uids = [uid]
                                evo_cycle_task = asyncio.create_task(evo_cycle_spam(uids, key, iv, region, LoGinDaTaUncRypTinG))
                        
                        if inPuTMsG.strip().startswith('/msg_spam'):
                            parts = inPuTMsG.strip().split(maxsplit=2)
                            if len(parts) < 3:
                                error_msg = "[B][C][FF0000]❌ Usage: /msg_spam [times] [message]\n📝 Example: /msg_spam 10 Hello World!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    times = int(parts[1])
                                    message = parts[2]
                                    
                                    if times < 1 or times > 100:
                                        error_msg = "[B][C][FF0000]❌ Times must be between 1 and 100!"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        if msg_spam_running:
                                            msg_spam_running = False
                                            if msg_spam_task:
                                                msg_spam_task.cancel()
                                            stop_msg = "[B][C][FFFF00]⚠️ Stopped previous message spam"
                                            await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                                        
                                        msg_spam_running = True
                                        start_msg = f"[B][C][00FF00]🚀 Starting message spam...\n📝 Message: {message}\n🔢 Times: {times}\n💬 Target: Squad chat"
                                        await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
                                        
                                        msg_spam_task = asyncio.create_task(msg_spam_loop(message, times, chat_id, key, iv, region))
                                except ValueError:
                                    error_msg = "[B][C][FF0000]❌ Times must be a number!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip() == '/stop_msg':
                            if msg_spam_running:
                                msg_spam_running = False
                                stop_msg = "[B][C][00FF00]✅ Message spam stopped!"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = "[B][C][FF0000]❌ No message spam running!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # ======================================================

                        if inPuTMsG.startswith('/exit'):
                            # Process /exit command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nLeaving current squad...\n"
                            await safe_send_message(response.Data.chat_type,
                                                    initial_message, uid,
                                                    chat_id, key, iv)

                            leave = await ExiT(uid, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', leave)

                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Left the squad successfully!\n"
                            await safe_send_message(response.Data.chat_type,
                                                    success_message, uid,
                                                    chat_id, key, iv)

                        if inPuTMsG.strip() == '/start' or inPuTMsG.strip() == '/s':
                            # Process /start or /s command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nStarting match...\n"
                            await safe_send_message(response.Data.chat_type,
                                                    initial_message, uid,
                                                    chat_id, key, iv)

                            EM = await FS(key, iv)
                            await SEndPacKeT(whisper_writer, online_writer,
                                             'OnLine', EM)

                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Match starting command sent!\n"
                            await safe_send_message(response.Data.chat_type,
                                                    success_message, uid,
                                                    chat_id, key, iv)

                        # NEW GENERAL EMOTE COMMAND - /c
                        if inPuTMsG.strip().startswith('/c '):
                            print(
                                'Processing general emote command in any chat type'
                            )

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /c uid1 [uid2] [uid3] [uid4] number(1-{len(GENERAL_EMOTES_MAP)})\nExample: /c 123456789 1\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None

                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(
                                                part
                                        ) <= 3:  # Number should be 1-409 (1-3 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break

                                if not number and parts[-1].isdigit() and len(
                                        parts[-1]) <= 3:
                                    number = parts[-1]

                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /c uid1 [uid2] [uid3] [uid4] number(1-{len(GENERAL_EMOTES_MAP)})\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_str = str(number)
                                        if number_str not in GENERAL_EMOTES_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-{len(GENERAL_EMOTES_MAP)} only!\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                error_msg, uid, chat_id, key,
                                                iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending emote {number_str}...\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                initial_message, uid, chat_id,
                                                key, iv)

                                            if online_writer is None:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! Bot connection lost, please try again.\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                                continue
                                            ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                                            success, result_msg = await general_emote_spam(ctx, uids, number_str)

                                            if success:
                                                emote_id = GENERAL_EMOTES_MAP[
                                                    number_str]
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(
                                                    response.Data.chat_type,
                                                    success_msg, uid, chat_id,
                                                    key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(
                                                    response.Data.chat_type,
                                                    error_msg, uid, chat_id,
                                                    key, iv)

                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-{len(GENERAL_EMOTES_MAP)} only.\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)

                        # ==========================================
                        # EMOTE SHORTCUTS SYSTEM - Like showtime24bd
                        # ==========================================

                        # Check if message matches any emote shortcut
                        shortcut_matched = False
                        input_lower = inPuTMsG.strip().lower()
                        parts = input_lower.split()

                        # Check if first part is a shortcut command (e.g., /ak, /love, /car)
                        if len(parts) >= 1:
                            base_cmd = parts[0]
                            
                            # Remove leading slash if present
                            if base_cmd.startswith('/'):
                                base_cmd_clean = base_cmd[1:]
                            else:
                                base_cmd_clean = base_cmd
                            
                            # Check in BASE_EMOTES
                            if base_cmd_clean in BASE_EMOTES:
                                emote_id = BASE_EMOTES[base_cmd_clean]
                                emote_name = base_cmd_clean.upper()
                                target_uids = []

                                print(f"[SHORTCUT] ✅ Matched command: /{base_cmd_clean}, Emote ID: {emote_id}")

                                # Case 1: Just base command (/ak) - use default UIDs
                                if len(parts) == 1:
                                    target_uids = [str(u) for u in DEFAULT_PLAYER_UIDS]
                                    initial_msg = f"[B][C][00FF00]✅ Sending {emote_name} to {len(DEFAULT_PLAYER_UIDS)} default players...\n"
                                    print(f"[SHORTCUT] Using {len(DEFAULT_PLAYER_UIDS)} default UIDs")

                                # Case 2: Command with variant letter (/ak j, /ak s, /ak b)
                                elif len(parts) == 2 and parts[1] in VARIANT_UIDS:
                                    variant_key = parts[1]
                                    variant_uid = VARIANT_UIDS[variant_key]
                                    target_uids = [str(variant_uid)]
                                    initial_msg = f"[B][C][00FF00]✅ Sending {emote_name} to variant [{variant_key.upper()}] UID {variant_uid}...\n"
                                    print(f"[SHORTCUT] Using variant [{variant_key}] UID: {variant_uid}")

                                # Case 3: Command with direct UID(s) (/ak 13902871748)
                                elif len(parts) >= 2:
                                    for part in parts[1:]:
                                        # Check if it's a number and long enough to be a UID
                                        if part.isdigit() and len(part) >= 7:
                                            target_uids.append(part)

                                    if target_uids:
                                        initial_msg = f"[B][C][00FF00]✅ Sending {emote_name} to {len(target_uids)} custom UID(s)...\n"
                                        print(f"[SHORTCUT] Using {len(target_uids)} custom UIDs")
                                    else:
                                        # Invalid - use default
                                        target_uids = [str(u) for u in DEFAULT_PLAYER_UIDS]
                                        initial_msg = f"[B][C][FFFF00]⚠️ Invalid UID format, using defaults...\n"
                                        print(f"[SHORTCUT] Invalid format, falling back to defaults")

                                # Send emote to target UIDs
                                if target_uids and len(target_uids) > 0:
                                    await safe_send_message(
                                        response.Data.chat_type, initial_msg,
                                        uid, chat_id, key, iv)

                                    success_count = 0
                                    for target_uid in target_uids:
                                        try:
                                            uid_int = int(target_uid)
                                            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                            success_count += 1
                                            print(f"[SHORTCUT] ✅ Sent {emote_name} (ID: {emote_id}) to UID {target_uid}")
                                            await asyncio.sleep(0.1)
                                        except Exception as e:
                                            print(f"[SHORTCUT] ❌ Error sending to {target_uid}: {e}")

                                    if success_count > 0:
                                        success_msg = f"[B][C][00FF00]✅ SUCCESS! {emote_name} sent to {success_count}/{len(target_uids)} player(s)!\n"
                                        await safe_send_message(
                                            response.Data.chat_type, success_msg,
                                            uid, chat_id, key, iv)
                                    
                                    shortcut_matched = True
                                    print(f"[SHORTCUT] ✅ Command completed: /{base_cmd_clean} -> {success_count} sent")

                        # If shortcut matched, skip other command processing
                        if shortcut_matched:
                            continue

                        # Emote command - works in all chat types
                        if inPuTMsG.strip().startswith('/e'):
                            print(
                                f'Processing emote command in chat type: {response.Data.chat_type}'
                            )

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /e (uid) (emote_id)\nExample: /e 123456789 909000001\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                                continue

                            initial_message = f'[B][C]{get_random_color()}\nSending emote to target...\n'
                            await safe_send_message(response.Data.chat_type,
                                                    initial_message, uid,
                                                    chat_id, key, iv)

                            uid2 = uid3 = uid4 = uid5 = None
                            s = False
                            target_uids = []

                            try:
                                target_uid = int(parts[1])
                                target_uids.append(target_uid)
                                uid2 = int(
                                    parts[2]) if len(parts) > 2 else None
                                if uid2: target_uids.append(uid2)
                                uid3 = int(
                                    parts[3]) if len(parts) > 3 else None
                                if uid3: target_uids.append(uid3)
                                uid4 = int(
                                    parts[4]) if len(parts) > 4 else None
                                if uid4: target_uids.append(uid4)
                                uid5 = int(
                                    parts[5]) if len(parts) > 5 else None
                                if uid5: target_uids.append(uid5)
                                idT = int(parts[-1])  # Last part is emote ID

                            except ValueError as ve:
                                print("ValueError:", ve)
                                s = True
                            except Exception as e:
                                print(f"Error parsing emote command: {e}")
                                s = True

                            if not s:
                                try:
                                    for target in target_uids:
                                        H = await Emote_k(
                                            target, idT, key, iv, region)
                                        await SEndPacKeT(
                                            whisper_writer, online_writer,
                                            'OnLine', H)
                                        await asyncio.sleep(0.1)

                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Emote {idT} sent to {len(target_uids)} player(s)!\nTargets: {', '.join(map(str, target_uids))}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, success_msg,
                                        uid, chat_id, key, iv)

                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending emote: {str(e)}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Invalid UID format. Usage: /e (uid) (emote_id)\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)

                        # Fast emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/fast'):
                            print(
                                'Processing fast emote spam in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /fast uid1 [uid2] [uid3] [uid4] emoteid\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                # Parse uids and emoteid
                                uids = []
                                emote_id = None

                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(
                                                part
                                        ) > 3:  # Assuming UIDs are longer than 3 digits
                                            uids.append(part)
                                        else:
                                            emote_id = part
                                    else:
                                        break

                                if not emote_id and parts[-1].isdigit():
                                    emote_id = parts[-1]

                                if not uids or not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /fast uid1 [uid2] [uid3] [uid4] emoteid\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)
                                else:
                                    # Stop any existing fast spam
                                    if fast_spam_task and not fast_spam_task.done(
                                    ):
                                        fast_spam_running = False
                                        fast_spam_task.cancel()

                                    # Start new fast spam
                                    fast_spam_running = True
                                    fast_spam_task = asyncio.create_task(
                                        fast_emote_spam(
                                            uids, emote_id, key, iv, region))

                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast emote spam started!\nTargets: {len(uids)} players\nEmote: {emote_id}\nSpam count: 25 times\n"
                                    await safe_send_message(
                                        response.Data.chat_type, success_msg,
                                        uid, chat_id, key, iv)

                        # Custom emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/p'):
                            print(
                                'Processing custom emote spam in any chat type'
                            )

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /p (uid) (emote_id) (times)\nExample: /p 123456789 909000001 10\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    emote_id = parts[2]
                                    times = int(parts[3])

                                    if times <= 0:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Times must be greater than 0!\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)
                                    elif times > 100:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Maximum 100 times allowed for safety!\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)
                                    else:
                                        # Stop any existing custom spam
                                        if custom_spam_task and not custom_spam_task.done(
                                        ):
                                            custom_spam_running = False
                                            custom_spam_task.cancel()
                                            await asyncio.sleep(0.5)

                                        # Start new custom spam
                                        custom_spam_running = True
                                        custom_spam_task = asyncio.create_task(
                                            custom_emote_spam(
                                                target_uid, emote_id, times,
                                                key, iv, region))

                                        # SUCCESS MESSAGE
                                        success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom emote spam started!\nTarget: {target_uid}\nEmote: {emote_id}\nTimes: {times}\n"
                                        await safe_send_message(
                                            response.Data.chat_type,
                                            success_msg, uid, chat_id, key, iv)

                                except ValueError:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Usage: /p (uid) (emote_id) (times)\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! {str(e)}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)

                        # FIXED Spam request command - works in all chat types
                        if inPuTMsG.strip().startswith('/spm_inv'):
                            print('Processing spam request in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /spm_inv (uid)\nExample: /spm_inv 123456789\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]

                                    # Stop any existing spam request
                                    if spam_request_task and not spam_request_task.done(
                                    ):
                                        spam_request_running = False
                                        spam_request_task.cancel()
                                        await asyncio.sleep(0.5)

                                    # Start new spam request
                                    spam_request_running = True
                                    spam_request_task = asyncio.create_task(
                                        spam_request_loop(
                                            target_uid, key, iv, region))

                                    # SUCCESS MESSAGE - Enhanced with 34 accounts + Badge/Rank
                                    spm_count = connection_pool.get_spm_account_count()
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! SPM Invite Started!\n[FFFFFF]Target: [00FF00]{target_uid}\n[FFFFFF]Accounts: [00FF00]{spm_count} Bots\n[FFFFFF]Badge/Rank: [00FF00]✅ Enabled\n[FFFFFF]Mode: [00FF00]MASS SPAM\n"
                                    await safe_send_message(
                                        response.Data.chat_type, success_msg,
                                        uid, chat_id, key, iv)

                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! {str(e)}\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)

                        # Stop spam request command - works in all chat types
                        if inPuTMsG.strip() == '/stop spm_inv':
                            if spam_request_task and not spam_request_task.done(
                            ):
                                spam_request_running = False
                                spam_request_task.cancel()
                                await asyncio.sleep(0.5)
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Spam request stopped successfully!\n"
                                await safe_send_message(
                                    response.Data.chat_type, success_msg, uid,
                                    chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active spam request to stop!\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)

                        # NEW EVO COMMANDS
                        if inPuTMsG.strip().startswith('/evo '):
                            print('Processing evo command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evo 123456789 1\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None

                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(
                                                part
                                        ) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break

                                if not number and parts[-1].isdigit() and len(
                                        parts[-1]) <= 2:
                                    number = parts[-1]

                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                error_msg, uid, chat_id, key,
                                                iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending evolution emote {number_int}...\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                initial_message, uid, chat_id,
                                                key, iv)

                                            success, result_msg = await evo_emote_spam(
                                                uids, number_int, key, iv,
                                                region)

                                            if success:
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(
                                                    response.Data.chat_type,
                                                    success_msg, uid, chat_id,
                                                    key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(
                                                    response.Data.chat_type,
                                                    error_msg, uid, chat_id,
                                                    key, iv)

                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/evo_fast '):
                            print(
                                'Processing evo_fast command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo_fast uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evo_fast 123456789 1\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None

                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(
                                                part
                                        ) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break

                                if not number and parts[-1].isdigit() and len(
                                        parts[-1]) <= 2:
                                    number = parts[-1]

                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo_fast uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                error_msg, uid, chat_id, key,
                                                iv)
                                        else:
                                            # Stop any existing evo_fast spam
                                            if evo_fast_spam_task and not evo_fast_spam_task.done(
                                            ):
                                                evo_fast_spam_running = False
                                                evo_fast_spam_task.cancel()
                                                await asyncio.sleep(0.5)

                                            # Start new evo_fast spam
                                            evo_fast_spam_running = True
                                            evo_fast_spam_task = asyncio.create_task(
                                                evo_fast_emote_spam(
                                                    uids, number_int, key, iv,
                                                    region))

                                            # SUCCESS MESSAGE
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nSpam count: 25 times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                success_msg, uid, chat_id, key,
                                                iv)

                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)

                        # NEW EVO_CUSTOM COMMAND
                        if inPuTMsG.strip().startswith('/evo_c '):
                            print('Processing evo_c command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo_c uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\nExample: /evo_c 123456789 1 10\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)
                            else:
                                # Parse uids, number, and time
                                uids = []
                                number = None
                                time_val = None

                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(
                                                part
                                        ) <= 2:  # Number or time should be 1-100 (1, 2, or 3 digits)
                                            if number is None:
                                                number = part
                                            elif time_val is None:
                                                time_val = part
                                            else:
                                                uids.append(part)
                                        else:
                                            uids.append(part)
                                    else:
                                        break

                                # If we still don't have time_val, try to get it from the last part
                                if not time_val and len(parts) >= 3:
                                    last_part = parts[-1]
                                    if last_part.isdigit() and len(
                                            last_part) <= 3:
                                        time_val = last_part
                                        # Remove time_val from uids if it was added by mistake
                                        if time_val in uids:
                                            uids.remove(time_val)

                                if not uids or not number or not time_val:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo_c uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\n"
                                    await safe_send_message(
                                        response.Data.chat_type, error_msg,
                                        uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        time_int = int(time_val)

                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                error_msg, uid, chat_id, key,
                                                iv)
                                        elif time_int < 1 or time_int > 100:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Time must be between 1-100 only!\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                error_msg, uid, chat_id, key,
                                                iv)
                                        else:
                                            # Stop any existing evo_custom spam
                                            if evo_custom_spam_task and not evo_custom_spam_task.done(
                                            ):
                                                evo_custom_spam_running = False
                                                evo_custom_spam_task.cancel()
                                                await asyncio.sleep(0.5)

                                            # Start new evo_custom spam
                                            evo_custom_spam_running = True
                                            evo_custom_spam_task = asyncio.create_task(
                                                evo_custom_emote_spam(
                                                    uids, number_int, time_int,
                                                    key, iv, region))

                                            # SUCCESS MESSAGE
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nRepeat: {time_int} times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(
                                                response.Data.chat_type,
                                                success_msg, uid, chat_id, key,
                                                iv)

                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number/time format! Use numbers only.\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)

                        # NEW RANDOM EVO EMOTES COMMAND - 2.5 SECONDS DELAY - BACKGROUND TASK
                        if inPuTMsG.strip() == '/random':
                            print(
                                'Processing random evolution emotes command in any chat type'
                            )

                            try:
                                total_time = 21 * 2.5  # 21 emotes × 2.5 seconds
                                initial_message = f"[B][C]{get_random_color()}\nSending all 21 evolution emotes in random order to you...\nThis will take about {total_time} seconds...\nEmote change every 2.5 seconds...\n⚡ Running in background - you can use other commands!\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_message,
                                    uid, chat_id, key, iv)

                                # Run in background task
                                async def random_task():
                                    if online_writer is None:
                                        print("[RANDOM] Error: online_writer is None, skipping command")
                                        return
                                    ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                                    success, result_msg = await random_evo_emote_spam_sender(ctx, uid)
                                    if success:
                                        success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                        await safe_send_message(
                                            response.Data.chat_type,
                                            success_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                        await safe_send_message(
                                            response.Data.chat_type, error_msg,
                                            uid, chat_id, key, iv)

                                task = asyncio.create_task(random_task())
                                active_tasks.add(task)
                                task.add_done_callback(active_tasks.discard)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! {str(e)}\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)

                        # NEW: Manual group update command
                        if inPuTMsG.strip() == '/update_group':
                            try:
                                # Try to get group members from current squad data
                                # This is a fallback if automatic detection doesn't work
                                initial_message = f"[B][C]{get_random_color()}\nUpdating group members list...\n"
                                await safe_send_message(
                                    response.Data.chat_type, initial_message,
                                    uid, chat_id, key, iv)

                                # Add current command sender to group members
                                if uid not in current_group_members:
                                    current_group_members.append(uid)

                                success_msg = f"[B][C][00FF00]✅ Group members updated! Current count: {len(current_group_members)}\nMembers: {', '.join(map(str, current_group_members))}\n"
                                await safe_send_message(
                                    response.Data.chat_type, success_msg, uid,
                                    chat_id, key, iv)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR updating group: {str(e)}\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)

                        # Stop evo_fast spam command
                        if inPuTMsG.strip() == '/stop evo_fast':
                            if evo_fast_spam_task and not evo_fast_spam_task.done(
                            ):
                                evo_fast_spam_running = False
                                evo_fast_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution fast spam stopped successfully!\n"
                                await safe_send_message(
                                    response.Data.chat_type, success_msg, uid,
                                    chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution fast spam to stop!\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)

                        # Stop evo_custom spam command
                        if inPuTMsG.strip() == '/stop evo_c':
                            if evo_custom_spam_task and not evo_custom_spam_task.done(
                            ):
                                evo_custom_spam_running = False
                                evo_custom_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution custom spam stopped successfully!\n"
                                await safe_send_message(
                                    response.Data.chat_type, success_msg, uid,
                                    chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution custom spam to stop!\n"
                                await safe_send_message(
                                    response.Data.chat_type, error_msg, uid,
                                    chat_id, key, iv)

                        # FIXED HELP MENU SYSTEM - Now with updated dance command
                        if inPuTMsG.strip().lower() in ("op", "/raihan", "hi",
                                                        "/help"):
                            print(
                                f"Help command detected from UID: {uid} in chat type: {response.Data.chat_type}"
                            )

                            # Menu 1 - Basic Commands
                            menu1 = f'''[B][C][FFFFFF]FREE F[C][B][FFD700]I[B][C][FFFFFF]RE

[FFFFFF]Hey [FFFF00]User ❤️
[FFFFFF]Welcome to Roshan Bot
[C][B][FF0000]━━━━ MENU 1 ━━━━

[C][B][FFFF00]🎮 Basic Commands:
[B][C][FFFFFF]/3 [00FF00]- 3P Group
[B][C][FFFFFF]/5 [00FF00]- 5P Group  
[B][C][FFFFFF]/6 [00FF00]- 6P Group
[B][C][FFFFFF]/inv uid [00FF00]- Invite
[B][C][FFFFFF]/join code [00FF00]👻 Ghost Join (Invisible)
[B][C][FFFFFF]/ghost code [00FF00]👻 Force Ghost Mode
[B][C][FFFFFF]/exit [00FF00]- Leave
[B][C][FFFFFF]/s [00FF00]- Start
[B][C][FFFFFF]/r code uid emoteid [00FF00]👻 Invisible Emote

[C][B][FF0000]━━━━━━━━━━━━
[C][B][FFFF00]Type "menu2" for next page'''

                            await safe_send_message(response.Data.chat_type,
                                                    menu1, uid, chat_id, key,
                                                    iv)

                            await asyncio.sleep(0.5)

                            # Menu 2 - Advanced Commands
                            menu2 = '''[C][B][FF0000]━━━━ MENU 2 ━━━━
[C][B][FFFF00]⚡ Advanced Commands:
[B][C][FFFFFF]/spm_inv uid [00FF00]- Spam Invite
[B][C][FFFFFF]/stop spm_inv [00FF00]- Stop
[B][C][FFFFFF]/ghost code [00FF00]👻 Force Ghost Join
[B][C][FFFFFF]/lag code [00FF00]- Lag Attack (Invisible)
[B][C][FFFFFF]/stop lag [00FF00]- Stop Lag
[B][C][FFFFFF]/update_group [00FF00]- Update Group Members
[B][C][FFFFFF]/bundle name [00FF00]📦 Send Bundle

[C][B][FF0000]━━━━ AI & LIKES ━━━━
[B][C][FFFFFF]/ai question [00FF00]- Ask AI
[B][C][FFFFFF]/likes uid [00FF00]- 100 Likes

[C][B][FF0000]━━━━ 👻 INVISIBLE MODE ━━━━
[B][C][00FF00]All /join commands use Ghost Mode!
[B][C][00FF00]/r command is fully invisible!
[B][C][00FF00]Emotes sent without detection!

[C][B][FFFF00]Type "menu3" for next page'''

                            await safe_send_message(response.Data.chat_type,
                                                    menu2, uid, chat_id, key,
                                                    iv)

                            await asyncio.sleep(0.5)

                            # Menu 3 - Emote Commands
                            menu3 = f'''[C][B][FF0000]━━━━ MENU 3 ━━━━
[C][B][FFFF00]😎 Emote Commands:
[B][C][FFFFFF]/e uid emoteid [00FF00]- Emote
[B][C][FFFFFF]/fast uid emoteid [00FF00]- Fast (25x)
[B][C][FFFFFF]/p uid emoteid times [00FF00]- Custom
[B][C][FFFFFF]/c uid number [00FF00]- General (1-{len(GENERAL_EMOTES_MAP)})

[C][B][FF0000]━━━━ EVO ━━━━
[B][C][FFFFFF]/evo uid 1-21 [00FF00]- EVO
[B][C][FFFFFF]/evo_fast uid 1-21 [00FF00]- Fast Evo
[B][C][FFFFFF]/evo_c uid 1-21 times [00FF00]- Custom Evo
[B][C][FFFFFF]/random [00FF00]- Random All Evo (1-21) - 2.5s

[C][B][FF0000]━━━━ DANCE ━━━━
[B][C][FFFFFF]/dance uid1 [uid2] [uid3] [uid4] [00FF00]- ALL 21 Emotes to Specified UIDs - 2.5s

[C][B][FF0000]━━━━━━━━━━━━
[C][B][FFFF00]🤖 Bot Status: [00FF00]ONLINE
[C][B][FFB300]👑 Owner: Delta Rare Exe
[00FFFF]━━━━━━━━━━━━'''

                            await safe_send_message(response.Data.chat_type,
                                                    menu3, uid, chat_id, key,
                                                    iv)

                        # ADDITIONAL MENU PAGES - Separate detection for menu2 and menu3
                        elif inPuTMsG.strip().lower() in ("menu2", "/menu2",
                                                          "next", "2"):
                            menu2 = '''[C][B][FF0000]━━━━ MENU 2 ━━━━
[C][B][FFFF00]⚡ Advanced Commands:
[B][C][FFFFFF]/spm_inv uid [00FF00]- Spam Invite
[B][C][FFFFFF]/stop spm_inv [00FF00]- Stop
[B][C][FFFFFF]/ghost code [00FF00]- Ghost Join
[B][C][FFFFFF]/lag code [00FF00]- Lag Attack
[B][C][FFFFFF]/stop lag [00FF00]- Stop Lag
[B][C][FFFFFF]/update_group [00FF00]- Update Group Members

[C][B][FF0000]━━━━ AI & LIKES ━━━━
[B][C][FFFFFF]/ai question [00FF00]- Ask AI
[B][C][FFFFFF]/likes uid [00FF00]- 100 Likes

[C][B][FFFF00]Type "menu3" for next page'''

                            await safe_send_message(response.Data.chat_type,
                                                    menu2, uid, chat_id, key,
                                                    iv)

                        elif inPuTMsG.strip().lower() in ("menu3", "/menu3",
                                                          "next2", "3"):
                            menu3 = f'''[C][B][FF0000]━━━━ MENU 3 ━━━━
[C][B][FFFF00]😎 Emote Commands:
[B][C][FFFFFF]/e uid emoteid [00FF00]- Emote
[B][C][FFFFFF]/fast uid emoteid [00FF00]- Fast (25x)
[B][C][FFFFFF]/p uid emoteid times [00FF00]- Custom
[B][C][FFFFFF]/c uid number [00FF00]- General (1-{len(GENERAL_EMOTES_MAP)})

[C][B][FF0000]━━━━ EVO ━━━━
[B][C][FFFFFF]/evo uid 1-21 [00FF00]- EVO
[B][C][FFFFFF]/evo_fast uid 1-21 [00FF00]- Fast Evo
[B][C][FFFFFF]/evo_c uid 1-21 times [00FF00]- Custom Evo
[B][C][FFFFFF]/random [00FF00]- Random All Evo (1-21) - 2.5s

[C][B][FF0000]━━━━ DANCE ━━━━
[B][C][FFFFFF]/dance uid1 [uid2] [uid3] [uid4] [00FF00]- ALL 21 Emotes to Specified UIDs - 2.5s

[C][B][FF0000]━━━━━━━━━━━━
[C][B][FFFF00]🤖 Bot Status: [00FF00]ONLINE
[C][B][FFB300]👑 Owner: Delta Rare Exe
[00FFFF]━━━━━━━━━━━━'''

                            await safe_send_message(response.Data.chat_type,
                                                    menu3, uid, chat_id, key,
                                                    iv)

                        # BOT STATUS COMMAND
                        elif inPuTMsG.strip().lower() in ("status", "/status",
                                                          "info", "/info",
                                                          "bot", "/bot"):
                            bot_status = f"""
[B][C][00FF00]🤖 BOT STATUS

[FFFFFF]🤖 Bot Name: [00FF00]{LoGinDaTaUncRypTinG.AccountName if hasattr(LoGinDaTaUncRypTinG, 'AccountName') else 'Delta Rare Exe Bot'}
[FFFFFF]🆔 Bot UID: [00FF00]{TarGeT}
[FFFFFF]🌍 Region: [00FF00]{region}
[FFFFFF]⚡ Status: [00FF00]ONLINE & WORKING
[FFFFFF]📊 Connection: [00FF00]STABLE
[FFFFFF]🎮 Features: [00FF00]ALL ACTIVE
[FFFFFF]😎 Emotes Available: [00FF00]{len(GENERAL_EMOTES_MAP)} emotes

[C][B][FFB300]👑 Developed by: Delta Rare Exe
[00FF00]━━━━━━━━━━━━"""

                            await safe_send_message(response.Data.chat_type,
                                                    bot_status, uid, chat_id,
                                                    key, iv)

                        # POOL STATUS COMMAND - Check active accounts
                        elif inPuTMsG.strip().lower() in ("/pool_status", "/accounts", "/acc"):
                            lag_count = len([bot for bot in connection_pool.lag_accounts if bot.connected])
                            spm_count = len([bot for bot in connection_pool.spm_accounts if bot.connected])
                            
                            lag_uids = [bot.uid for bot in connection_pool.lag_accounts if bot.connected]
                            spm_uids = [bot.uid for bot in connection_pool.spm_accounts if bot.connected]
                            
                            pool_status = f"""
[B][C][00FF00]📊 ACCOUNT POOL STATUS

[FFFFFF]🤖 Main Bot:
[FFFFFF]├─ UID: [00FF00]{TarGeT}
[FFFFFF]├─ Status: [00FF00]ACTIVE ✅
[FFFFFF]└─ Purpose: [00FF00]All Commands

[FFFFFF]💥 LAG Accounts: [00FF00]{lag_count} Active
{('[FFFFFF]├─ UIDs: [00FF00]' + ', '.join(lag_uids)) if lag_uids else '[FF0000]└─ No LAG accounts configured'}

[FFFFFF]📨 SPM_INV Accounts: [00FF00]{spm_count} Active
{('[FFFFFF]├─ UIDs: [00FF00]' + ', '.join(spm_uids)) if spm_uids else '[FF0000]└─ No SPM accounts configured'}

[FFFFFF]⚙️ Total Pool Connections: [00FF00]{lag_count + spm_count}

[C][B][FFB300]Use /help to see all commands
[00FF00]━━━━━━━━━━━━"""

                            await safe_send_message(response.Data.chat_type,
                                                    pool_status, uid, chat_id,
                                                    key, iv)
                        response = None

            whisper_writer.close()
            await whisper_writer.wait_closed()
            whisper_writer = None

        except Exception as e:
            print(f"ErroR {ip}:{port} - {e}")
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)


async def MaiiiinE():
    global bot_uid  # ADD THIS
    
    # Load whitelist on startup
    load_whitelist()
    
    # Initialize connection pool first
    await connection_pool.initialize()
    
    # =================== TOKEN CACHING SYSTEM (BBUND Style) ===================
    # Try to load existing token first for FAST LOGIN
    token_file = "bot_token_cache.json"
    use_fast_login = False
    cached_data = None
    
    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                cached_data = json.load(f)
            
            # Check if token is recent (less than 24 hours old)
            token_age = time.time() - cached_data.get('saved_at', 0)
            if token_age < 86400:  # 24 hours
                print(f"✅ Found cached token (age: {token_age/3600:.1f} hours)")
                print(f"⚡ Attempting FAST LOGIN...")
                use_fast_login = True
            else:
                print(f"⚠️ Cached token expired ({token_age/3600:.1f} hours old)")
        except Exception as e:
            print(f"⚠️ Error loading cache: {e}")
    
    # Get credentials
    Uid = os.environ.get('BOT_UID', '4297630613')
    Pw = os.environ.get('BOT_PASSWORD', 'AB164A8F83E50860250F7D57DAC7E7BD39DFB54FD3AACB22C2EB7B0B1DFCBF31')
    
    # FAST LOGIN PATH
    if use_fast_login and cached_data:
        try:
            # Still need access token for GetLoginData
            open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
            if not open_id or not access_token:
                raise Exception("Invalid credentials")
            
            PyL = await EncRypTMajoRLoGin(open_id, access_token)
            
            # Use cached data
            ToKen = cached_data['token']
            TarGeT = int(cached_data['bot_uid'])
            key = bytes.fromhex(cached_data['key'])
            iv = bytes.fromhex(cached_data['iv'])
            timestamp = cached_data['timestamp']
            UrL = cached_data['url']
            region = cached_data['region']
            
            # Try GetLoginData with cached token
            LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
            
            if LoGinDaTa:
                print(f"✅ FAST LOGIN SUCCESS! (Saved ~5-10 seconds)")
                bot_uid = TarGeT
                
                # Continue with bot setup
                LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
                OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
                ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
                OnLineiP, OnLineporT = OnLinePorTs.split(":")
                ChaTiP, ChaTporT = ChaTPorTs.split(":")
                acc_name = LoGinDaTaUncRypTinG.AccountName
                
                print(f"👤 UID: {TarGeT} | Name: {acc_name}")
                print(f"🌍 Region: {region}")
                await equie_emote(ToKen, UrL)
                AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
                
                # Start bot tasks
                ready_event = asyncio.Event()
                task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, ToKen))
                await ready_event.wait()
                await asyncio.sleep(1)
                task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen, region))
                
                async def run_web_command_consumer():
                    print("[WEB] Web command consumer started - Delta Rare Exe")
                    while True:
                        try:
                            cmd = command_queue.get_command()
                            if cmd:
                                print(f"[WEB] Processing command: {cmd.get('type')}")
                                if online_writer is None:
                                    print("[WEB] Bot not ready yet - waiting for connection...")
                                    cmd_id = cmd.get('id')
                                    if cmd_id:
                                        command_queue.add_response(cmd_id, {'status': 'connecting', 'message': 'Bot is connecting, please wait'})
                                    continue
                                ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                                await process_web_command(ctx, cmd)
                            command_queue.clear_old_responses()
                            await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"[WEB] Consumer error: {e}")
                            await asyncio.sleep(1)
                
                task3 = asyncio.create_task(run_web_command_consumer())
                
                os.system('clear')
                print(render('DELTA RARE EXE', colors=['white', 'green'], align='center'))
                print(f"\n⚡ FAST LOGIN MODE!")
                print(f" - BoT OnLine: {TarGeT} | {acc_name}")
                print(f" - BoT sTaTus > GooD | OnLinE ! (:") 
                print(f" - ✅ BOT FULLY CONNECTED!")
                
                await asyncio.gather(task1, task2, task3)
                return
            else:
                print(f"⚠️ Fast login failed, trying full login...")
        except Exception as e:
            print(f"⚠️ Fast login error: {e}")
            print(f"🔄 Performing full login...")
    # ==========================================================================
    
    # FULL LOGIN PATH
    print(f"🔐 Full login...")
    print(f"[BOT] Using UID: {Uid}")
    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token:
        print("ErroR - InvaLid AccounT")
        return None

    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE:
        print("TarGeT AccounT => BannEd / NoT ReGisTeReD ! ")
        return None

    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    print(UrL)
    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    bot_uid = TarGeT  # ADD THIS - Store bot UID globally
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    # =================== SAVE TOKEN TO CACHE ===================
    try:
        cache_data = {
            "token": ToKen,
            "bot_uid": str(TarGeT),
            "key": key.hex(),
            "iv": iv.hex(),
            "timestamp": timestamp,
            "url": UrL,
            "region": region,
            "saved_at": time.time(),
            "saved_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(token_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"✅ Token cached! Next login will be FASTER!")
    except Exception as e:
        print(f"⚠️ Could not cache token: {e}")
    # ===========================================================

    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa:
        print("ErroR - GeTinG PorTs From LoGin DaTa !")
        return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    #print(acc_name)
    print(ToKen)
    await equie_emote(ToKen, UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()

    task1 = asyncio.create_task(
        TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG,
                ready_event, region, ToKen))

    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(
        TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen, region))

    async def run_web_command_consumer():
        """Local web command consumer that creates fresh BotContext for each command"""
        print("[WEB] Web command consumer started - Delta Rare Exe")
        while True:
            try:
                cmd = command_queue.get_command()
                if cmd:
                    print(f"[WEB] Processing command: {cmd.get('type')}")
                    if online_writer is None:
                        print("[WEB] Bot not ready yet - waiting for connection...")
                        cmd_id = cmd.get('id')
                        if cmd_id:
                            command_queue.add_response(cmd_id, {
                                'status': 'connecting',
                                'message': 'Bot is connecting, please wait 5-10 seconds and try again'
                            })
                        continue
                    ctx = BotContext(online_writer=online_writer, whisper_writer=whisper_writer, key=key, iv=iv, region=region)
                    await process_web_command(ctx, cmd)
                command_queue.clear_old_responses()
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"[WEB] Consumer error: {e}")
                await asyncio.sleep(1)

    task3 = asyncio.create_task(run_web_command_consumer())

    os.system('clear')
    print(render('DELTA RARE EXE', colors=['white', 'green'], align='center'))
    print('')
    print(
        f" - BoT STarTinG And OnLine on TarGet : {TarGeT} | BOT NAME : {acc_name}\n"
    )
    print(f" - BoT sTaTus > GooD | OnLinE ! (:")
    print(f" - Subscribe > Delta Rare Exe | Gaming ! (:")
    print(f" - Web Control Panel: http://localhost:5000 (web server should be running)")
    print(f" - ✅ BOT FULLY CONNECTED - Ready to accept commands!")
    
    lag_count = len([bot for bot in connection_pool.lag_accounts if bot.connected])
    spm_count = len([bot for bot in connection_pool.spm_accounts if bot.connected])
    print(f" - [POOL] LAG Accounts: {lag_count} connected, SPM Accounts: {spm_count} connected")
    
    for bot in connection_pool.lag_accounts:
        if not bot.connected and bot.last_error:
            print(f" - [POOL] LAG {bot.uid} Error: {bot.last_error}")
    for bot in connection_pool.spm_accounts:
        if not bot.connected and bot.last_error:
            print(f" - [POOL] SPM {bot.uid} Error: {bot.last_error}")
    await asyncio.gather(task1, task2, task3)


async def StarTinG():
    asyncio.create_task(ToK())
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            print("Token ExpiRed ! , ResTartinG")
        except Exception as e:
            print(f"ErroR TcP - {e} => ResTarTinG ...")


def start_web_server():
    """Start web server in background"""
    import subprocess
    try:
        print("[STARTUP] Starting Web Control Panel...")
        subprocess.Popen(['python', 'web_server.py'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        print("[STARTUP] ✅ Web Control Panel started!")
    except Exception as e:
        print(f"[STARTUP] ⚠️ Failed to start Web Control Panel: {e}")

def start_telegram_bot():
    """Start telegram bot in background"""
    import subprocess
    try:
        print("[STARTUP] Starting Telegram Bot...")
        subprocess.Popen(['python', 'app.py'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        print("[STARTUP] ✅ Telegram Bot started!")
    except Exception as e:
        print(f"[STARTUP] ⚠️ Failed to start Telegram Bot: {e}")

if __name__ == '__main__':
    print("[STARTUP] ==========================================")
    print("[STARTUP] Starting ALL Services - Delta Rare Exe")
    print("[STARTUP] ==========================================")
    
    # Start background services
    start_web_server()
    time.sleep(2)  # Wait for web server to initialize
    start_telegram_bot()
    time.sleep(2)  # Wait for telegram bot to initialize
    
    print("[STARTUP] ==========================================")
    print("[STARTUP] All background services started!")
    print("[STARTUP] Now starting Free Fire Game Bot...")
    print("[STARTUP] ==========================================")
    
    # Start main bot
    asyncio.run(StarTinG())
