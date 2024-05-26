from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import jwt
from functools import wraps
import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'inventory'

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'yoursecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

# Create
@app.route('/product', methods=['POST'])
@token_required
def create_product():
    data = request.get_json()
    name = data['name']
    description = data.get('description', '')
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO products (name, description, price) VALUES (%s, %s, %s)', (name, description, price))
    mysql.connection.commit()
    return jsonify({'message': 'Product created successfully!'}), 201

# Read
@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM products WHERE id = %s', (id,))
    product = cursor.fetchone()
    if product:
        return jsonify(product)
    return jsonify({'message': 'Product not found!'}), 404

# Update
@app.route('/product/<int:id>', methods=['PUT'])
@token_required
def update_product(id):
    data = request.get_json()
    name = data['name']
    description = data.get('description', '')
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE products SET name = %s, description = %s, price = %s WHERE id = %s', (name, description, price, id))
    mysql.connection.commit()
    return jsonify({'message': 'Product updated successfully!'}), 200

# Delete
@app.route('/product/<int:id>', methods=['DELETE'])
@token_required
def delete_product(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM products WHERE id = %s', (id,))
    mysql.connection.commit()
    return jsonify({'message': 'Product deleted successfully!'}), 200

# Search
@app.route('/products', methods=['GET'])
def search_products():
    query_params = request.args
    name = query_params.get('name')
    price = query_params.get('price')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM products WHERE"
    conditions = []
    params = []
    if name:
        conditions.append("name LIKE %s")
        params.append(f"%{name}%")
    if price:
        conditions.append("price = %s")
        params.append(price)
    if conditions:
        query += " AND ".join(conditions)
        cursor.execute(query, params)
    else:
        cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products)

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Could not verify!'}), 401

if __name__ == '__main__':
    app.run(debug=True)
