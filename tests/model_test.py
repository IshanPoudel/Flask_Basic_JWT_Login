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

# Function to add a model
def add_model(token, model_name, description, tags, model_file_path):
    url = f'{BASE_URL}/model/add'
    headers = {'Authorization': f'Bearer {token}'}

    # JSON payload
    data = {
        'name': model_name,
        'description': description,
        'tags': tags,
    }

    # Prepare files
    files = {'model_file': open(model_file_path, 'rb')}

    print(data)
    print(files)

    # Send the request with JSON payload and files
    response = requests.post(url, data=data ,files=files , headers=headers)
    # Print the response details
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Content:", response.content)  # or response.text for decoded content
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

    # Test adding a model
    model_name = "Test Model"
    description = "This is a test model."
    tags = [1, 2]
    model_file_path = "/home/ec2-user/dummy_stock_models_for_upload/abc.joblib"

    add_model_response = add_model(jwt_token, model_name, description, tags, model_file_path)
    print('Add Model (Success):', add_model_response.json())
