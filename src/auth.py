# src/auth.py

from utils import read_config

def check_credentials(username, password):
    config = read_config()
    stored_username = config['AUTH']['username']
    stored_password = config['AUTH']['password']
    return username == stored_username and password == stored_password