from flask import Flask, request, jsonify, send_file, url_for
from flask_cors import CORS
import json, os

# Create the Flask app
app = Flask(__name__)
CORS(app)

# Root route for Render homepage
@app.route("/", methods=["GET"])
def home():
    return "Weather Backend is running!"

# File paths
LATEST_FILE = "latest.json"
FIRMWARE_FILE = "firmware.bin"

# Load latest reading from file if it exists
def load_latest():
    if os.path.exists(LATEST_FILE):
        try:
            with open(LATEST_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

latest_reading = load_latest()

# Health check route
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# Ingest new sensor data
@app.route("/ingest", methods=["POST"])
def ingest():
    global latest_reading
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "invalid JSON"}), 400
    if "timestamp" not in data:
        return jsonify({"error": "missing timestamp"}), 400
    latest_reading = data
    with open(LATEST_FILE, "w") as f:
        json.dump(latest_reading, f)
    return jsonify({"message": "data received"})

# Return latest reading
@app.route("/latest", methods=["GET"])
def latest():
    if latest_reading:
        return jsonify(latest_reading)
    return jsonify({"error": "no data yet"}), 404

# Firmware metadata
@app.route("/firmware/latest", methods=["GET"])
def firmware_latest():
    return jsonify({
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- Dashboard route ---
@app.route("/dashboard")
def dashboard():
    # This will look for templates/index.html
    return render_template("index.html")


# --- Example API routes ---
# Replace these with your real sensor logic

@app.route("/latest")
def latest():
    # Example JSON response
    return jsonify({
        "temperature": 22,
        "humidity": 55,
        "pressure": 1013,
        "rain_hour": 0.00,
        "rain_day": 0.00,
        "wind_speed": 0,
        "wind_dir": "SE",
        "battery_voltage": 3.7,
        "battery_percent": 85,
        "sun_alt": 45,
        "sun_az": 180,
        "timestamp": "2025-12-05T09:34:00Z"
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    # Here you would normally save sensor data
    return jsonify({"received": data}), 201


# --- Entry point ---
if __name__ == "__main__":
    # Use Render's PORT if available, otherwise default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
