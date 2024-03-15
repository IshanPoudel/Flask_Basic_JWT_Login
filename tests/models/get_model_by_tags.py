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

def get_models_by_tags(token, tag_ids):
    url = f'{BASE_URL}/model/model_by_tags'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'tags': tag_ids}  # Assuming tag IDs are provided as a list

    # Send the GET request
    response = requests.get(url, headers=headers, json=data)

    # Print the response details for debugging
    print("Get Models by Tags (Status Code):", response.status_code)
    print("Get Models by Tags (Response Content):", response.content)  # or response.text for decoded content
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

    
    
    

    #Test getting model by tags
    # Define tag IDs to fetch models
    tag_ids = [1, 3]  # Example tag IDs

    # Perform the GET request to fetch models by tags
    get_models_by_tags_response = get_models_by_tags(jwt_token, tag_ids)
    print('Get Models by Tags (Response):', get_models_by_tags_response.json())

     
