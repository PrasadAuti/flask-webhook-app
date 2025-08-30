from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response
import uuid
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        crs = conn.cursor()
        crs.execute(
            """CREATE TABLE IF NOT EXISTS webhooks
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            data TEXT,
            added_at TEXT NOT NULL
            )"""
        )

# Check if user is exsiting or new,
# if new then generate UUID for user and set the cookies
# else redirect to dashboard page
@app.route('/', methods=['GET'])
def check_user():
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
        resp = make_response(redirect(url_for("user_page", user_id=user_id)))
        resp.set_cookie("user_id", user_id, max_age=60*60*24*365)  # 1 year
        return resp
    return redirect(url_for("user_dashboard", user_id=user_id)), 308


@app.route('/webhooks/<user_id>', methods=['GET'])
def user_dashboard(user_id):
    return render_template("dashboard.html", user_id=user_id)


@app.route('/api/webhook/<user_id>', methods=['POST'])
def receive_webhooks(user_id):
    webhook_data = request.get_json()
    if webhook_data:
        with sqlite3.connect("database.db") as conn:
            crs = conn.cursor()
            crs.execute(
                "INSERT INTO webhooks (user_id, data, added_at) VALUES (?, ?, datetime('now'))",
                (user_id, webhook_data)
            )
            conn.commit()
        return jsonify({"message": "Webhook received!"}), 201
    return jsonify({"message": "Webhook data in not JSON"}), 201

@app.route('api/webhooks', methods=['GET'])
def fetch_webhhoks_from_db():
    user_id = request.cookies.get("user_id")
    if user_id:
        with sqlite3.connect("database.db") as conn:
            crs = conn.cursor()
            crs.execute(
                "SELECT data FROM webhooks WHERE user_id=?", (user_id,)
            )
            webhook_data = crs.fetchall()
            return jsonify(webhook_data), 200

    else:
        return jsonify({"error": "user_id not passed in cookies"}), 400

if __name__ == "__main__":
    app.run()