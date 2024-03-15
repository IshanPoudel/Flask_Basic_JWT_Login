import requests

# mysql -u ishan -p < /home/ec2-user/trademinds_flask/SQL_start.sql 
# Base URL of your Flask application
BASE_URL = 'http://localhost:5000/auth'

# Function to register a new user
def register(email, password, username):
    url = f'{BASE_URL}/register'
    data = {
        'email': email,
        'password': password,
        'username': username
    }
    response = requests.post(url, json=data)
    return response

# Function to login an existing user
def login(username, password):
    url = f'{BASE_URL}/login'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    return response

# Function to change password
def change_password(username, old_password, new_password):
    url = f'{BASE_URL}/change_password'
    data = {
        'username': username,
        'old_password': old_password,
        'new_password': new_password
    }
    response = requests.post(url, json=data)
    return response

if __name__ == '__main__':
    # Test registration - successful
    registration_response_success = register('test@example.com', 'password123', 'testuser')
    print('Registration (Success):', registration_response_success.json())

    # Test registration - email already exists
    registration_response_fail_email_exists = register('test@example.com', 'password123', 'testuser')
    print('Registration (Fail - Email Exists):', registration_response_fail_email_exists.json())

    # Test registration - username already taken
    registration_response_fail_username_exists = register('test2@example.com', 'password123', 'testuser')
    print('Registration (Fail - Username Taken):', registration_response_fail_username_exists.json())

    # Test login - successful
    login_response_success = login('testuser', 'password123')
    print('Login (Success):', login_response_success.json())

    # Test login - invalid credentials
    login_response_fail_invalid_credentials = login('testuser', 'wrongpassword')
    print('Login (Fail - Invalid Credentials):', login_response_fail_invalid_credentials.json())

    # Test change password - successful
    change_password_response_success = change_password('testuser', 'password123', 'newpassword456')
    print('Change Password (Success):', change_password_response_success.json())

    # Test change password - wrong old password
    change_password_response_fail_wrong_old_password = change_password('testuser', 'wrongpassword', 'newpassword456')
    print('Change Password (Fail - Wrong Old Password):', change_password_response_fail_wrong_old_password.json())

    # Test change password - new password too short
    change_password_response_fail_new_password_short = change_password('testuser', 'newpassword456', 'short')
    print('Change Password (Fail - New Password Too Short):', change_password_response_fail_new_password_short.json())
