import paystack, ebills, requests, os, secrets
from ebills import Verify
from pprint import pprint
from dotenv import load_dotenv
from paystack import DedicatedVirtualAccount


ebills.username="Ecode2"
ebills.password="Elias_code11"

load_dotenv(override=True)

paystack.api_key = os.getenv("API_AUTH_KEY")

""" response = requests.post(url='http://localhost:8000/api/v1/bills/plan',
            headers={"accept": "application/json", 
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTM5ODI4MDQuMzIwNjg1LCJzdWIiOiJqb2huZG9lIn0.8R33YobQ1lCm7DiGReFus7xkpFVrQCMcCsYTZFULWeU",
                "Content-Type": "application/json"}, 
            json={
                "bill_type": "electric",
                "brand": "IBEDC"
            }
)

print(response.json()) """

#response = Airtime.buy({"phone": "09060636536", "network_id": "mtn", "amount": 200})
#response = Verify.verify({"customer_id": "23300112309", "service_id": "ibadan-electric", "variation_id": "prepaid"})

#pprint( response )

""" response= DedicatedVirtualAccount.create(customer="CUS_hiz3uxycoa5ewrb", preferred_bank="test-bank")

print(response) """

""" print(secrets.token_urlsafe(32)) """