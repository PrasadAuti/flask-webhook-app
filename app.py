from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response
import uuid
import sqlite3
import json
import traceback

app = Flask(__name__)


def init_db():
    with sqlite3.connect("database.db") as conn:
        crs = conn.cursor()
        crs.execute(
            """CREATE TABLE IF NOT EXISTS webhooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                headers TEXT,
                payload TEXT,
                method TEXT,
                query_params TEXT,
                received_at TEXT NOT NULL
            )"""
        )
        conn.commit()

def safe_json_loads(s):
    if s is None:
        return None
    try:
        return json.loads(s)
    except Exception:
        # If somehow a row has non-JSON here, just return the original string
        return s


@app.route('/', methods=['GET'])
def check_user():
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
        resp = make_response(redirect(url_for("user_dashboard", user_id=user_id)))
        resp.set_cookie("user_id", user_id, max_age=60*60*24*365)  # 1 year
        return resp
    return redirect(url_for("user_dashboard", user_id=user_id), code=308)


@app.route('/webhooks/<user_id>', methods=['GET'])
def user_dashboard(user_id):
    return render_template("dashboard.html", user_id=user_id)


@app.route('/api/webhook/<user_id>', methods=['GET','POST','PUT','PATCH','DELETE'])
def receive_webhooks(user_id):
    try:
        headers_json = json.dumps(dict(request.headers))
        query_params_json = json.dumps(request.args.to_dict(flat=True))
        raw_body = request.get_data(as_text=True)  # raw payload as text
        method = request.method

        with sqlite3.connect("database.db") as conn:
            crs = conn.cursor()
            crs.execute("""
                INSERT INTO webhooks (user_id, headers, payload, method, query_params, received_at)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (user_id, headers_json, raw_body, method, query_params_json))
            conn.commit()

        return jsonify({"message": "Webhook received!"}), 201
    except Exception:
        print("Error while processing received webhook data: %s", traceback.format_exc())
        return jsonify({"error": "Error while processing received webhook data"}), 500


@app.route('/api/webhooks', methods=['GET'])
def fetch_webhooks_from_db():
    user_id = request.cookies.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id not found in cookies"}), 400

    with sqlite3.connect("database.db") as conn:
        crs = conn.cursor()
        crs.execute("""
            SELECT id, headers, payload, method, query_params, received_at
            FROM webhooks
            WHERE user_id=?
            ORDER BY id DESC
        """, (user_id,))
        rows = crs.fetchall()

    items = []
    for id_, headers, payload, method, qparams, received_at in rows:
        items.append({
            "id": id_,
            "method": method,
            "headers": safe_json_loads(headers),       # dict (ideally)
            "query_params": safe_json_loads(qparams),  # dict (ideally)
            "payload": payload,                        # raw text
            "received_at": received_at
        })

    return jsonify(items), 200

@app.route('/api/webhook/delete/<id>', methods=['DELETE'])
def delete_webhook_data(id):
    with sqlite3.connect("database.db") as conn:
        crs = conn.cursor()
        crs.execute("DELETE FROM webhooks WHERE id=?", (id,))
        conn.commit()
    return jsonify({"message": f"Deleted webhook {id}"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
