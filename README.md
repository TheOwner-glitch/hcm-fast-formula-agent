# Oracle HCM Fast Formula Agent

This Flask-based tool helps Oracle Cloud HCM users generate, explain, validate, and modify Fast Formulas using the OpenAI API. Designed for both HR and technical users, it provides a user-friendly interface to streamline Fast Formula development and analysis.

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fast-formula-agent.git
cd fast-formula-agent
````

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

## ▶️ 5. Launch the App (Development Mode)

### On **Windows** (PowerShell):

```powershell
cd fast-formula-agent
.\venv\Scripts\Activate
$env:FLASK_APP = "app.main"
$env:FLASK_ENV = "development"
flask run
```

### On **macOS/Linux**:

```bash
cd fast-formula-agent
source venv/bin/activate
export FLASK_APP=app.main
export FLASK_ENV=development
flask run
```

Once running, open in your browser:

* 🌐 **Main App**: [http://localhost:5000](http://localhost:5000)
* 🔐 **Admin Panel**: [http://localhost:5000/admin/](http://localhost:5000/admin/)

---

## 🚀 Production Deployment (Using Gunicorn)

To run this app in production, use [**Gunicorn**](https://gunicorn.org/), a Python WSGI HTTP server:

```bash
gunicorn app.main:app --bind 0.0.0.0:5000
```

This provides better performance and security compared to the Flask development server.

If you're using Docker, consider modifying your Dockerfile like this:

```dockerfile
CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:5000"]
```

---

## 🛳️ Docker Support

This app includes a lightweight `Dockerfile` for containerized environments.

### Build the Docker image:

```bash
docker build -t fast-formula-agent .
```

### Run the container:

```bash
docker run -p 5000:5000 --env-file .env fast-formula-agent
```

### Notes:

* The container runs using Gunicorn for production readiness.
* Make sure your `.env` file is present in the root directory.

---

## 📦 Plugin System

This project supports a **modular plugin architecture** for custom actions. Plugins live in the `plugins/` folder and can be added without modifying core logic. Example included: `summarize_formula`.

To add new actions:

* Define a plugin in a `.py` file using the same structure
* Register it in `plugins/__init__.py`

---

## 🔐 Notes

* Do **not** commit your `.env` file to GitHub — it contains sensitive credentials.
* The app uses the `OPENAI_API_KEY` from `.env` to access the OpenAI API.
* Session-based login and audit logging are built in.