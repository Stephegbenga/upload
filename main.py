from flask import Flask, request
from decouple import config
from pprint import pprint
from server import createorder
import requests
import hashlib
import base64
import hmac
import json

user_name = config('user_name')
password = config('password')
shopkey = config('shopkey')

print(user_name)
print(password)

app = Flask(__name__)

variant_token = "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"

def accesstoken():
    url = "https://api.malfini.com/api/v4/api-auth/login"

    payload = json.dumps({
        "username": user_name,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

# This creates an address of that user on Malfini
def createaddress(name, street, countrycode, zipcode, city, phoneno, email):
    token = accesstoken()
    url = "https://api.malfini.com/api/v4/address"

    payload = json.dumps({
        "name": name,
        "recipient": name,
        "street": street, #"test_street"
        "countryCode": countrycode,#"DE"
        "zipCode": zipcode, #"65929",
        "city": city, #"test city 2",
        "phone": phoneno, #"+1-8722717528",
        "email": email, #"testing01@xample.com",
        "invoiceDeliveryId": 3,
        "isValid": True
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)
    return response['id']



@app.route('/ordercreate', methods=['POST'])
def ordercreation():
    products = []
    data = request.get_json()
    lineitems = data['line_items']
    for lineitem in lineitems:
        quantity = lineitem['quantity']
        sku = lineitem['sku']
        qusku = {"productSizeCode":sku, "count":quantity}
        products.append(qusku)
    ordercode = createorder(data['id'], products)
    print(ordercode)

if __name__ == '__main__':
    app.run(debug=True,  port=8080)
