from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------
# MySQL Configuration
# -----------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'   # change if needed
app.config['MYSQL_DB'] = 'college_db'

mysql = MySQL(app)

# -----------------------
# ADD STUDENT
# -----------------------
@app.route('/add', methods=['POST'])
def add_student():
    data = request.json

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO students (name, email, course, gender, review)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['name'], data['email'], data['course'],
          data['gender'], data['review']))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student Added Successfully"})


# -----------------------
# GET ALL STUDENTS
# -----------------------
@app.route('/get', methods=['GET'])
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    cur.close()

    students = []
    for row in rows:
        students.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "course": row[3],
            "gender": row[4],
            "review": row[5]
        })

    return jsonify(students)


# -----------------------
# UPDATE STUDENT
# -----------------------
@app.route('/update/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE students
        SET name=%s, email=%s, course=%s, gender=%s, review=%s
        WHERE id=%s
    """, (data['name'], data['email'], data['course'],
          data['gender'], data['review'], id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student Updated Successfully"})


# -----------------------
# DELETE STUDENT
# -----------------------
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student Deleted Successfully"})


if __name__ == '__main__':
    app.run(debug=True)