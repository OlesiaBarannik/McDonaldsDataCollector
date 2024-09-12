from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_data():
    """Load data from products.json file."""
    try:
        with open('products.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

products_data = load_data()


@app.route('/all_products/', methods=['GET'])
def get_all_products():
    """Return all products."""
    if not products_data:
        return jsonify({"error": "No data available"}), 404
    return jsonify(products_data)


@app.route('/products/<string:product_name>', methods=['GET'])
def get_product(product_name):
    """Return information about a specific product."""
    product = next((item for item in products_data if item['name'] == product_name), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route('/products/<string:product_name>/<string:product_field>', methods=['GET'])
def get_product_field(product_name, product_field):
    """Return a specific field of a product."""
    product = next((item for item in products_data if item['name'] == product_name), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    if product_field not in product:
        return jsonify({"error": "Field not found"}), 404
    return jsonify({product_field: product[product_field]})


if __name__ == "__main__":
    app.run(debug=True)
