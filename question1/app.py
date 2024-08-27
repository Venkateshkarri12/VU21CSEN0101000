from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Configuration
AUTH_URL = "http://20.244.56.144/test/auth"
PRODUCTS_URL_TEMPLATE = "http://20.244.56.144/test/companies/{company}/categories/{category}/products"
AUTH_PAYLOAD = {
    "companyName": "Gitam",
    "clientID": "10378cea-0c47-4d83-aa0a-28cfef0dae10",
    "clientSecret": "gGuWylzKfvTDuuyd",
    "ownerName": "Venkatesh",
    "ownerEmail": "vkarri4@gitam.in",
    "rollNo": "VU21CSEN0101000"
}

# In-memory token storage
token_info = {
    "access_token": None,
    "expires_in": None
}

def get_token():
    response = requests.post(AUTH_URL, json=AUTH_PAYLOAD)
    if response.status_code == 200:
        data = response.json()
        token_info["access_token"] = data["access_token"]
        token_info["expires_in"] = data["expires_in"]
    else:
        raise Exception("Failed to fetch token")

@app.route('/products', methods=['GET'])
def get_products():
    company = request.args.get('company')
    category = request.args.get('category')
    top = request.args.get('top')
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')

    if not all([company, category, top, min_price, max_price]):
        return jsonify({"error": "Missing required query parameters"}), 400

    # Fetch token if not available or expired
    if not token_info["access_token"]:
        # get_token()
        pass

    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzI0NzQzNzU4LCJpYXQiOjE3MjQ3NDM0NTgsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjEwMzc4Y2VhLTBjNDctNGQ4My1hYTBhLTI4Y2ZlZjBkYWUxMCIsInN1YiI6InZrYXJyaTRAZ2l0YW0uaW4ifSwiY29tcGFueU5hbWUiOiJHaXRhbSIsImNsaWVudElEIjoiMTAzNzhjZWEtMGM0Ny00ZDgzLWFhMGEtMjhjZmVmMGRhZTEwIiwiY2xpZW50U2VjcmV0IjoiZ0d1V3lsektmdlREdXV5ZCIsIm93bmVyTmFtZSI6IlZlbmthdGVzaCIsIm93bmVyRW1haWwiOiJ2a2Fycmk0QGdpdGFtLmluIiwicm9sbE5vIjoiVlUyMUNTRU4wMTAxMDAwIn0.D-5t3517208rrN8gHDg-0zo7mJt21SHdlwvklGo2gdQ"
    }

    products_url = PRODUCTS_URL_TEMPLATE.format(company=company, category=category)
    params = {
        "top": top,
        "minPrice": min_price,
        "maxPrice": max_price
    }

    response = requests.get(products_url, headers=headers, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch products"}), response.status_code

@app.route('/categories/<categoryname>/products', methods=['GET'])
def get_products_by_category(categoryname):
    company = request.args.get('company')
    top = request.args.get('top')
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')

    if not all([company, top, min_price, max_price]):
        return jsonify({"error": "Missing required query parameters"}), 400

    # Fetch token if not available or expired
    if not token_info["access_token"]:
        get_token()

    headers = {
        "Authorization": f"Bearer {token_info['access_token']}"
    }

    products_url = PRODUCTS_URL_TEMPLATE.format(company=company, category=categoryname)
    params = {
        "top": top,
        "minPrice": min_price,
        "maxPrice": max_price
    }

    response = requests.get(products_url, headers=headers, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch products"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
