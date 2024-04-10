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



# Function to subscribe to a model
def subscribe_model(token, model_id):
    url = f'{BASE_URL}/sub/subscribe/{model_id}'
    headers = {'Authorization': f'Bearer {token}'}
    
    # Send the POST request to subscribe to the model
    response = requests.post(url, headers=headers)
    
    # Print the response details
    print("Subscribe Model (Status Code):", response.status_code)
    print("Subscribe Model (Response Content):", response.content)
    return response


if __name__ == '__main__':


    #Now create a second user that likes and subscribes
    
    password="joey123"
    username="joeyhussain"

    # registration_response_success = register(email, password, username)
    # print('Registration (Success):', registration_response_success.json())

    login_response_success = login(username, password)
    # print('Login (Success):', login_response_success.json())

    jwt_token = login_response_success.json().get('access_token')


    # Test subscribing to the model
    #Use a model_id
    #ASSUMING THERE IS A SUBSCRIBE WITH USER_ID TWO
    model_id=10

    #Subscribes to second model
    subscribe_model_response = subscribe_model(jwt_token, model_id)
    print('Subscribe Model (Response):', subscribe_model_response.json())

    