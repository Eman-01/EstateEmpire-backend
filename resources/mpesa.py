import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth

class Mpesa:
    def __init__(self):
        self.consumer_key = "Gz9yMno47qs7qJsTitdZnos5nmCxCWi0yuWtkjWpAG4mArPn"
        self.consumer_secret = "SrsAo1XkrwTgco7HlerzKQVNnfj3z5SX8JJAGSii90SgFamOhKrlAjMrBtK1GoWm"
        self.shortcode = 174379
        self.passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    def get_access_token(self):
        try:
            api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
            response = requests.get(api_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.RequestException as e:
            print("Error getting access token:", str(e))
            raise Exception("Failed to get access token from M-Pesa API")

    def _get_password(self, timestamp):
        password = f"{self.shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(password.encode()).decode()

    def stk_push(self, phone_number, amount, transaction_desc):
        try:
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
                "AccountReference": "EstateEmpire",
                "TransactionDesc": transaction_desc
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print("Error in stk_push:", str(e))
            return {"error": str(e), "status_code": 500}