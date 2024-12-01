from plaid import Configuration, ApiClient
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
import os

def get_plaid_client():
    configuration = Configuration(
        host=Configuration.Sandbox,  # Change to Configuration.Production in production
        api_key={
            'clientId': os.getenv('674baed10feadb0019e09fa5'),
            'secret': os.getenv('d90fb3b19d7856b3f5b387fa30823f'),
        }
    )
    
    api_client = ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    return client
