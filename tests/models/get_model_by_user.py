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



def get_models_by_user(token):
    url = f'{BASE_URL}/model/model_by_user'
    headers = {'Authorization': f'Bearer {token}'}

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Print the response details for debugging
    print("Get Models by User (Status Code):", response.status_code)
    print("Get Models by User (Response Content):", response.content)  # or response.text for decoded content
    return response





if __name__ == '__main__':
    # Test user registration and login
    email = "arsenal@gmail.com"
    password = "arsenal"
    username = "arsenalfirst"

    registration_response_success = register(email, password, username)
    # print('Registration (Success):', registration_response_success.json())

    login_response_success = login(username, password)
    # print('Login (Success):', login_response_success.json())

    jwt_token = login_response_success.json().get('access_token')

    
    #Test getting all models

    get_models_response = get_models_by_user(jwt_token)
    print('Get Models by User (Response):', get_models_response.json())
    

    # #Test getting model by tags
    # # Define tag IDs to fetch models
    # tag_ids = [1, 2]  # Example tag IDs

    # # Perform the GET request to fetch models by tags
    # get_models_by_tags_response = get_models_by_tags(jwt_token, tag_ids)
    # print('Get Models by Tags (Response):', get_models_by_tags_response.json())

     
