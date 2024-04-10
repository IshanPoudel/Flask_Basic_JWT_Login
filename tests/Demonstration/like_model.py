import requests
import json

# Add the BASE_URL if not already defined
BASE_URL = 'http://localhost:5000'



# Function to login an existing user
def login(username, password):
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    return response

# Function to like a model
def like_model(token, model_id):
    url = f'{BASE_URL}/sub/like/{model_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, headers=headers)
    return response

if __name__ == '__main__':
    
    password = "joey123"
    username = "joeyhussain"

    login_response_success = login(username, password)
    jwt_token = login_response_success.json().get('access_token')


    model_id = 10

    # Like the model
    like_model_response = like_model(jwt_token, model_id)
    print('Like Model (Response):', like_model_response.json())
