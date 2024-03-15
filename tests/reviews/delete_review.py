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


# Function to delete a review
def delete_review(token, review_id):
    url = f'{BASE_URL}/review/delete_review/{review_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(url, headers=headers)
    return response


if __name__ == '__main__':
    # Register and login a user
    email = "cl@gmail.com"
    password = "championsleague"
    username = "arsenalwin"

    registration_response_success = register(email, password, username)
    login_response_success = login(username, password)
    jwt_token = login_response_success.json().get('access_token')

    # Test adding a review to a model
    model_id = 1
    comment = "This is an okay model"

    add_review_response = add_review(jwt_token, model_id, comment)
    print('Add Review (Response):', add_review_response.json())

    review_id = add_review_response.json().get('review_id')
    
    delete_review_response = delete_review(jwt_token, review_id)
    print('Delete Review (Response):', delete_review_response.json())


    #Add a deleting a model


