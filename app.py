from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('products.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL
    )
''')
conn.commit()

@app.route('/products', methods=['GET'])
def get_products():
    
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    result = [{'id': row[0], 'name': row[1], 'description': row[2], 'price': row[3]} for row in products]

    return jsonify(result)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    if product:
        result = {'id': product[0], 'name': product[1], 'description': product[2], 'price': product[3]}
        return jsonify(result)

    return jsonify({'message': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def add_product():

    data = request.get_json()
    cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', (data['name'], data['description'], data['price']))
    conn.commit()

    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
   
    data = request.get_json()
    cursor.execute('UPDATE products SET name=?, description=?, price=? WHERE id=?',
                   (data['name'], data['description'], data['price'], product_id))
    conn.commit()

    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()

    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
