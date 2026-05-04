import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
NOTIFICATION_URL = os.getenv('NOTIFICATION_URL', 'http://notification:8005')
INVENTORY_URL = os.getenv('INVENTORY_URL', 'http://inventory:8006')
PRODUCT_URL = os.getenv('PRODUCT_URL', 'http://product:8002')

@app.route('/cart', methods=['GET'])
def cart():
    return jsonify({'items': []})

@app.route('/checkout', methods=['POST'])
def checkout():
    payload = request.get_json() or {}
    product_id = payload.get('product_id')
    if not product_id:
        return jsonify({'error': 'product_id is required'}), 400

    item = requests.get(f'{PRODUCT_URL}/products/{product_id}')
    if item.status_code != 200:
        return jsonify({'error': 'product not found'}), 404

    inventory = requests.post(f'{INVENTORY_URL}/reserve', json={'product_id': product_id})
    if inventory.status_code != 200:
        return jsonify({'error': 'inventory reservation failed'}), 409

    notify = requests.post(f'{NOTIFICATION_URL}/notify', json={'message': f'Order placed for product {product_id}'})
    if notify.status_code != 200:
        return jsonify({'warning': 'notification failed'}), 202

    return jsonify({'status': 'checkout complete', 'product': item.json()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
