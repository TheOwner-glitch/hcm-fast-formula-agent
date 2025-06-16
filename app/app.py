from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client using API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt templates for the four actions
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

def log_interaction(action, prompt, response):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "prompt": prompt,
        "response": response
    }

    log_path = os.path.join(os.getcwd(), "history.jsonl")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-9:]  # keep last 9 to make room for new
    else:
        lines = []

    lines.append(json.dumps(log_entry) + "\n")
    with open(log_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    logic = ""
    inputs = ""
    original = ""
    action = ""

    if request.method == "POST":
        action = request.form["action"]
        model = request.form.get("model", "gpt-4")
        logic = request.form.get("logic", "")
        inputs = request.form.get("inputs", "")
        original = request.form.get("original", "")

        # Build the prompt using the selected action
        prompt = PROMPT_TEMPLATES[action].format(logic=logic, inputs=inputs, original=original)

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an Oracle HCM expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )
            result = response.choices[0].message.content
        except Exception as e:
            result = f"An error occurred while contacting OpenAI: {str(e)}"

        # Log the interaction
        log_interaction(action, prompt, result)

    return render_template("index.html", result=result, logic=logic, inputs=inputs, original=original, action=action)

if __name__ == "__main__":
    app.run(debug=True)