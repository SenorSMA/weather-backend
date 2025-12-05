import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- Dashboard route ---
@app.route("/dashboard")
def dashboard():
    return render_template("index.html")


# --- Example API routes ---
@app.route("/latest")
def latest():
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
    })  # <-- dictionary closed with } and jsonify closed with )


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    return jsonify({"received": data}), 201


# --- Entry point ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
