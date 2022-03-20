from flask import Flask, request
import phonenumbers
from decouple import config
from pprint import pprint
import requests
import hashlib
import base64
import hmac
import json

user_name = config('user_name')
password = config('password')
shopkey = config('shopkey')

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
    datatoken = accesstoken().json()
    token = datatoken['access_token']
    print(token)
    url = "https://api.malfini.com/api/v4/address"
    phonenumberprefix = phonenumbers.parse("100993393939", countrycode).country_code
    phonenumber = f'+{phonenumberprefix}-{phoneno}'
    payload = json.dumps({
        "name": name,
        "recipient": name,
        "street": street, #"test_street"
        "countryCode": countrycode,#"DE"
        "zipCode": f"{zipcode}", #"65929",
        "city": city, #"test city 2",
        "phone": phonenumber, #"+1-8722717528",
        "email": email, #"testing01@xample.com",
        "invoiceDeliveryId": 2,
        "isValid": True
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)
    return response['id']



@app.route('/ordercreate', methods=['POST'])
def ordercreation():
    data = request.get_json()
    print(data)
    products = []
    addressid = createaddress(data['shipping_address']['name'], data['shipping_address']['address1'], data['shipping_address']['country_code'], data['shipping_address']['zip'], data['shipping_address']['city'], data['shipping_address']['phone'], data['email'])
    print(addressid)
    lineitems = data['line_items']
    for lineitem in lineitems:
        quantity = lineitem['quantity']
        sku = lineitem['sku']
        qusku = {"productSizeCode":sku, "count":quantity}
        products.append(qusku)

    token = accesstoken().json()['access_token']
    print(token)
    url = "https://api.malfini.com/api/v4/order"
    payload = json.dumps({
        "invoiceDeliveryTypeId": 3,
        "addressId": int(addressid),
        "deliveryId": 75,
        "paymentId": 9,
        "customOrderId": f"{data['id']}",
        "products": products
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    return "Success"

@app.route('/5168649663:AAHe5Qq2wx4y3V_3MQ7ci3klc7ZKkTJ8kQM')
def tgwebhook():
    data = request.get_json()
    print(data)
    return "success"


if __name__ == '__main__':
    app.run()
