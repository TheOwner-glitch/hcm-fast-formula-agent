# Oracle HCM Fast Formula Agent

This Flask-based tool helps Oracle Cloud HCM users generate, explain, validate, and modify Fast Formulas using the OpenAI API. Designed with HR and technical users in mind, it provides a powerful, user-friendly interface to streamline Fast Formula development and analysis.

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fast-formula-agent.git
cd fast-formula-agent
```

### 2. Create Your Environment File

Copy the environment template and set your actual OpenAI API key:

```bash
cp env.template .env
```

Edit `.env` to include your OpenAI credentials (e.g., `OPENAI_API_KEY=sk-...`).

### 3. Set Up Python Environment

Create and activate a virtual environment, then install dependencies:

#### On **Windows**:

```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

#### On **macOS/Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Optional: Customize Users

Edit `app/users.json` to add usernames and password hashes for login access.

---

## ▶️ 5. Launch the App

### On **Windows** (PowerShell):

```powershell
cd fast-formula-agent
.\venv\Scripts\Activate
$env:FLASK_APP = "app/app.py"
$env:FLASK_ENV = "development"
flask run
```

### On **macOS/Linux**:

```bash
cd fast-formula-agent
source venv/bin/activate
export FLASK_APP=app/app.py
export FLASK_ENV=development
flask run
```

Once running, open in your browser:

* 🌐 **Main App**: [http://localhost:5000](http://localhost:5000)
* 🔐 **Admin Panel**: [http://localhost:5000/admin/](http://localhost:5000/admin/)

---

## 🔐 Notes

* Do **not** commit your `.env` file to GitHub — it contains sensitive credentials.
* The app uses the `OPENAI_API_KEY` from `.env` to access the OpenAI API.
* Session-based login and audit logging are built in.