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

    # Define a route to get all model information with user data
    @general_blueprint.route('/models', methods=['GET'])
    def get_all_models():
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    m.Model_ID, 
                    m.Description, 
                    m.Like_Count, 
                    m.Subscribe_Count, 
                    m.Name AS Model_Name, 
                    m.Model_File_Path,
                    u.User_ID AS Creator_ID,
                    u.User AS Creator_Name,
                    u.Email AS Creator_Email,
                    u.Profile_Picture_Path AS Creator_Profile_Picture
                FROM 
                    Models m
                JOIN 
                    Users u ON m.UserID = u.User_ID;
            """)
            models = cur.fetchall()
            cur.close()
            return jsonify(models), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch models", "details": str(e)}), 500

    # Define a route to get all reviews with reviewer information
    @general_blueprint.route('/reviews', methods=['GET'])
    def get_all_reviews():
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    r.Review_ID, 
                    r.Comment, 
                    r.Upvote, 
                    r.Model_ID, 
                    r.UserID AS Reviewer_ID, 
                    u.User AS Reviewer_Name, 
                    u.Profile_Picture_Path AS Reviewer_Profile_Picture 
                FROM 
                    Reviews r 
                JOIN 
                    Users u ON r.UserID = u.User_ID;
            """)
            reviews = cur.fetchall()
            cur.close()
            return jsonify(reviews), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch reviews", "details": str(e)}), 500

    # Define a route to get all review upvotes
    @general_blueprint.route('/review_upvotes', methods=['GET'])
    def get_all_review_upvotes():
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    ru.Review_ID, 
                    ru.User_ID AS Upvoter_ID,
                    u.User AS Upvoter_Name
                FROM 
                    Review_Upvotes ru
                JOIN 
                    Users u ON ru.User_ID = u.User_ID;
            """)
            review_upvotes = cur.fetchall()
            cur.close()
            return jsonify(review_upvotes), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch review upvotes", "details": str(e)}), 500
    
        # Define a route to get model information by ID with user data
   
   
    @general_blueprint.route('/models/<int:model_id>', methods=['GET'])
    def get_model_by_id(model_id):
        try:
            cur = mysql.connection.cursor()
            # Get model information
            cur.execute("""
                SELECT 
                    m.Model_ID, 
                    m.Description, 
                    m.Like_Count, 
                    m.Subscribe_Count, 
                    m.Name AS Model_Name, 
                    m.Model_File_Path,
                    u.User_ID AS Creator_ID,
                    u.User AS Creator_Name,
                    u.Email AS Creator_Email,
                    u.Profile_Picture_Path AS Creator_Profile_Picture
                FROM 
                    Models m
                JOIN 
                    Users u ON m.UserID = u.User_ID
                WHERE 
                    m.Model_ID = %s;
            """, (model_id,))
            model = cur.fetchone()
            if not model:
                return jsonify({"error": "Model not found"}), 404
            
            # Get review IDs for the model
            cur.execute("""
                SELECT 
                    Review_ID
                FROM 
                    Reviews
                WHERE 
                    Model_ID = %s;
            """, (model_id,))
            review_ids = [review['Review_ID'] for review in cur.fetchall()]

            cur.close()

            model['review_ids'] = review_ids  # Add review IDs to the model dictionary
            return jsonify(model), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch model and review IDs", "details": str(e)}), 500

    @general_blueprint.route('/reviews/<int:review_id>', methods=['GET'])
    def get_review_by_id(review_id):
        try:
            cur = mysql.connection.cursor()
            # Get review information
            cur.execute("""
                SELECT 
                    r.Review_ID, 
                    r.Comment, 
                    r.Upvote, 
                    r.Model_ID, 
                    r.UserID AS Reviewer_ID, 
                    u.User AS Reviewer_Name, 
                    u.Profile_Picture_Path AS Reviewer_Profile_Picture 
                FROM 
                    Reviews r 
                JOIN 
                    Users u ON r.UserID = u.User_ID
                WHERE 
                    r.Review_ID = %s;
            """, (review_id,))
            review = cur.fetchone()
            if not review:
                return jsonify({"error": "Review not found"}), 404
            
            # Get upvote information for the review
            cur.execute("""
                SELECT 
                    ru.User_ID AS Upvoter_ID,
                    u.User AS Upvoter_Name
                FROM 
                    Review_Upvotes ru
                JOIN 
                    Users u ON ru.User_ID = u.User_ID
                WHERE 
                    ru.Review_ID = %s;
            """, (review_id,))
            upvotes = cur.fetchall()

            cur.close()

            review['upvotes'] = upvotes  # Add upvote information to the review dictionary
            return jsonify(review), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch review and upvotes", "details": str(e)}), 500

    
    return general_blueprint