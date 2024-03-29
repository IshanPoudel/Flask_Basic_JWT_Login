import requests

# mysql -u ishan -p < /home/ec2-user/trademinds_flask/SQL_start.sql 
# Base URL of your Flask application
BASE_URL = 'http://localhost:5000/auth'


# # Function to login an existing user
# def login(username, password):
#     url = f'{BASE_URL}/login'
#     data = {
#         'username': username,
#         'password': password
#     }
#     response = requests.post(url, json=data)
#     return response

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
   
    #  # Test login - successful
    # login_response_success = login('maulik', 'maulik123')
    # print('Login (Success):', login_response_success.json())

    # Test change password - successful
    change_password_response_success = change_password('maulik', 'maulik123', 'maulik456')
    print('Change Password (Success):', change_password_response_success.json())


