from flask import Flask, render_template, request, redirect, url_for, session
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import time
from werkzeug.security import check_password_hash
from app.logging_config import setup_logger
from app.admin import admin_bp

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "Vp*^:yR<DC>W_?|]m([;vwo<-yTF~n")
app.register_blueprint(admin_bp, url_prefix="/admin")

# Load users with hashed passwords from users.json
USERS_PATH = os.path.join(os.path.dirname(__file__), "users.json")
with open(USERS_PATH, "r") as f:
    USERS = json.load(f)

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt templates
PROMPT_TEMPLATES = {
    "generate": (
        "You are an Oracle HCM Fast Formula expert. "
        "Generate a fast formula based on the following description:\n"
        "{logic}\n"
        "Inputs: {inputs}\n"
        "Return only the formula code with inline comments."
    ),
    "modify": (
        "You are an Oracle HCM Fast Formula expert. "
        "Modify the following formula based on this request:\n"
        "Formula:\n{original}\n\n"
        "Change Request:\n{logic}\n"
        "Return the updated formula with inline comments."
    ),
    "explain": (
        "You are an Oracle Cloud HCM Fast Formula expert.\n"
        "Your job is to explain this Fast Formula clearly and thoroughly in plain English for an HR analyst who is not technical.\n"
        "DO NOT ask for more context or make assumptions about missing inputs.\n"
        "Just read the formula and explain what it is doing, line by line if needed.\n"
        "Here is the formula:\n\n{original}\n\n"
        "Return a concise and accurate explanation that includes:\n"
        "- The purpose of the formula\n"
        "- Any conditions or thresholds applied\n"
        "- The variables and values used\n"
        "- What the final returned value means"
    ),
    "validate": (
        "You are an Oracle HCM Fast Formula expert.\n"
        "Please validate the following Fast Formula:\n\n{original}\n\n"
        "Identify any syntax or logic issues, and return a corrected version if needed.\n"
        "Explain any changes you made after the corrected formula."
    )
}

def log_interaction(action, prompt, response, duration=None):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "prompt": prompt,
        "response": response,
        "duration": duration,
        "user": session.get("username", "unknown")
    }

    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.makedirs(static_dir, exist_ok=True)
    log_path = os.path.join(static_dir, "history.jsonl")

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-9:]
    else:
        lines = []

    lines.append(json.dumps(log_entry) + "\n")
    with open(log_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = USERS.get(username)

        if hashed_password and check_password_hash(hashed_password, password):
            session["authenticated"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    result = None
    logic = ""
    inputs = ""
    original = ""
    action = ""

    if request.method == "POST":
        client_ip = request.remote_addr
        user_agent = request.headers.get("User-Agent", "Unknown")
        action = request.form["action"]
        model = request.form.get("model", "gpt-4")
        logic = request.form.get("logic", "")
        inputs = request.form.get("inputs", "")
        original = request.form.get("original", "")

        logger.info(f"[{client_ip}] UserAgent: {user_agent}")
        logger.info(f"[{client_ip}] Request: action={action}, model={model}, user={session.get('username')}")

        prompt = PROMPT_TEMPLATES[action].format(logic=logic, inputs=inputs, original=original)

        try:
            start_time = time.perf_counter()

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an Oracle HCM expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )

            end_time = time.perf_counter()
            duration = round(end_time - start_time, 2)

            result = response.choices[0].message.content
            logger.info(f"[{client_ip}] OpenAI success – Action: {action}, Time: {duration}s")
        except Exception as e:
            result = f"An error occurred while contacting OpenAI: {str(e)}"
            logger.error(f"[{client_ip}] OpenAI error: {str(e)}")
            duration = None

        log_interaction(action, prompt, result, duration)

    return render_template("index.html", result=result, logic=logic, inputs=inputs, original=original, action=action)

if __name__ == "__main__":
    app.run(debug=True)