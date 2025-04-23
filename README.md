# PlatformDatabaseAD
# 🚀 Funding Platform Web App

A Django-based platform where users can discover and apply to funding opportunities tailored for changemakers and entrepreneurs.


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd funding_app
```


### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```


### 3. Install Dependencies
   
```bash
pip install -r requirements.txt
```


### 4. Apply Migrations

```bash
python manage.py migrate
```


### 5. Create a Superuser (optional)

```bash
python manage.py createsuperuser
```


###6. Run the Server

```bash
python manage.py runserver
```

Then visit http://127.0.0.1:8000 in your browser.

⸻

📁 File Structure Overview
```bash
funding_app/
│
├── funding/                 # Django app
├── templates/               # HTML files
├── static/                  # Custom CSS & JS
├── requirements.txt
├── README.md
└── manage.py
```
