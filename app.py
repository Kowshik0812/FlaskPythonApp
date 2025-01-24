from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

# Database connection
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

# Route to fetch data from Students table
@app.route('/students', methods=['GET'])
def get_students():
    query = "SELECT * FROM Students"
    cursor.execute(query)
    rows = cursor.fetchall()
    students = [{"ID": row[0], "Name": row[1], "Age": row[2]} for row in rows]
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
