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





#Function to delete a model
# Function to delete a model
def delete_model(token, model_id):
    url = f'{BASE_URL}/model/delete/{model_id}'
    headers = {'Authorization': f'Bearer {token}'}

    # Send the DELETE request
    response = requests.delete(url, headers=headers)
    
    # Print the response details
    print("Delete Model (Status Code):", response.status_code)
    print("Delete Model (Response Content):", response.content)
    return response






if __name__ == '__main__':
    # Test user registration and login
    email = "arsenal@gmail.com"
    password = "maulik"
    username = "maulik456"

  

    login_response_success = login(username, password)
    # print('Login (Success):', login_response_success.json())

    jwt_token = login_response_success.json().get('access_token')

    

    #Test deleting a model
    # model_id = add_model_response.json().get('model_id')
    #Assuming you have a model with model_id = 1
    delete_model_response = delete_model(jwt_token ,11)
    print('Delete Model (Response):', delete_model_response.json())

    

     
