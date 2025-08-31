# Webhook Dashboard (Flask)

A simple webhook receiver and dashboard built with **Flask**, **SQLite**, and vanilla **JavaScript**.  
It lets you collect webhooks, inspect their payloads, headers, and query params, and manage them from a UI.

---

## ✨ Features
- ✅ Receive webhooks on unique per-user endpoints  
- ✅ Store webhook requests (headers, payload, method, query params, timestamp)  
- ✅ Dashboard UI to list and inspect webhooks  
- ✅ Refresh button to reload webhooks dynamically  
- ✅ Delete webhooks from the dashboard (with red delete button)  
- ✅ Cookie-based `user_id` for separating data  

---

## 📦 Requirements

- Python 3.8+
- Flask
- SQLite (comes pre-installed with Python)

---

## 🚀 Getting Started

### 1. Clone this repo
```bash
git clone https://github.com/PrasadAuti/flask-webhook-app.git
```

### 2. Create virtual environment
```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
### 3. Install dependencies
```
pip install flask
```

### 4. Run the server
```
python app.py
```
##### Flask will start at http://127.0.0.1:5000
---

### 🖼️ Screenshots
- Check Project demo and screenshot in static/demo

---
## 📡 Usage
1. Open the dashboard in your browser.
    > The app will generate a unique user_id and assign it via cookies.

2. You’ll see your personal webhook endpoint like:
    > /api/webhook/<user_id>

3. Send any HTTP request (GET, POST, PUT, PATCH, DELETE) to that endpoint. 
    > Example:
```
curl -X POST http://127.0.0.1:5000/api/webhook/<user_id> \
     -H "Content-Type: application/json" \
     -d '{"hello":"world"}'

```
4. Refresh the dashboard → new webhook appears in the list.
5. Click a webhook → see details (headers, query params, payload).
6. Hover over a webhook → red delete button (×) appears, click to remove it.
---

## ⚠️ Notes
- This uses SQLite (fine for dev/small projects). For production, use Postgres/MySQL.
- No authentication → don’t expose to the public internet without securing.
- Payloads are stored as raw text. Large binary payloads may not render well in the UI.
