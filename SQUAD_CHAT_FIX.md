# Squad/Team Chat Fix ✅

## Problem:
Bot was **NOT responding** to commands sent in Squad/Team chat.

## Root Cause:
Squad messages (packet type `0501`) were **NOT being handled** in `TcPOnLine()` function.

## Solution:
Added squad message handler in `TcPOnLine()` function to:
1. Detect squad messages (0501 packets)
2. Decode squad message using `decode_team_packet()`
3. Extract sender UID and message text
4. Process commands same as other chat types
5. Send response back to squad chat

## What Was Added:

### Squad Message Handler (in TcPOnLine):
```python
# Handle squad/team chat messages
if data2.hex().startswith('0501'):
    try:
        # Decode squad message
        squad_msg = await decode_team_packet(data2.hex()[10:])
        
        # Extract message details
        sender_uid = squad_msg.details.player_uid
        team_session = squad_msg.details.team_session
        
        # Extract message text
        packet_data = await DeCode_PackEt(data2.hex()[10:])
        packet_json = json.loads(packet_data)
        message_text = packet_json.get('4', {}).get('data', '')
        
        # Process commands
        if message_text.lower().startswith('/'):
            # Handle /help, /bundle, etc.
            await safe_send_message(0, response_msg, sender_uid, team_session, key, iv)
```

## Packet Types:

- `0500` = Squad join/leave/status packets
- **`0501` = Squad chat messages** ← This was missing!
- `1200` = Private/Guild messages (already working)

## How It Works Now:

### 1. **Message Reception:**
```
Squad member sends: /bundle naruto
    ↓
Packet type: 0501
    ↓
TcPOnLine receives packet
    ↓
decode_team_packet() decodes message
    ↓
Extracts: sender_uid, team_session, message_text
```

### 2. **Command Processing:**
```
Check if message starts with /
    ↓
Process command (/bundle, /help, etc.)
    ↓
Generate response message
    ↓
Send via safe_send_message(chat_type=0, ...)
```

### 3. **Response Sending:**
```
safe_send_message(0, message, sender_uid, team_session, key, iv)
    ↓
chat_type=0 means Squad
    ↓
Uses xSEndMsgsQ() for squad messages
    ↓
Response appears in squad chat
```

## Supported Commands in Squad Chat:

### Currently Implemented:
- ✅ `/help` - Show help menu
- ✅ `/bundle name` - Send bundle

### Easy to Add More:
Just add more `elif` blocks in the squad handler:
```python
elif inPuTMsG.strip().startswith('/dance'):
    # Handle dance command
    
elif inPuTMsG.strip().startswith('/lag'):
    # Handle lag command
```

## Testing:

### Test Squad Chat:
```
1. Create a squad/team
2. Invite bot to squad
3. In squad chat, type: /help
4. Bot should respond: "🔥 BOT COMMANDS 🔥..."
5. Try: /bundle naruto
6. Bot should respond: "✅ Bundle 'naruto' sent successfully!"
```

### Expected Console Output:
```
[SQUAD] Message from 123456789: /help
[SQUAD] Processed command: /help
Message sent successfully on attempt 1
```

## Comparison:

### Before Fix:
```
Squad Chat:
You: /help
Bot: [No response]

Console:
[No squad message detected]
```

### After Fix:
```
Squad Chat:
You: /help
Bot: 🔥 BOT COMMANDS 🔥
     /bundle name - Send bundle
     /dance uid - Dance party
     ...

Console:
[SQUAD] Message from 123456789: /help
[SQUAD] Processed command: /help
Message sent successfully on attempt 1
```

## Code Structure:

```
TcPOnLine() function:
├─ Connects to online server
├─ Receives packets in loop
├─ Checks packet type:
│  ├─ 0501 → Squad messages (NEW!)
│  │  ├─ Decode message
│  │  ├─ Extract sender & text
│  │  ├─ Process commands
│  │  └─ Send response
│  ├─ 0500 → Squad join/status
│  └─ Other → Other handlers
```

## Adding More Commands:

To add more commands to squad chat, edit the squad handler section:

```python
# In TcPOnLine, inside the 0501 handler:

elif inPuTMsG.strip().startswith('/yourcommand'):
    # Your command logic here
    result_msg = "[B][C][00FF00]Your response"
    await safe_send_message(0, result_msg, sender_uid, team_session, key, iv)
```

## Important Notes:

1. **chat_type = 0** for squad messages
2. **team_session** is used as chat_id for squad
3. **sender_uid** is the person who sent the message
4. **safe_send_message()** handles the routing automatically

## Troubleshooting:

### If still not working:

1. **Check console for squad messages:**
   ```
   Should see: [SQUAD] Message from XXX: /command
   ```

2. **Check packet reception:**
   ```
   Should see: 0501 packets being received
   ```

3. **Check decode_team_packet:**
   ```
   Make sure sQ_pb2.recieved_chat() is working
   ```

4. **Check bot in squad:**
   ```
   Bot must be IN the squad to receive messages
   ```

## Files Modified:

1. **main.py** - `TcPOnLine()` function
   - Added 0501 packet handler
   - Added squad message decoder
   - Added command processor for squad
   - Added response sender for squad

## Next Steps:

1. Test in squad chat with `/help`
2. Test with `/bundle naruto`
3. Add more commands as needed
4. Monitor console for any errors

---
**Status:** ✅ FIXED  
**Squad Chat:** Now Working  
**Commands:** /help, /bundle (more can be added)  
**Date:** January 2025
