import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth

class Mpesa:
    def __init__(self):
        self.consumer_key = "Gz9yMno47qs7qJsTitdZnos5nmCxCWi0yuWtkjWpAG4mArPn"  # Replace with your M-Pesa consumer key
        self.consumer_secret = "SrsAo1XkrwTgco7HlerzKQVNnfj3z5SX8JJAGSii90SgFamOhKrlAjMrBtK1GoWm"  # Replace with your M-Pesa consumer secret
        self.shortcode = 174379  # Replace with your M-Pesa shortcode
        self.passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'  # Replace with your Lipa na M-Pesa passkey

    def get_access_token(self):
        api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        response = requests.get(api_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))

        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print("M-Pesa Access Token Response:", response.text)  # Log the response
            raise Exception("Failed to get access token from M-Pesa API")

    def _get_password(self, timestamp):
        # Password is base64 encoded combination of shortcode, passkey and timestamp
        from base64 import b64encode
        password = f"{self.shortcode}{self.passkey}{timestamp}"
        return b64encode(password.encode()).decode()

    def stk_push(self, phone_number, amount, transaction_desc):
        access_token = self.get_access_token()
        url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = self._get_password(timestamp)

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            'PhoneNumber': phone_number,
            "CallBackURL": "https://mydomain.com/path",  # Replace with your callback URL
            "AccountReference": "EstateEmpire",  # Description of the transaction
            "TransactionDesc": transaction_desc
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("M-Pesa STK Push Response:", response.text)  # Log the response
            return {"error": response.json(), "status_code": response.status_code}
