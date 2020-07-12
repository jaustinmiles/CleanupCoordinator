import json
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import DRIVE_TYPE, DRIVE_PROJECT_ID, DRIVE_PRIVATE_KEY_ID, DRIVE_PRIVATE_KEY, DRIVE_CLIENT_EMAIL, \
    DRIVE_CLIENT_ID, DRIVE_AUTH_URI, DRIVE_TOKEN_URI, DRIVE_AUTH_PROVIDER_CERT, DRIVE_CLIENT_CERT


def get_google_creds():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = {
        "type": DRIVE_TYPE,
        "project_id": DRIVE_PROJECT_ID,
        "private_key_id": DRIVE_PRIVATE_KEY_ID,
        "private_key": DRIVE_PRIVATE_KEY,
        "client_email": DRIVE_CLIENT_EMAIL,
        "client_id": DRIVE_CLIENT_ID,
        "auth_uri": DRIVE_AUTH_URI,
        "token_uri": DRIVE_TOKEN_URI,
        "auth_provider_x509_cert_url": DRIVE_AUTH_PROVIDER_CERT,
        "client_x509_cert_url": DRIVE_CLIENT_CERT
    }
    with open('temp_client_key.json', 'w') as keyfile:
        json.dump(creds_dict, keyfile)
    creds = ServiceAccountCredentials.from_json_keyfile_name('temp_client_key.json', scope)
    client = gspread.authorize(creds)
    os.remove('temp_client_key.json')
    return client
