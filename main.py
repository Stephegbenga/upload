from flask import Flask, request, abort
import hmac
import hashlib
import base64
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print(data)


if __name__ == '__main__':
    app.run(debug=True,  port=8080)
