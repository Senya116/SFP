from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from generate_qr_codes import products

app = Flask(__name__)

# Пример базы данных
fridge = []
shopping_list = []
custom_list = []

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    product = next((p for p in products if p['name'] == data['name']), None)
    if product:
        fridge.append(product)
        print(f"Product added to fridge: {product}")  # Отладочное сообщение
        return jsonify({"message": "Product added"}), 201
    else:
        return jsonify({"message": "Product not found in database"}), 404

@app.route('/remove_product', methods=['POST'])
def remove_product():
    data = request.json
    global fridge
    fridge = [product for product in fridge if product['name'] != data['name']]
    return jsonify({"message": "Product removed"}), 200

@app.route('/remove_product_by_qr', methods=['POST'])
def remove_product_by_qr():
    data = request.json
    global fridge
    for i, product in enumerate(fridge):
        if product['name'] == data['name']:
            del fridge[i]
            return jsonify({"message": "Product removed by QR code"}), 200
    return jsonify({"message": "Product not found in fridge"}), 404

@app.route('/get_fridge', methods=['GET'])
def get_fridge():
    print(f"Fridge contents: {fridge}")  # Отладочное сообщение
    return jsonify(fridge), 200

@app.route('/get_product', methods=['GET'])
def get_product():
    name = request.args.get('name')
    product = next((product for product in products if product['name'] == name), None)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"message": "Product not found"}), 404

@app.route('/add_to_shopping_list', methods=['POST'])
def add_to_shopping_list():
    data = request.json
    existing_product = next((product for product in shopping_list if product['name'] == data['name']), None)
    if existing_product:
        existing_product['quantity'] += int(data['quantity'])
    else:
        shopping_list.append(data)
    print(f"Product added to shopping list: {data}")  # Отладочное сообщение
    return jsonify({"message": "Product added to shopping list"}), 201

@app.route('/remove_from_shopping_list', methods=['POST'])
def remove_from_shopping_list():
    data = request.json
    global shopping_list
    shopping_list = [product for product in shopping_list if product['name'] != data['name']]
    return jsonify({"message": "Product removed from shopping list"}), 200

@app.route('/get_shopping_list', methods=['GET'])
def get_shopping_list():
    return jsonify(shopping_list), 200

@app.route('/add_to_custom_list', methods=['POST'])
def add_to_custom_list():
    data = request.json
    custom_list.append(data)
    print(f"Product added to custom list: {data}")  # Отладочное сообщение
    return jsonify({"message": "Product added to custom list"}), 201

@app.route('/remove_from_custom_list', methods=['POST'])
def remove_from_custom_list():
    data = request.json
    global custom_list
    custom_list = [product for product in custom_list if product['name'] != data['name']]
    return jsonify({"message": "Product removed from custom list"}), 200

@app.route('/get_custom_list', methods=['GET'])
def get_custom_list():
    return jsonify(custom_list), 200

@app.route('/analytics', methods=['GET'])
def analytics():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # Логика для анализа потребления
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    analytics_data = [product for product in fridge if start <= datetime.strptime(product['expiry_date'], '%Y-%m-%d') <= end]
    return jsonify(analytics_data), 200

@app.route('/notifications', methods=['GET'])
def notifications():
    today = datetime.now()
    notifications = []
    for product in fridge:
        expiry_date = datetime.strptime(product['expiry_date'], '%Y-%m-%d')
        if (expiry_date - today).days <= 3:
            notifications.append({
                'name': product['name'],
                'expiry_date': product['expiry_date'],
                'status': 'Expiring soon' if (expiry_date - today).days > 0 else 'Expired'
            })
    return jsonify(notifications), 200

if __name__ == '__main__':
    app.run(debug=True)
