
from flask import Flask, request, jsonify, send_file, url_for
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

LATEST_FILE = "latest.json"
FIRMWARE_FILE = "firmware.bin"

def load_latest():
    if os.path.exists(LATEST_FILE):
        try:
            with open(LATEST_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

latest_reading = load_latest()

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

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

@app.route("/latest")
def latest():
    if latest_reading:
        return jsonify(latest_reading)
    return jsonify({"error": "no data yet"}), 404

@app.route("/firmware/latest")
def firmware_latest():
    return jsonify({
        "version": "1.0.0",
        "url": url_for("firmware_download", _external=True),
        "sha256": "replace-with-real-sha256"
    })

@app.route("/firmware/download")
def firmware_download():
    if os.path.exists(FIRMWARE_FILE):
        return send_file(FIRMWARE_FILE, as_attachment=True)
    return jsonify({"error": "firmware not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
