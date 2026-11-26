"""
DJ NOTFALL-STUDIO (gross) - Backend
Original Frontend: src/App.tsx + src/index.css (React + Vite + Tailwind)
Backend: Python + Flask

Lokal (Frontend dev):
  npm install
  npm run dev          -> http://localhost:5173
  python app.py        -> http://localhost:5000 (API + gebautes Frontend aus dist/)

Lokal (gebautes Frontend + Backend zusammen):
  npm run build
  python app.py        -> http://localhost:5000

Render (Docker, siehe Dockerfile + render.yaml):
  gunicorn -w 1 -b 0.0.0.0:$PORT app:app
"""
import json, os, random
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
DATA_FILE = os.path.join(BASE_DIR, "studio.json")

app = Flask(__name__, static_folder="dist", static_url_path="")
CORS(app)

TRACKS = [
    {"id": 0, "name": "House 124", "genre": "House", "bpm": 124, "key": "A-moll"},
    {"id": 1, "name": "Techno 135", "genre": "Techno", "bpm": 135, "key": "F-moll"},
    {"id": 2, "name": "Hip-Hop 90", "genre": "HipHop", "bpm": 90, "key": "C-moll"},
    {"id": 3, "name": "Drum & Bass 174", "genre": "DnB", "bpm": 174, "key": "G-moll"},
    {"id": 4, "name": "Disco 118", "genre": "Disco", "bpm": 118, "key": "D-Dur"},
    {"id": 5, "name": "Chill 100", "genre": "Chill", "bpm": 100, "key": "E-Dur"},
]

STREAM_TRACKS = [
    {"id": "stream-1", "name": "House Sunset", "genre": "House", "bpm": 124, "key": "A-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
    {"id": "stream-2", "name": "Techno Pulse", "genre": "Techno", "bpm": 135, "key": "F-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
    {"id": "stream-3", "name": "Deep House Night", "genre": "House", "bpm": 122, "key": "C-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"},
    {"id": "stream-4", "name": "Hip-Hop Boom", "genre": "HipHop", "bpm": 90, "key": "G-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"},
    {"id": "stream-5", "name": "DnB Rush", "genre": "DnB", "bpm": 174, "key": "D-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"},
    {"id": "stream-6", "name": "Disco Fever", "genre": "Disco", "bpm": 118, "key": "B-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3"},
    {"id": "stream-7", "name": "Chill Vibes", "genre": "Chill", "bpm": 100, "key": "E-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3"},
    {"id": "stream-8", "name": "Trap Night", "genre": "Trap", "bpm": 140, "key": "F-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"},
    {"id": "stream-9", "name": "Afro Heat", "genre": "Afro", "bpm": 112, "key": "A-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3"},
    {"id": "stream-10", "name": "Melodic Techno", "genre": "Techno", "bpm": 128, "key": "G-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3"},
    {"id": "stream-11", "name": "LoFi Dreams", "genre": "LoFi", "bpm": 82, "key": "C-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3"},
    {"id": "stream-12", "name": "Peak Time", "genre": "House", "bpm": 132, "key": "A-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3"},
]

DEFAULT_DATA = {"bpm": 128, "master": 0.8, "presets": [], "beats": [], "scenes": [], "hardware": "Kein Gerät"}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return dict(DEFAULT_DATA)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in DEFAULT_DATA.items():
            if k not in d:
                d[k] = v
        return d
    except Exception:
        return dict(DEFAULT_DATA)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    dist_index = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(dist_index):
        return send_file(dist_index)
    return send_file(os.path.join(BASE_DIR, "index.html"))

@app.route("/assets/<path:path>")
def assets(path):
    return send_from_directory(os.path.join(DIST_DIR, "assets"), path)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "DJ NOTFALL-STUDIO (gross)", "version": "2.0.0"})

@app.route("/api/tracks", methods=["GET"])
def get_tracks():
    return jsonify(TRACKS)

@app.route("/api/stream-tracks", methods=["GET"])
def get_stream_tracks():
    return jsonify(STREAM_TRACKS)

@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(load_data())

@app.route("/api/state", methods=["POST"])
def save_state():
    data = request.get_json(force=True)
    cur = load_data()
    cur.update(data)
    if "bpm" in cur:
        cur["bpm"] = int(max(20, min(180, int(cur["bpm"]))))
    save_data(cur)
    return jsonify({"ok": True, "state": cur})

@app.route("/api/presets", methods=["GET"])
def get_presets():
    return jsonify(load_data().get("presets", []))

@app.route("/api/presets", methods=["POST"])
def save_preset():
    data = request.get_json(force=True)
    cur = load_data()
    presets = cur.get("presets", [])
    preset = {"id": len(presets) + 1, "name": str(data.get("name", "Preset"))[:60], "bpm": int(data.get("bpm", 128))}
    presets.append(preset)
    cur["presets"] = presets
    save_data(cur)
    return jsonify({"ok": True, "preset": preset})

@app.route("/api/beats", methods=["GET"])
def get_beats():
    return jsonify(load_data().get("beats", []))

@app.route("/api/beats", methods=["POST"])
def save_beat():
    data = request.get_json(force=True)
    if not isinstance(data.get("steps"), list):
        return jsonify({"error": "steps muss eine Liste sein"}), 400
    cur = load_data()
    beats = cur.get("beats", [])
    beat = {"id": len(beats) + 1, "name": str(data.get("name", "Beat"))[:60], "bpm": int(max(20, min(180, int(data.get("bpm", 128))))), "steps": data["steps"]}
    beats.append(beat)
    cur["beats"] = beats
    save_data(cur)
    return jsonify({"ok": True, "beat": beat})

@app.route("/api/random-mix", methods=["GET"])
def random_mix():
    mixes = [
        {"genre": "Keller-Techno", "bpm": 132, "line": "Der Bass kommt aus dem Keller - und bleibt da!"},
        {"genre": "Schlager-House", "bpm": 124, "line": "Alle singen mit, keiner weiss warum!"},
        {"genre": "Balkon-Rave", "bpm": 140, "line": "Nachbarn tanzen heimlich mit."},
        {"genre": "Sofa-Bass", "bpm": 96, "line": "So weich, dass die Couch mitschaukelt."},
    ]
    return jsonify(random.choice(mixes))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"DJ NOTFALL-STUDIO (gross) laeuft auf Port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
