input_data = {"customer_name":"MODERN RECOVEsRYs",
              "amount":100000}

from datetime import datetime
import requests,json

customer_name = input_data.get('customer_name')
item_name = input_data.get('customer_name')

payment_mode = "Bank Transfer"
amount = input_data.get('amount')

# Get access token_____________
url = "https://accounts.zoho.com/oauth/v2/token"
payload = {
    'client_id': '1000.L4314NHQK3N8FTBKI9PAV2UI92D19F',
    'client_secret': '3298258a7846c19b693de81388d493d44b06018340',
    'grant_type': 'refresh_token',
    'refresh_token': '1000.df3c22a447429c0b002841aa04df40a5.56a47ec5ca91f39f2767d35da1ce92a7',
    'scope': 'ZohoBooks.fullaccess.all'
}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(url, headers=headers, data=payload)
token = response.json().get('access_token')
# End Token____________________

Zoho_headers = {'Authorization': f'Zoho-oauthtoken {token}', 'content-type': 'application/json'}


url = "https://api.mercury.com/api/v1/account/efe79804-e534-11ed-89d7-bb9ff4bf2c36/transactions?limit=500&offset=0"
Mercury_headers = {
  'Authorization': 'Bearer secret-token:mercury_production_rma_J9eitYeay6JH3UidqkaprDu7Ktu5HEqKFGdZuEwLo1Txi_yrucrem',
  'accept': 'application/json',
}

current_date = datetime.now().date()
formatted_date = current_date.strftime("%Y-%m-%d")

# Static____
# formatted_date="2023-06-28"
# Remove Static_____

# Get Current date time
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

response = requests.get(url, headers=Mercury_headers)
if response.status_code == 200:
    transactions = json.loads(response.text)
    for trans in transactions.get('transactions'):
        Created_date = str(trans.get('createdAt')).split('T')[0]
        if formatted_date == Created_date:
            dt = str(trans.get('createdAt'))

            # Get Records that were created in one hour.
            dates = dt.replace('T',' ').split('.')[0]
            Mercury_Time = dates.split(' ')[1]
            Current_time = str(formatted_datetime).split(' ')[1]
            Mercury_Hours = Mercury_Time.split(':')[0]
            Mercury_Minutes = Mercury_Time.split(':')[1]
            Current_Hours = Current_time.split(':')[0]
            Current_Minutes = Current_time.split(':')[1]
            
            # Static_____
            # Mercury_Hours="1"
            # Current_HoursAdd = int(Current_Hours)-6
            # End______

            # if Mercury_Hours == Current_HoursAdd: # hours match
            Amount = trans.get('amount')
            Status = trans.get('status')
            BankDescription = trans.get('bankDescription')
            ExternalMemo = trans.get('externalMemo')
            Name = trans.get('counterpartyName')
            output = {"Name":Name}
            if '-' in str(Amount):
                pass
            else:
                # Get Customer and match
                print("Positive___")
                url = f"https://www.zohoapis.com/books/v3/contacts?search_text={customer_name}&organization_id=810961040"
                response = requests.request("GET", url, headers=Zoho_headers, data=payload)
                if response.status_code == 200:
                    contacts_Here = json.loads(response.text).get('contacts')
                    if len(contacts_Here)!=0:
                        for contacts in contacts_Here:
                            if contacts.get('customer_name') == customer_name:
                                customer_id = contacts.get('contact_id')
                                print(customer_id,"-----Customer is already created")  
                                output = {"ItemId":customer_id}
                            else:
                                # Create Customer
                                url = "https://www.zohoapis.com/books/v3/contacts?organization_id=810961040"
                                payload = json.dumps({"contact_name": customer_name})
                                response = requests.request("POST", url, headers=Zoho_headers, data=payload)
                                if response.status_code == 201:
                                    customer_id = response.json().get('contact').get('contact_id')
                                    print(customer_id,"-----Customer is created")
                                    output = {"ItemId":customer_id}
                    else:
                        # Create Customer
                        print("Create Else Part")
                        url = "https://www.zohoapis.com/books/v3/contacts?organization_id=810961040"
                        payload = json.dumps({"contact_name": customer_name})
                        response = requests.request("POST", url, headers=Zoho_headers, data=payload)
                        if response.status_code == 201:
                            customer_id = response.json().get('contact').get('contact_id')
                            print(customer_id,"-----Customer is created")
                            output = {"ItemId":customer_id}
    

                # Get Items and match
                url = f"https://www.zohoapis.com/books/v3/items?search_text={item_name}&organization_id=810961040"
                response = requests.request("GET", url, headers=Zoho_headers, data=payload)
                if response.status_code == 200:
                    Items_Here = json.loads(response.text).get('items')
                    if len(Items_Here)!=0:
                        for contacts in Items_Here:
                            if contacts.get('item_name') == item_name:
                                item_id = contacts.get('item_id')
                                print(item_id,"-----Item is already created")
                                output = {"ItemId":item_id}
                            else:
                                # Create Item
                                if '-' in str(amount):
                                    rate = str(amount).split('-')[1]
                                else:
                                    rate = amount
                                url = "https://www.zohoapis.com/books/v3/items?organization_id=810961040"
                                payload = json.dumps({"name": item_name, "rate": rate})
                                response = requests.post(url, headers=Zoho_headers, data=payload)
                                if response.status_code == 201:
                                    item_id = response.json().get('item').get('item_id')
                                    print(item_id,"----Item is created")
                                    output = {"ItemId":item_id}
                    else:
                        print("Else item is created here")
                        # Create Item
                        if '-' in str(amount):
                            rate = str(amount).split('-')[1]
                        else:
                            rate = amount
                        url = "https://www.zohoapis.com/books/v3/items?organization_id=810961040"
                        payload = json.dumps({"name": item_name, "rate": rate})
                        response = requests.post(url, headers=Zoho_headers, data=payload)
                        if response.status_code == 201:
                            item_id = response.json().get('item').get('item_id')
                            print(item_id,"----Item is created")
                            output = {"ItemId":item_id}
                
                
                # Create Invoice
                url = "https://www.zohoapis.com/books/v3/invoices?organization_id=810961040"
                payload = json.dumps({"customer_id": customer_id,"line_items": [{"item_id": item_id}]})
                print(payload,"_____")
                response = requests.post(url, headers=Zoho_headers, data=payload)
                if response.status_code == 201:
                    invoice_id = response.json().get('invoice').get('invoice_id')
                    Invoice_Number = response.json().get('invoice').get('invoice_number')
                    print("Invoice is created",Invoice_Number)

                # Create Payment
                current_date = datetime.now().strftime("%Y-%m-%d")
                url = "https://www.zohoapis.com/books/v3/customerpayments?organization_id=810961040"
                if '-' in str(amount):
                    amt = str(amount).split('-')[1]
                else:
                    amt = amount
                payload = json.dumps({
                    "customer_id": customer_id,
                    "payment_mode": payment_mode,
                    "amount": amt,
                    "date": current_date,
                    "invoices": [
                        {
                            "invoice_id": invoice_id,
                            "invoice_number":str(Invoice_Number)
                        }
                                ],
                    "invoice_id": invoice_id,
                })
                response = requests.post(url, headers=Zoho_headers, data=payload)
                payment_id = response.json().get('payment').get('payment_id')
                print(payment_id,"Payment is created")
                output = {"payment_id":payment_id}