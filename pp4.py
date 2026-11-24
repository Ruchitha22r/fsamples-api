from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# Initialize database
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER
        )
    """)

    conn.commit()
    conn.close()


# CREATE - Add a student
@app.route("/students", methods=["POST"])
def insert_student():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, email, age) VALUES (?, ?, ?)",
        (
            data["name"],
            data["email"],
            data.get("age", 0)
        )
    )

    conn.commit()
    student_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student created",
        "id": student_id
    }), 201


# READ - Get all students
@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    conn.close()

    students = []

    for row in rows:
        students.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[3]
        })

    return jsonify(students)


# READ - Get one student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "age": row[3]
    })


# UPDATE - Update student name by ID
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET name = ? WHERE id = ?",
        (data["name"], student_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.close()

    return jsonify({
        "message": "Student name updated"
    })


# DELETE - Delete student by ID
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.close()

    return jsonify({
        "message": "Student deleted"
    })


# Start the application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
