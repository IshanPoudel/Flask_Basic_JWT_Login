from flask import Flask, jsonify , request
from flask_jwt_extended import JWTManager
from flask_mysqldb import MySQL

#All our route classes
from auth import auth_blueprint
from general_routes import general_blueprint
from model import model_blueprint


from flask_jwt_extended import jwt_required, get_jwt_identity


app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'trademinds'  # Change this!
jwt = JWTManager(app)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ishan'
app.config['MYSQL_PASSWORD'] = 'ishan'
app.config['MYSQL_DB'] = 'trademind_dev'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Register the authentication blueprint and pass the MySQL instance
app.register_blueprint(auth_blueprint(mysql), url_prefix='/auth')

app.register_blueprint(general_blueprint(mysql), url_prefix='/general')

app.register_blueprint(model_blueprint(mysql), url_prefix='/model')





# Define a function to get the user_id from JWT token before each request

@app.before_request
def before_request_callback():
    #These are views we skip because we don't need jwtfor these
    excluded_endpoints = ['auth', 'general']
    if request.endpoint and request.endpoint in app.view_functions:
        view_module = app.view_functions[request.endpoint].__module__
        if view_module not in excluded_endpoints and 'protected' in view_module:
            user_id = get_jwt_identity()
            if user_id:
                setattr(request, 'current_user_id', user_id)



@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(user_id=current_user), 200



if __name__ == '__main__':
    app.run(debug=True)

