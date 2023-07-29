import requests,json

url = "https://api.mercury.com/api/v1/account/efe79804-e534-11ed-89d7-bb9ff4bf2c36/transactions?limit=500&offset=0"

headers = {
  'Authorization': 'Bearer secret-token:mercury_production_rma_J9eitYeay6JH3UidqkaprDu7Ktu5HEqKFGdZuEwLo1Txi_yrucrem',  # Replace YOUR_BEARER_TOKEN with your actual bearer token
  'accept': 'application/json',
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    transactions = json.loads(response.text)
    for trans in transactions.get('transactions'):
        print(trans,"_______")
        break

