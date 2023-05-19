import requests


def get_access_token(client_id, client_secret):
    url = 'https://api.moltin.com/oauth/access_token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }

    response = requests.post(url, data=payload)
    return response.json()['access_token']


def get_products(token):
    url = 'https://api.moltin.com/pcm/products'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    products = response.json()['data']
    return products


def get_product_by_id(token, product_id):
    url = f'https://api.moltin.com/pcm/products/{product_id}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    product_content = response.json()['data']
    return product_content


def create_cart(token, user_id):
    url = 'https://api.moltin.com/v2/carts'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'data': {
            'name': str(user_id),
            'description': 'For a fish',
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    cart_content = response.json()['data']
    return cart_content


def get_cart_content(token, reference):
    url = f'https://api.moltin.com/v2/carts/{reference}'
    headers = {
        'Authorization': f'Bearer {token}',
        }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    cart_content = response.json()['data']
    return cart_content


def add_product_to_cart(token, cart_reference, product_id, quantity):
    url = f'https://api.moltin.com/v2/carts/{cart_reference}/items'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'data': {
            'id': product_id,
            'type': 'cart_item',
            'quantity': quantity,
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()


def get_cart_products(token, reference):
    url = f'https://api.moltin.com/v2/carts/{reference}/items'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    cart_products = response.json()['data']
    return cart_products


def remove_item_from_cart(token, cart_reference, item_id):
    url = f'https://api.moltin.com/v2/carts/{cart_reference}/items/{item_id}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()


def get_price_book(token, pricebook_id):
    url = f'https://api.moltin.com/pcm/pricebooks/{pricebook_id}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    pricebook_content = response.json()
    return pricebook_content


def get_product_price(token, pricebook_id, product_price_id):
    url = f'https://api.moltin.com/pcm/pricebooks/{pricebook_id}/prices/{product_price_id}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    produce_price = response.json()
    return produce_price


def get_all_prices(token, pricebook_id):
    url = f'https://api.moltin.com/pcm/pricebooks/{pricebook_id}/prices'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    prices_content = response.json()
    return prices_content


def get_product_image(token, product_id):
    url = f'https://api.moltin.com/pcm/products/{product_id}/relationships/main_image'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    image_relationships = response.json()['data']
    return image_relationships


def get_image_link(token, image_id):
    url = f'https://api.moltin.com/v2/files/{image_id}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    image_content = response.json()['data']
    image_link = image_content['link']['href']
    return image_link


def get_all_carts(token):
    url = 'https://api.moltin.com/v2/carts'
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    return response.json()


def create_customer(token, user_id, email):
    url = 'https://api.moltin.com/v2/customers'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'data': {
            'type': 'customer',
            'name': user_id,
            'email': email,
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['data']


def get_customer_by_id(token, customer_id):
    url = f'https://api.moltin.com/v2/customers/{customer_id}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']
