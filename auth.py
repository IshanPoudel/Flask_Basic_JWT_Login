from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt


import re
def auth_blueprint(mysql):
    auth_bp = Blueprint('auth', __name__)
    bcrypt = Bcrypt()


    @auth_bp.route('/register', methods=['POST'])
    def register():
        email = request.json.get('email', '')
        password = request.json.get('password', '')
        username = request.json.get('username', '')

        # Basic validation
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({"error": "Invalid email address"}), 400
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters long"}), 400

        cur = mysql.connection.cursor()
        # Check for existing email
        cur.execute("SELECT * FROM Users WHERE Email = %s", [email])
        if cur.fetchone():
            return jsonify({"error": "Email already exists"}), 400
        
        # Check for existing username
        cur.execute("SELECT * FROM Users WHERE User = %s", [username])
        if cur.fetchone():
            return jsonify({"error": "Username already taken"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute("INSERT INTO Users (User, Email, Hashed_Password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "User created successfully"}), 201

    @auth_bp.route('/login', methods=['POST'])
    def login():

        username = request.json.get('username', '')
        password = request.json.get('password', '')

        #Need to hashed user-inputted password
        # user_inputted_password = generate_password_hash(password, method='pbkdf2:sha256')

        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Hashed_Password FROM Users WHERE User = %s", [username])
        user = cur.fetchone()

        if not user:
            return jsonify({"error": "Invalid login credentials"}), 401



        

        if not user or not bcrypt.check_password_hash(user['Hashed_Password'], password):
            print(password)
            print(user['Hashed_Password'])
           
           
            return jsonify({"error": "Invalid login credentials"}), 401

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=user['User_ID'])
        print("Succesfully logged in " , access_token)
        return jsonify(access_token=access_token), 200

    @auth_bp.route('/change_password', methods=['POST'])
    def change_password():
        username = request.json.get('username', '')
        old_password = request.json.get('old_password', '')
        new_password = request.json.get('new_password', '')

        if len(new_password) < 6:
            return jsonify({"error": "New password must be at least 6 characters long"}), 400

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE User = %s", [username])
        user = cur.fetchone()

        if not user or not bcrypt.check_password_hash(user['Hashed_Password'], old_password):
            return jsonify({"error": "Invalid username or old password"}), 401

        hashed_new_password=bcrypt.generate_password_hash(new_password).decode('utf-8')
        cur.execute("UPDATE Users SET Hashed_Password = %s WHERE User = %s", (hashed_new_password, username))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Password changed successfully"}), 200

    return auth_bp
