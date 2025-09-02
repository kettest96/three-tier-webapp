from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend JS to call API

# Connect to MySQL
db = mysql.connector.connect(
    host="db",
    user="root",
    password="rootpass",
    database="testdb"
)
cursor = db.cursor()

# Create users and orders table if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item VARCHAR(100),
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")
db.commit()

# Sample user for testing
cursor.execute("INSERT IGNORE INTO users (username, password) VALUES ('ravi','pass123')")
db.commit()


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s",
                   (data['username'], data['password']))
    user = cursor.fetchone()
    if user:
        return jsonify({"success": True, "user_id": user[0]})
    return jsonify({"success": False, "message": "Invalid credentials"})


@app.route("/order", methods=["POST"])
def order():
    data = request.json
    cursor.execute("INSERT INTO orders (user_id, item) VALUES (%s, %s)",
                   (data['user_id'], data['item']))
    db.commit()
    return jsonify({"success": True, "message": f"Order '{data['item']}' placed successfully!"})


@app.route("/orders/<int:user_id>", methods=["GET"])
def get_orders(user_id):
    cursor.execute("SELECT item FROM orders WHERE user_id=%s", (user_id,))
    orders = [row[0] for row in cursor.fetchall()]
    return jsonify({"orders": orders})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

