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

    

    login_response_success = login(username, password)
    # print('Login (Success):', login_response_success.json())

    jwt_token = login_response_success.json().get('access_token')

    #jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMzU2MTk0OCwianRpIjoiYWNiN2Y0ODUtZGM5YS00MTQxLWIwZjMtNDBmNTUyOTgwMWI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNzEzNTYxOTQ4LCJjc3JmIjoiNzliNGI0ZmMtYjg3NS00NGFlLTk2OWItOTcxN2U3YzY3ZWI2IiwiZXhwIjoxNzEzNTYyODQ4fQ.mnDmYiw6HcQUDR3SvcHwNGYBs_Ndvih3fqlyvZ_E8OE"

    print(jwt_token)

   

     
