from flask import Blueprint, jsonify, current_app

# Define a blueprint for general requests
def general_blueprint(mysql):
    general_blueprint = Blueprint('general', __name__)

    # Define a route for checking database connection
    @general_blueprint.route('/check_db_connection', methods=['GET'])
    def check_db_connection():
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT 1')  # Executes a simple SELECT query
            cur.close()
            return jsonify({"message": "Successfully connected to the database."}), 200
        except Exception as e:
            return jsonify({"error": "Failed to connect to the database.", "details": str(e)}), 500

    # Define other routes for general requests here...

    return general_blueprint
