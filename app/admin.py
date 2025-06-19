from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
import json
import os
from datetime import datetime
from collections import Counter, defaultdict
import statistics

admin_bp = Blueprint("admin", __name__, template_folder="templates")

USERS_PATH = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=2)

@admin_bp.route("/", methods=["GET"])
def dashboard():
    if session.get("username") != "admin":
        return redirect(url_for("login"))

    users = load_users()
    logs = []

    log_path = os.path.join(os.path.dirname(__file__), "static", "history.jsonl")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    logs.append(entry)
                except:
                    pass

    # --- Metrics ---
    total_interactions = len(logs)
    action_counts = Counter(entry["action"] for entry in logs if "action" in entry)
    user_usage = Counter(entry.get("user", "unknown") for entry in logs)
    durations = []
    error_count = 0
    last_timestamp = None

    for entry in logs:
        if "response" in entry and isinstance(entry["response"], str):
            if "An error occurred" in entry["response"]:
                error_count += 1
        if "timestamp" in entry:
            try:
                ts = datetime.fromisoformat(entry["timestamp"])
                if last_timestamp is None or ts > last_timestamp:
                    last_timestamp = ts
            except:
                pass
        if "duration" in entry:
            try:
                durations.append(float(entry["duration"]))
            except:
                pass

    average_duration = round(statistics.mean(durations), 2) if durations else 0

    metrics = {
        "total_interactions": total_interactions,
        "action_counts": dict(action_counts),
        "user_usage": dict(user_usage),
        "average_duration": average_duration,
        "error_count": error_count,
        "last_interaction": last_timestamp.strftime("%Y-%m-%d %H:%M:%S") if last_timestamp else "N/A"
    }

    return render_template("admin_dashboard.html", users=users.keys(), logs=logs[-10:], metrics=metrics)

@admin_bp.route("/add_user", methods=["POST"])
def add_user():
    if session.get("username") != "admin":
        return redirect(url_for("login"))

    username = request.form.get("username")
    password = request.form.get("password")

    users = load_users()
    if username and username not in users:
        users[username] = generate_password_hash(password)
        save_users(users)

    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/delete_user", methods=["POST"])
def delete_user():
    if session.get("username") != "admin":
        return redirect(url_for("login"))

    username = request.form.get("username")
    users = load_users()
    if username in users and username != "admin":
        del users[username]
        save_users(users)

    return redirect(url_for("admin.dashboard"))