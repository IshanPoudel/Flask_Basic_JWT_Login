import requests






#import requests

# Add the BASE_URL if not already defined
BASE_URL = 'http://localhost:5000/auth'


# Function to login an existing user
def login(username, password):
    url = f'{BASE_URL}/login'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    return response



if __name__ == '__main__':
    login_response_success = login('testuser', 'newpassword456')
    print('Login (Success):', login_response_success.json())