# Oracle HCM Fast Formula Agent

This Flask-based tool helps Oracle Cloud HCM users **generate**, **explain**, **validate**, and **modify** Fast Formulas using the OpenAI API.

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fast-formula-agent.git
cd fast-formula-agent
```

### 2. Create Your Environment File
Copy the template and fill in your actual OpenAI API key:
```bash
cp env.template .env
```

### 3. Set Up Python Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the App
```bash
flask run
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔐 Notes

- Do **NOT** commit your `.env` file to GitHub.
- This app uses the `OPENAI_API_KEY` from the `.env` file to call the OpenAI API.

---

## 📄 License

MIT or internal use. Customize as needed.
