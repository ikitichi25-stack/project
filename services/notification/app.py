from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json() or {}
    message = data.get('message')
    if not message:
        return jsonify({'error': 'message required'}), 400
    print(f'Notification requested: {message}')
    return jsonify({'status': 'notification queued', 'message': message}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)
