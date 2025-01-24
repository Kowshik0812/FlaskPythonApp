from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Database connection setup
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=studentdbserverr.database.windows.net;'
    'DATABASE=StudentDB;'
    'UID=adminuser;'
    'PWD=Kowshik@123'

)
cursor = conn.cursor()

@app.route('/')
def home():
    return "Hello, Azure Flask App with SQL!"

# Route to fetch all students from the database
@app.route('/students', methods=['GET'])
def get_students():
    query = "SELECT * FROM Students"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Convert the rows into a list of dictionaries
    students = [{"ID": row[0], "Name": row[1], "Age": row[2]} for row in rows]
    return jsonify(students)

# Route to fetch a student by ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    query = "SELECT * FROM Students WHERE ID = ?"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    
    if row:
        student = {"ID": row[0], "Name": row[1], "Age": row[2]}
        return jsonify(student)
    else:
        return jsonify({"message": "Student not found"}), 404

# Route to create a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    query = "INSERT INTO Students (ID, Name, Age) VALUES (?, ?, ?)"
    cursor.execute(query, (data['ID'], data['Name'], data['Age']))
    conn.commit()
    return jsonify({"message": "Student added successfully!"}), 201

# Route to update student information
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json
    query = "UPDATE Students SET Name = ?, Age = ? WHERE ID = ?"
    cursor.execute(query, (data['Name'], data['Age'], id))
    conn.commit()

    if cursor.rowcount > 0:
        return jsonify({"message": "Student updated successfully!"})
    else:
        return jsonify({"message": "Student not found"}), 404

# Route to delete a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    query = "DELETE FROM Students WHERE ID = ?"
    cursor.execute(query, (id,))
    conn.commit()

    if cursor.rowcount > 0:
        return jsonify({"message": "Student deleted successfully!"})
    else:
        return jsonify({"message": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)



