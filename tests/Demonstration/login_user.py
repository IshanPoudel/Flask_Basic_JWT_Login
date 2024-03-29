import requests

# mysql -u ishan -p < /home/ec2-user/trademinds_flask/SQL_start.sql 
# Base URL of your Flask application
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
    # Test registration - successful
    # registration_response_success = register('maulik@example.com', 'maulik123', 'maulik')
    # print('Registration (Success):', registration_response_success.json())

     # Test login - successful
    login_response_success = login('maulik', 'maulik123')
    print('Login (Success):', login_response_success.json())