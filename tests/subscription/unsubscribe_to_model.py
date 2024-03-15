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



# Function to unsubscribe from a model
def unsubscribe_model(token, model_id):
    url = f'{BASE_URL}/sub/unsubscribe/{model_id}'
    headers = {'Authorization': f'Bearer {token}'}
    
    # Send the POST request to unsubscribe from the model
    response = requests.post(url, headers=headers)
    
    # Print the response details
    print("Unsubscribe Model (Status Code):", response.status_code)
    print("Unsubscribe Model (Response Content):", response.content)
    return response


if __name__ == '__main__':


    #Now create a second user that likes and subscribes
    email = "cl@gmail.com"
    password="championsleague"
    username="arsenalwin"

    registration_response_success = register(email, password, username)
    # print('Registration (Success):', registration_response_success.json())

    login_response_success = login(username, password)
    # print('Login (Success):', login_response_success.json())

    jwt_token = login_response_success.json().get('access_token')


    # Test subscribing to the model
    #Use a model_id
    model_id=1

   
    # Test unsubscribing from the model
    unsubscribe_model_response = unsubscribe_model(jwt_token, model_id)
    print('Unsubscribe Model (Response):', unsubscribe_model_response.json())

    


    