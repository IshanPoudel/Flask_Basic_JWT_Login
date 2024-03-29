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

# Function to add a review to a model
def add_review(token, model_id, comment):
    url = f'{BASE_URL}/review/add_review'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'model_id': model_id,
        'comment': comment
    }
    response = requests.post(url, json=data, headers=headers)
    return response

if __name__ == '__main__':
    # Register and login a user
    email = "joey@gmail.com"
    password = "joey123"
    username = "joeyhussain"

    registration_response_success = register(email, password, username)
    login_response_success = login(username, password)
    jwt_token = login_response_success.json().get('access_token')

    # Test adding a review to a model
    model_id = 10
    comment = "This is a great model to use."

    add_review_response = add_review(jwt_token, model_id, comment)
    print('Add Review (Response):', add_review_response.json())
