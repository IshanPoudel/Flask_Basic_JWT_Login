from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define a blueprint for model requests
def model_blueprint(mysql):
    model_blueprint = Blueprint('model', __name__)

    # Directory to store model files
    model_file_path = '/home/ec2-user/stock_models/'

    # Route for adding a model
    @model_blueprint.route('/add', methods=['POST'])
    @jwt_required()  # Requires authentication
    def add_model():
        print("Adding a model")
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({"error": "User ID not found in token"}), 401
        

        #Extract model details from the JSON data
        name = request.form.get('name')
        description = request.form.get('description')
        tags = request.form.get('tags')  # Assuming tags is a list of tag IDs

        

        #Extract the model file from the files parameter
        model_file = request.files.get('model_file')
        if not model_file :
            return jsonify({"error": "Model name and file are required"}), 400

        
        try:

            #Save the model file to the specified directory
            print("Opened the file")
            model_file_path_to_save = f"{model_file_path}/{name}.joblib"
            model_file.save(model_file_path_to_save)
            print("Saved the model")
            
            cur = mysql.connection.cursor()


            # Insert the model details into the database
            cur.execute("INSERT INTO Models (UserID, Name, Description, Model_File_Path) VALUES (%s, %s, %s, %s)",
                        (current_user_id, name, description, model_file_path))
            model_id = cur.lastrowid

            # Insert tags for the model into the Model_Tags table
            for tag_id in tags:
                cur.execute("INSERT INTO Model_Tags (Model_ID, TagID) VALUES (%s, %s)", (model_id, tag_id))

            mysql.connection.commit()
            return jsonify({"message": "Model added successfully", "model_id": model_id}), 201
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": "Failed to add model", "details": str(e)}), 500
        finally:
            cur.close()

    return model_blueprint
