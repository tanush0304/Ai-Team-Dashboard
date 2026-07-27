# 🤖 AI Team Dashboard

An AI-powered full-stack dashboard for managing teams, projects, and daily updates. The application combines a modern React frontend with a FastAPI backend and integrates Groq LLM + Supabase to provide an intelligent assistant capable of answering natural language questions about organizational data.

---

## 🚀 Features

### 📊 Dashboard
- Modern enterprise dashboard UI
- Team statistics
- Project overview
- Recent daily updates
- Top contributor section
- Interactive charts

### 👥 Team Management
- View all team members
- Add new members
- Update member information
- Delete members

### 📁 Project Management
- View projects
- Create new projects
- Edit project details
- Delete projects

### 📝 Daily Updates
- Track employee updates
- Add daily work logs
- Edit updates
- Delete updates

### 🤖 AI Assistant
- Natural language querying
- SQL generation using Groq LLM
- Conversation history
- SQL validation
- Safe SELECT-only execution
- Hybrid AI pipeline
- Context-aware responses

---

# 🛠 Tech Stack

## Frontend

- React.js
- Chakra UI
- React Router
- Axios
- Chart.js

## Backend

- FastAPI
- Python
- Supabase
- Groq API

## Database

- Supabase PostgreSQL

---

# 📂 Project Structure

```
AI-Team-Dashboard/
│
├── backend/
│   ├── ai/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/tanush0304/Ai-Team-Dashboard.git
cd Ai-Team-Dashboard
```

---

## 2. Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder.

Example:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GROQ_API_KEY=your_groq_api_key
```

Run backend

```bash
uvicorn app:app --reload
```

Backend runs at

```
http://localhost:8000
```

---

## 3. Frontend Setup

```bash
cd frontend

npm install
```

Start React app

```bash
npm start
```

Frontend runs at

```
http://localhost:3000
```

---

# 🤖 AI Workflow

User Question

↓

Context Builder

↓

Prompt Generation

↓

Groq LLM

↓

SQL Validation

↓

Safe SQL Execution

↓

Supabase Database

↓

AI Response

---

# 📸 Screenshots

Add screenshots here after deployment.

Example:

```
Dashboard Screenshot

AI Assistant Screenshot

Projects Page

Team Members Page
```

---

# 🔒 Security

- Environment variables stored in `.env`
- `.env` excluded using `.gitignore`
- SQL validation before execution
- Only safe SELECT queries are allowed
- API keys are never committed

---

# 📌 Future Improvements

- User authentication
- Role-based access control
- AI-generated analytics
- Real-time notifications
- File uploads
- Export reports (PDF/Excel)
- Dark mode
- Docker deployment

---

# 👨‍💻 Author

**Tanush A K**

- GitHub: https://github.com/tanush0304

---

# ⭐ If you found this project helpful

Please consider giving it a ⭐ on GitHub.
