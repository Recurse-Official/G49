# backend/utils/plaid_client.py
from plaid import Client
from flask import current_app

def get_plaid_client():
    config = current_app.config
    client = Client(
        client_id=config.PLAID_CLIENT_ID,
        secret=config.PLAID_SECRET,
        environment=config.PLAID_ENV,
    )
    return client
