

from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)



# Database configuration
# db_config = {
#     'user': 'root',
#     'password': '9930',
#     'host': 'localhost',
#     'database': 'test_db'
# }

# Database configuration
db_config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '9930'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'test_db')
}

# Create a database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# CRUD Operations
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, description, quantity) VALUES (%s, %s, %s)',
                   (data['name'], data['description'], data['quantity']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Item created!'}), 201

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items WHERE id = %s', (id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(item)

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET name = %s, description = %s, quantity = %s WHERE id = %s',
                   (data['name'], data['description'], data['quantity'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Item updated!'})

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Item deleted!'})



def check_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("-------------------------------------------------------------------------------------------Successfully connected to MySQL database")
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Tables in the database: {tables}")
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")

if __name__ == '__main__':
    check_db_connection()
    app.run(host='0.0.0.0', port=5000, debug=True)


