import requests






#import requests

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


def test_jwt(token):
    url = f'{BASE_URL}/protected'
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url ,headers=headers)
    return response


if __name__ == '__main__':
    login_response_success = login('testuser', 'newpassword456')
    print('Login (Success):', login_response_success.json())

    jwt_token = login_response_success.json().get('access_token')
    protected_resource = test_jwt(jwt_token)
    print(protected_resource.json())





