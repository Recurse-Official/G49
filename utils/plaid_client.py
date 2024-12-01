# backend/utils/plaid_client.py
from plaid import Client
from flask import current_app

def get_plaid_client():
    config = current_app.config
    client = Client(
        client_id=config["674baed10feadb0019e09fa5"],
        secret=config["d90fb3b19d7856b3f5b387fa30823f"],
        environment="sandbox",
    )
    return client
