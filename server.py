from main import *

def createorder(customerid, products):
    token = accesstoken().json()['access_token']
    url = "https://api.malfini.com/api/v4/order"
    payload = json.dumps({
        "invoiceDeliveryTypeId": 3,
        "addressId": 157441,
        "deliveryId": 75,
        "paymentId": 9,
        "customOrderId": customerid,
        "products": products
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response

