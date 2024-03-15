Client provides email and password, which is sent to the server
Server then verifies that email and password are correct and responds with an auth token
Client stores the token and sends it along with all subsequent requests to the API
Server decodes the token and validates it

Model_files

    # Route for deleting a model
    @model_blueprint.route('/delete/<int:model_id>', methods=['DELETE'])
    @jwt_required()  # Requires authentication
    def delete_model(model_id):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({"error": "User ID not found in token"}), 401

        cur = mysql.connection.cursor()
        try:
            # Check if the model belongs to the current user
            cur.execute("SELECT UserID, Model_File FROM Models WHERE Model_ID = %s", (model_id,))
            model = cur.fetchone()
            if not model or model['UserID'] != current_user_id:
                return jsonify({"error": "Model not found or user does not have permission to delete"}), 404

            # Delete the model file from the directory
            model_file_path = model['Model_File']
            # Add code to delete the model file from the directory here...

            # Delete the model record from the database
            cur.execute("DELETE FROM Models WHERE Model_ID = %s", (model_id,))
            mysql.connection.commit()
            return jsonify({"message": "Model deleted successfully"}), 200
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": "Failed to delete model", "details": str(e)}), 500
        finally:
            cur.close()

    # Route for fetching models by user ID
    @model_blueprint.route('/models/user', methods=['GET'])
    @jwt_required()  # Requires authentication
    def get_models_by_user_id():
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({"error": "User ID not found in token"}), 401

        cur = mysql.connection.cursor()
        try:
            # Fetch models belonging to the current user
            cur.execute("SELECT * FROM Models WHERE UserID = %s", (current_user_id,))
            models = cur.fetchall()
            return jsonify({"models": models}), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch models by user ID", "details": str(e)}), 500
        finally:
            cur.close()

    # Route for fetching models by tags
    @model_blueprint.route('/models/tags', methods=['GET'])
    def get_models_by_tags():
        tags = request.json.get('tags')  # Assuming tags are provided as JSON
        if not tags:
            return jsonify({"error": "At least one tag must be provided"}), 400

        cur = mysql.connection.cursor()
        try:
            # Fetch models associated with all provided tags
            cur.execute("""
                SELECT m.*
                FROM Models m
                JOIN Model_Tags mt ON m.Model_ID = mt.Model_ID
                WHERE mt.TagID IN %s
                GROUP BY m.Model_ID
                HAVING COUNT(DISTINCT mt.TagID) = %s
            """, (tuple(tags), len(tags)))
            models = cur.fetchall()
            return jsonify({"models": models}), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch models by tags", "details": str(e)}), 500
        finally:
            cur.close()

    # Other routes as needed...