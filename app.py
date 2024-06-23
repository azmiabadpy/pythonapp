from flask import Flask, render_template, jsonify, request
import pymysql
import os

app = Flask(__name__)

# Database connection function
def connect_to_db():
    try:
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME']
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Create table function (for demonstration)
def create_table():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL
                )
            """)
            print("Table 'users' created successfully")
            cursor.close()
        except pymysql.MySQLError as e:
            print(f"Error creating table: {e}")
        finally:
            connection.close()

# API endpoint to fetch database name
@app.route('/api/database', methods=['GET'])
def get_database_name():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()[0]
            cursor.close()
            return jsonify({'database_name': database_name}), 200
        except pymysql.MySQLError as e:
            return jsonify({'error': str(e)}), 500
        finally:
            connection.close()
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

# API endpoint to handle form submission and store data in database
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and Email are required'}), 400

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            connection.commit()
            cursor.close()
            return jsonify({'message': 'Data stored successfully'}), 200
        except pymysql.MySQLError as e:
            return jsonify({'error': str(e)}), 500
        finally:
            connection.close()
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

# API endpoint to fetch all users from the database
@app.route('/api/users', methods=['GET'])
def get_users():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            cursor.close()

            # Convert database rows to a list of dictionaries
            users_list = []
            for user in users:
                user_dict = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2]
                }
                users_list.append(user_dict)

            return jsonify({'users': users_list}), 200
        except pymysql.MySQLError as e:
            return jsonify({'error': str(e)}), 500
        finally:
            connection.close()
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

# Render index.html template for adding and viewing data
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    create_table()  # Create 'users' table if it doesn't exist
    app.run(host='0.0.0.0', port=80)

