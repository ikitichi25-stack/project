from flask import Flask, jsonify, request

app = Flask(__name__)
stock = {
    1: 10,
    2: 5,
    3: 25
}

@app.route('/stock', methods=['GET'])
def get_stock():
    return jsonify({ 'stock': stock }), 200

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    if product_id not in stock:
        return jsonify({ 'error': 'unknown product' }), 404
    if stock[product_id] <= 0:
        return jsonify({ 'error': 'out of stock' }), 409
    stock[product_id] -= 1
    return jsonify({ 'status': 'reserved', 'product_id': product_id, 'remaining': stock[product_id] }), 200

@app.route('/release', methods=['POST'])
def release():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    if product_id not in stock:
        return jsonify({ 'error': 'unknown product' }), 404
    stock[product_id] += 1
    return jsonify({ 'status': 'released', 'product_id': product_id, 'remaining': stock[product_id] }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
