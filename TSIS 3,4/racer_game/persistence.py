import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    default = {"sound": False, "car_color": [50, 180, 255], "difficulty": "normal"}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                default.update(json.load(f))
        except Exception:
            pass
    return default


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_result(name, score, distance):
    data = load_leaderboard()
    data.append({"name": name, "score": score, "distance": int(distance)})
    data.sort(key=lambda x: x["score"], reverse=True)
    data = data[:10]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
