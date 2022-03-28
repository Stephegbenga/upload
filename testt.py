from rq import Worker, Queue
import os
import requests
from time import sleep
import json

def token():
    try:
        url = "https://api.malfini.com/api/v4/api-auth/login"

        payload = json.dumps({
            "username": "baseshirt",
            "password": "2018BVBsebbe!!!"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        # print(response)
        token = response['access_token']
        return token
    except:
        sleep(2)
        url = "https://api.malfini.com/api/v4/api-auth/login"

        payload = json.dumps({
            "username": "baseshirt",
            "password": "2018BVBsebbe!!!"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        # print(response)
        token = response['access_token']
        return token


def uploadproducts(product):
    url = "https://richtiger-kevin.myshopify.com/admin/api/2021-10/products.json"

    payload = json.dumps({"product":product})
    headers = {
        'X-Shopify-Access-Token': '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',
        'Content-Type': 'application/json'
    }
    responses = requests.request("POST", url, headers=headers, data=payload).json()
    # pprint(responses)
    productdetails = {"product_id":responses['product']['id'], "code":product['code']}
    # print(productdetails)
    return (productdetails)


def getmalfiniprice(productSizeCode):
    tokenn = token()
    url = "https://api.malfini.com/api/v4/product/prices"
    payload = {}
    headers = {
        'Authorization': f'Bearer {tokenn}'
    }
    responses = requests.request("GET", url, headers=headers, data=payload).json()
    for response in responses:
        if response['productSizeCode'] == productSizeCode and response['limit'] == 1:
            product_price = response['price']
            return product_price

# Variant Uploader Function
def variantuploader(variantBody, product_id):
    url = f"https://richtiger-kevin.myshopify.com/admin/api/2021-10/products/{product_id}/variants.json"
    payload = json.dumps({
        "variant": variantBody
    })
    headers = {
        'X-Shopify-Access-Token': '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',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)
    return "Success"


# Getting Variant
def uploadvariant(productdetails):
    url = "https://api.malfini.com/api/v4/product"
    tokenn = token()
    variantBody = {}
    payload = {}
    headers = {
        'Authorization': f'Bearer {tokenn}'
    }
    responses = requests.request("GET", url, headers=headers, data=payload).json()
    for response in responses:
        if response['code'] == productdetails['code']:
            variants = response['variants']
            for variant in variants:
                # print(f"This is Variant {variant}")
                image_link = variant['images'][0]['link']
                image_id = uploadimage(image_link, productdetails['product_id'])
                for variantss in variant['nomenclatures']:
                    # print(f"This is Variant {variantss}")
                    variantBody['option1'] = f"{variant['name']} {variantss['sizeName']}"
                    variantBody['weight'] = variantss['grossWeight']
                    variantBody['sku'] = variantss['productSizeCode']
                    variantBody['price'] = getmalfiniprice(variantss['productSizeCode'])
                    variantBody['image_id'] = image_id
                    variantBody['inventory_managment'] = True
                    uploaded = variantuploader(variantBody, productdetails['product_id'])


def uploadimage(image_link, product_id):

    url = f"https://richtiger-kevin.myshopify.com/admin/api/2021-10/products/{product_id}/images.json"

    payload = json.dumps({
        "image": {
            "src": image_link
        }
    })
    headers = {
        'X-Shopify-Access-Token': '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',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    # print(response)
    return response['image']['id']









def getinventorydata(inventory_item_id):
    url = f"https://richtiger-kevin.myshopify.com/admin/api/2022-01/inventory_levels.json?inventory_item_ids={inventory_item_id}"

    payload = {}
    headers = {
        'X-Shopify-Access-Token': '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'
    }
    response = requests.request("GET", url, headers=headers, data=payload).json()
    # print(response)
    return response['location_id']


def setinventoryquantity(inventory_item_id, location_id, quantity):
    url = "https://richtiger-kevin.myshopify.com/admin/api/2022-01/inventory_levels/set.json"

    payload = json.dumps({
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": quantity
    })
    headers = {
        'X-Shopify-Access-Token': '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',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    # print(response)
    return response

def getavailabilities(productSizeCode):
    tokenn = token()
    url = "https://api.malfini.com/api/v4/product/availabilities"
    payload={}
    headers = {
      'Authorization': f'Bearer {tokenn}'
    }
    responses = requests.request("GET", url, headers=headers, data=payload).json()
    # print(responses)
    for response in responses:
        if response['productSizeCode'] == productSizeCode:
            return response['quantity']


def getallshopifyproductandupdatequantity():
    url = "https://richtiger-kevin.myshopify.com/admin/api/2021-10/products.json"
    payload = {}
    headers = {
        'X-Shopify-Access-Token': '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'
    }
    responses = requests.request("GET", url, headers=headers, data=payload).json()
    # print(responses)
    for response in responses['products']:
        for variants in response['variants']:
            productSizeCode = variants['sku']
            inventory_item_id = variants['inventory_item_id']
            print(productSizeCode)
            if productSizeCode == None:
                print("The Sku is Empty")
            else:
                location_id = getinventorydata(inventory_item_id)
                quantity = getavailabilities(productSizeCode)
                setinventoryquantity(inventory_item_id, location_id, quantity)

def alertme():
    url = "https://script.google.com/macros/s/AKfycbwkDCT5QIorhA7-H3las9z4mWBBNeP5J741bDBcQ_R4fAnKX8TlGZhnBDQljTbGHCJZ/exec?message=All products and Inventory has been updated Successfully&email=stephengbenga300@gmail.com&subject=Malfini Api BaseShirt"

    payload = {}
    headers = {
        'Cookie': 'NID=511=R8zd0zIjmwOU4uTwDyd3ZBu7KrEv4rwQZIg3QM8QbVZEzeFcnbr-1DSlutgPj03fzYZmRvUMZqp-B7H1aTuy5sADwh6EvcFLoLkxp0cm8m-6OjclFst0hL6QBGE9p9tOZUfZkTb0h17_XbPSYGmP63N7Ikof1zrYU_8MXI6ftwI'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.json())


product = {}
product['options'] = {}
variantmainname = ""
variantBody = {}
variantBodyenclose = []
variant_prop = []


url = "https://api.malfini.com/api/v4/product"
tokenn = token()
payload={}
headers = {
  'Authorization': f'Bearer {tokenn}'
}
tttt = requests.request("GET", url, headers=headers, data=payload).json()

for x in tttt:
    for allvariants in x:
        os.system('clear')
        product['body_html'] = f"<ul><li>{x['specification']}</li>\n<li>{x['description']}</li></ul>"
        if x['subtitle'] == None:
            product['title'] = x['name']
        else:
            product['title'] = f"{x['name']} {x['subtitle']}"
        product['vendor'] = "malfini"
        product['code'] = x['code']
        product['options']['name'] = "Farbe"
        product['type'] = x['type']
        # pprint(product)
        resu = uploadproducts(product)
        uploadvariant(resu)

getallshopifyproductandupdatequantity()
alertme()

if __name__ == '__main__':
    worker = Worker(Queue)
    worker.work()
