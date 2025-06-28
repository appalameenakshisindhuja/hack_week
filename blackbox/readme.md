# 🕵️ Mystery API Explorer

Welcome to the **Mystery API Explorer** — a full-stack project to interactively test and reverse-engineer hidden behaviors of various Flask API endpoints through a beautiful dark-themed frontend.



---

## 📦 Features

- 🌌 Dark/Cyberpunk UI (inspired by futuristic terminal dashboards)
- 🎯 Test 7 mysterious API endpoints
- 🔄 Real-time responses with POST requests
- 🧠 Explore hidden behaviors and patterns
- 🧪 Manual Testing + Auto Discovery Tools
- 💡 Record your discoveries

---

## 🧩 Tech Stack

| Layer      | Tech                            |
|------------|----------------------------------|
| Frontend   | HTML, CSS (Neon theme), Vanilla JS |
| Backend    | Python, Flask + Flask-CORS      |
| Hosting    |  Local Flask  |

---

## 🛠️ Local Development

### 🧱 Prerequisites
- Python 3.7+
- Flask
- Flask-CORS

### 🔧 Backend Setup


# Clone the repo
git clone https://github.com/your-username/blackbox.git
cd blackbox

# Install dependencies
pip install flask flask-cors

# Run Flask server
python app.py
The backend runs at: http://localhost:5000

💻 Frontend Setup
You can open index.html directly OR serve with a local dev server:
# Option 1: Serve locally
npx serve
# OR
python -m http.server 5500
Frontend expects backend to run at: http://localhost:5000

To change that, edit this line in index.html:
const baseUrl = 'http://localhost:5000';

# # 📂 Project Structure
📁 blackbox/
├── app.py               # Flask API backend
├── index.html           # Stylish frontend
├── README.md            # This file
## 🧪 Available Endpoints
Endpoint	Behavior Summary
/api/echo	Reverses string on every 3rd request
/api/transform	ROT13 / Base64 / Pig Latin / Hash
/api/filter	Filter content: vowels, numbers, etc.
/api/sequence	Generates patterns like Fibonacci, primes
/api/memory	Stores & retrieves session data
/api/validator	Mystery & pattern-based validation

