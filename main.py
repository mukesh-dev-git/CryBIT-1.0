from flask import Flask, render_template, request, jsonify
from utility import fetch_from_mongodb, save_to_mongodb, delete_from_mongodb, load_config
from database import add_monitored_channel, clear_monitored_channels, remove_monitored_channel

app = Flask(__name__)
config = load_config()

@app.route('/')
def index():
    """Render the dashboard page."""
    scam_messages = fetch_from_mongodb("scam_messages")
    monitored_channels = fetch_from_mongodb("monitored_channels")  
    return render_template("index.html", scam_messages=scam_messages, monitored_channels=monitored_channels)

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    """Render the scan page and process manual scam detection requests."""
    if request.method == 'POST':
        message_text = request.form.get("message_text")
        # Placeholder for scam detection logic
        result = {"message": message_text, "risk_score": 0.7, "is_scam": True}
        save_to_mongodb(result, "scam_messages")
        return jsonify(result)
    return render_template("scan.html")

@app.route('/logs')
def logs():
    """Render the logs page displaying flagged scam messages."""
    scam_messages = fetch_from_mongodb("scam_messages")
    return render_template("logs.html", scam_messages=scam_messages)

@app.route('/channels')
def channels():
    """Render the channels page for monitoring Telegram channels."""
    monitored_channels = fetch_from_mongodb("monitored_channels")
    return render_template("channels.html", monitored_channels=monitored_channels)

from flask import Flask, render_template, request, jsonify

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Render and update scam detection settings."""
    if request.method == 'POST':
        try:           
            data = request.get_json() if request.is_json else request.form
           
            if "risk_threshold" in data:
                new_threshold = float(data["risk_threshold"])
                config["scam_detection"]["risk_threshold"] = new_threshold
          
            if "scam_keywords" in data:
                config["scam_detection"]["scam_keywords"] = data["scam_keywords"]
           
            if "admin_id" in data:
                config["telegram_admin_id"] = data["admin_id"]

            return jsonify({"success": True, "updated_config": config})

        except ValueError:
            return jsonify({"error": "Invalid input format"}), 400

    return render_template("settings.html", config=config)

@app.route('/api/scam-messages', methods=['GET'])
def get_scam_messages():
    """API endpoint to fetch flagged scam messages."""
    messages = fetch_from_mongodb("scam_messages")
    return jsonify(messages)

@app.route('/api/clear-messages', methods=['POST'])
def clear_messages():
    """API endpoint to clear all flagged messages."""
    delete_from_mongodb("scam_messages")
    return jsonify({"success": True, "message": "All scam messages cleared."})

@app.route('/message_analysis')
def message_analysis():
    """Render the message analysis page."""
    scam_messages = fetch_from_mongodb("scam_messages")
    return render_template("message_analysis.html", scam_messages=scam_messages)

@app.route('/add_channel', methods=['POST'])
def add_channel():
    """Add a new Telegram channel to the monitored list."""
    data = request.json
    channel_id = data.get("channel_id")

    if not channel_id:
        return jsonify({"success": False, "message": "Channel ID is required"}), 400

    add_monitored_channel(channel_id)
    return jsonify({"success": True, "message": f"✅ Channel {channel_id} added successfully!"})

@app.route('/clear_channels', methods=['POST'])
def clear_channels():
    """Clear all monitored channels."""
    clear_monitored_channels()  
    return jsonify({"message": "All channels cleared"}), 200

@app.route('/remove_channel', methods=['POST'])
def remove_channel():
    """Remove a Telegram channel from the monitored list."""
    data = request.json
    channel_id = data.get("channel_id")

    if channel_id:
        remove_monitored_channel(channel_id)  
        return jsonify({"message": "Channel removed successfully"}), 200

    return jsonify({"error": "Channel ID is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)
