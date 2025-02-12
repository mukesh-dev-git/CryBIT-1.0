from telethon import TelegramClient, events
from utility import load_config, save_to_mongodb, fetch_from_mongodb
from scam_detection import analyze_message
import asyncio
import time

# Load configuration
config = load_config()
api_id = config["telegram"]["api_id"]
api_hash = config["telegram"]["api_hash"]

# ✅ Use only a single user session (No bot token)
tg_client = TelegramClient('user_session', api_id, api_hash)

async def monitor_channels():
    """Fetch monitored channels from DB and join them."""
    channels = fetch_from_mongodb("monitored_channels")
    for channel in channels:
        try:
            entity = await tg_client.get_entity(channel["channel_id"])  # ✅ Use get_entity() for full details
            print(f"✅ Monitoring: {entity.title if hasattr(entity, 'title') else 'Unknown Channel'}")
        except Exception as e:
            print(f"⚠️ Error: Cannot find entity for {channel['channel_id']} - {e}")

@tg_client.on(events.NewMessage)
async def handle_new_message(event):
    """Analyze new messages and flag scams."""
    message_text = event.message.message
    print(f"📩 New Message Received: {message_text}")

    if message_text:
        result = analyze_message(message_text)
        print(f"🔍 Scam Detection Result: {result}")

        if result.get("is_scam", False):  # ✅ Ensure "is_scam" key exists and is True
            scam_data = {
                "channel": event.chat_id,
                "message": message_text,
                "risk_score": float(result["risk_score"]),  # ✅ Convert NumPy float64 to standard float
                "flags": result["flags"]
            }

            try:
                save_to_mongodb(scam_data, "scam_messages")
                print(f"✅ Scam Message Saved: {scam_data}")
            except Exception as e:
                print(f"❌ Error Saving Scam Message: {e}")

async def send_alert(scam_data):
    """Send a real-time alert to the admin if a scam message is detected."""
    admin_id = config.get("telegram_admin_id", None)
    if admin_id:
        alert_message = (f"🚨 Scam Alert!\n\nChannel: {scam_data['channel']}\n"
                         f"Message: {scam_data['message']}\n"
                         f"Risk Score: {scam_data['risk_score']}\n"
                         f"Flags: {', '.join(scam_data['flags'])}")
        await tg_client.send_message(admin_id, alert_message)  # ✅ Use tg_client instead of tg_bot

async def add_channel(channel_id):
    """Add a new channel to the monitoring list."""
    save_to_mongodb({"channel_id": channel_id}, "monitored_channels")
    await tg_client.get_entity(channel_id)
    return {"success": True, "message": f"✅ Channel {channel_id} added to monitoring."}

async def remove_channel(channel_id):
    """Remove a channel from the monitoring list."""
    from utility import delete_from_mongodb
    delete_from_mongodb("monitored_channels", {"channel_id": channel_id})
    return {"success": True, "message": f"❌ Channel {channel_id} removed from monitoring."}

def start_telegram_monitoring():
    """Start the Telegram monitoring service with auto-reconnect."""
    while True:
        try:
            print("🚀 Starting Telegram Monitoring...")
            with tg_client:
                tg_client.loop.run_until_complete(monitor_channels())
                tg_client.run_until_disconnected()
        except ConnectionError:
            print("❌ Connection to Telegram failed. Retrying in 10 seconds...")
            time.sleep(10)  # ✅ Wait before reconnecting

if __name__ == "__main__":
    start_telegram_monitoring()
