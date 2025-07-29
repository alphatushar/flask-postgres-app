from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "tasks_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.json.get("task")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task added!"}), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)

# Update Task
@app.route("/update/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    new_task = request.json.get("task")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET task=%s WHERE id=%s", (new_task, task_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Task {task_id} updated!"})

# Delete Task
@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Task {task_id} deleted!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)