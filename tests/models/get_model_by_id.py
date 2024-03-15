import requests
import json

# Add the BASE_URL if not already defined
BASE_URL = 'http://localhost:5000'

# Function to register a new user
def register(email, password, username):
    url = f'{BASE_URL}/auth/register'
    data = {
        'email': email,
        'password': password,
        'username': username
    }
    response = requests.post(url, json=data)
    return response

# Function to login an existing user
def login(username, password):
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    return response

# Function to get all models
def get_all_models(token):
    url = f'{BASE_URL}/model/get_all_models'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response

# Function to get a model by its ID
def get_model_by_id(token, model_id):
    url = f'{BASE_URL}/model/get_model_by_id/{model_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response

if __name__ == '__main__':
   # Test user registration and login
    email = "arsenal@gmail.com"
    password = "arsenal"
    username = "arsenalfirst"

    registration_response = register(email, password, username)

    login_response = login(username, password)

    jwt_token = login_response.json().get('access_token')

    # Test fetching all models
    all_models_response = get_all_models(jwt_token)
    print('All Models (Response):', all_models_response.json())

    # # Test fetching a model by its ID
    # # Assuming model_id is 1 for testing purposes
    model_id_to_fetch = 2
    model_by_id_response = get_model_by_id(jwt_token, model_id_to_fetch)
    print('Model by ID (Response):', model_by_id_response.json())
