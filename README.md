# FomVPSMailDataSender
A Django REST API to monitor and analyze outgoing email logs from a Postfix mail server. This project parses `mail.txt` (Postfix log), extracts outgoing email activity, and summarizes delivery statuses like `sent`, `bounced`, `deferred`, and more.
---

## 🚀 Features

- Parses raw Postfix logs
- Extracts sender, recipient, and status of each email
- Summarizes delivery stats
- JSON API endpoint for easy integration

---

## 📁 Project Structure
mailDataSender/
│
├── mailDataSender/ # Django project settings
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── api/ # Custom Django app
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── serializers.py # DRF serializers
│ ├── tests.py
│ ├── urls.py # API routes
│ └── views.py # OutgoingMailsView logic
│
├── mail.txt # Log file for parsing (Postfix output)
├── db.sqlite3 # SQLite database (if using Django models)
├── manage.py


2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the requirements
```bash
pip install django djangorestframework
```

🔌 Running the Server
```bash
python manage.py runserver
```
