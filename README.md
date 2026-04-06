# Hawkn ERP Stock Transfer Assessment

A minimal ERP-style stock transfer system built with **Django REST Framework + React**.

## Features
- Token-based login
- Create stock transfer requests
- Approve stock transfer with concurrency safety
- Duplicate approval prevention
- Branch-wise stock summary
- Transfer history with filtering
- Role-based authorization for approval
- Minimal React UI for demo flow
- Automated API tests

---

## Tech Stack
- Backend: Django, Django REST Framework
- Frontend: React, Axios
- Database: SQLite
- Auth: DRF Token Authentication

---

## Backend Setup
```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs at:
```text
http://127.0.0.1:8000
```

---

## Frontend Setup
```bash
cd frontend
npm install
npm start
```

Frontend runs at:
```text
http://localhost:3000
```

---

## Demo Credentials
```text
username: admin
password: admin
```

---

## Important APIs
### Login
```text
POST /api/token/
```

### Create transfer
```text
POST /api/transfers/
```

### Approve transfer
```text
POST /api/transfers/<id>/approve/
```

### Stock summary
```text
GET /api/branches/<id>/stock-summary/
```

### Transfer history
```text
GET /api/transfers/
```

---

## Run Tests
```bash
python manage.py test
```

---

## Demo Flow
1. Login in React UI
2. Create stock transfer
3. Approve transfer
4. Load stock summary
5. Show Django admin audit trail

---
