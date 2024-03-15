from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_mysqldb import MySQL
from auth import auth_blueprint
from flask_jwt_extended import jwt_required

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



#Sample to check database connection
@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT 1')  # Executes a simple SELECT query
        cur.close()
        return jsonify({"message": "Successfully connected to the database."}), 200
    except Exception as e:
        return jsonify({"error": "Failed to connect to the database.", "details": str(e)}), 500


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



if __name__ == '__main__':
    app.run(debug=True)

