from flask import Flask, render_template, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "guestbook.json")

def load_entries():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

def save_entries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries[-100:], f, ensure_ascii=False, indent=2)

@app.get("/")
def home():
    return render_template("index.html", entries=load_entries())

@app.get("/trinity")
def trinity():
    return render_template("trinity.html")

@app.get("/api/trinity-config")
def trinity_config():
    import json as _json
    config_path = os.path.join(os.path.dirname(__file__), "static", "data", "trinity-timeline.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return _json.load(f)
    except (OSError, _json.JSONDecodeError):
        return jsonify({"error": "config not found"}), 404

@app.post("/api/oath")
def oath():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "Cookie Runner")).strip()[:32] or "Cookie Runner"
    message = str(payload.get("message", "")).strip()[:180]
    if not message:
        message = "I celebrate friendship, teamwork, and every Cookie Run adventure!"
    entries = load_entries()
    entries.append({
        "name": name,
        "message": message,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_entries(entries)
    return jsonify({"ok": True, "count": len(entries), "entry": entries[-1]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
