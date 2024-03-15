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

    # Test adding a model
    model_name = "Test Model"
    description = "This is a test model."
    tags = [1, 2]
    model_file_path = "/home/ec2-user/dummy_stock_models_for_upload/abc.joblib"

    # add_model_response = add_model(jwt_token, model_name, description, tags, model_file_path)
    # print('Add Model (Success):', add_model_response.json())
    # add_model_response=add_model(jwt_token , "Test_model_2" , description , [1,3] , "/home/ec2-user/dummy_stock_models_for_upload/cde.joblib" )
    # print('Add Model (Success):', add_model_response.json())


    # #Test deleting a model
    # model_id = add_model_response.json().get('model_id')
    # delete_model_response = delete_model(jwt_token ,model_id)
    # print('Delete Model (Response):', delete_model_response.json())

    #Test getting all models

    get_models_response = get_models_by_user(jwt_token)
    print('Get Models by User (Response):', get_models_response.json())
    

