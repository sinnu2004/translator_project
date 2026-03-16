# 🌐 Django Language Translator App

A multilingual text translator web application built with Django and the Python `translate` library. Supports 20+ languages with a modern dark-themed pure CSS UI, translation history, and copy-to-clipboard functionality.

---

## 📁 Project Structure

```
translator_project/
│
├── translator/               ← Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── main/                     ← Main app
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── main/
│   │       └── index.html
│   └── static/
│       └── main/
│           └── style.css
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🖥️ Run Locally with VS Code

### Step 1 — Prerequisites

Make sure you have installed:
- **Python 3.9+** → https://www.python.org/downloads/
- **VS Code** → https://code.visualstudio.com/
- **Python extension for VS Code** (search "Python" in Extensions panel)

### Step 2 — Open the Project

```bash
# Open VS Code, then open the folder:
File → Open Folder → select "translator_project"
```

Or from terminal:
```bash
cd path/to/translator_project
code .
```

### Step 3 — Create a Virtual Environment

Open the VS Code integrated terminal (`Ctrl + `` ` ``):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install django
pip install translate
```

### Step 5 — Run Database Migrations

```bash
python manage.py migrate
```

### Step 6 — Start the Development Server

```bash
python manage.py runserver
```

### Step 7 — Open in Browser

Visit: **http://127.0.0.1:8000/**

---

## ✅ Features

| Feature | Status |
|---|---|
| Text input & translation | ✅ |
| 20+ language dropdown | ✅ |
| Django form with CSRF | ✅ |
| Modern dark UI (pure CSS) | ✅ |
| Character counter | ✅ |
| Copy translated text | ✅ |
| Translation history (localStorage) | ✅ |
| Responsive mobile layout | ✅ |
| Error handling | ✅ |

---

## 🚀 Deploy to Render (Free Hosting)

Render.com offers free Django hosting. Follow these steps:

### Step 1 — Create a `Procfile`

Create a file named `Procfile` (no extension) in the project root:

```
web: gunicorn translator.wsgi
```

### Step 2 — Install gunicorn

```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Step 3 — Update `settings.py` for production

```python
import os

DEBUG = False

ALLOWED_HOSTS = ['your-app-name.onrender.com']

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
```

### Step 4 — Add whitenoise for static files

```bash
pip install whitenoise
pip freeze > requirements.txt
```

In `settings.py`, add to MIDDLEWARE (after SecurityMiddleware):
```python
'whitenoise.middleware.WhiteNoiseMiddleware',
```

### Step 5 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/translator-app.git
git push -u origin main
```

### Step 6 — Deploy on Render

1. Go to https://render.com and sign up
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Set these settings:
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn translator.wsgi`
   - **Environment:** Python 3
5. Click **Create Web Service**

Your app will be live at `https://your-app-name.onrender.com` 🎉

---

## 🚀 Deploy to Railway (Alternative)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway init
railway up
```

---

## 🚀 Deploy to PythonAnywhere (Beginner Friendly)

1. Sign up at https://www.pythonanywhere.com
2. Go to **Files** and upload your project zip
3. Open a **Bash console** and run:
   ```bash
   pip install django translate
   python manage.py migrate
   ```
4. Go to **Web** tab → Add new web app → Django
5. Set source directory to your project folder
6. Click **Reload**

---

## 🔧 Supported Languages

| Language | Code |
|---|---|
| Hindi | hi |
| Marathi | mr |
| German | de |
| French | fr |
| Spanish | es |
| Arabic | ar |
| Chinese | zh |
| Japanese | ja |
| Korean | ko |
| Portuguese | pt |
| Russian | ru |
| Italian | it |
| Turkish | tr |
| Dutch | nl |
| Polish | pl |
| Swedish | sv |
| Urdu | ur |
| Bengali | bn |
| Tamil | ta |
| Telugu | te |

---

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'translate'`**
```bash
pip install translate
```

**Static files not loading**
```bash
python manage.py collectstatic
```

**Port already in use**
```bash
python manage.py runserver 8080
# Then visit http://127.0.0.1:8080
```

**Translation returns error**
- Check your internet connection (the translate library calls an external API)
- Try a shorter input text

---

## 📄 License

MIT License — free to use and modify.
