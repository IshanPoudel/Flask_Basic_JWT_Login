from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mysqldb import MySQL

# Define a blueprint for subscription and liking functionality
def subscription_blueprint(mysql):
    subscription_blueprint = Blueprint('subscription', __name__)
    
    @subscription_blueprint.route('/subscribe/<int:model_id>', methods=['POST'])
    @jwt_required()
    def subscribe_to_model(model_id):
        current_user_id = get_jwt_identity()
        cur = mysql.connection.cursor()
        try:
            # Check if the user is already subscribed to the model
            cur.execute("SELECT * FROM User_Model_Subscribe WHERE Model_ID = %s AND User_ID = %s",
                        (model_id, current_user_id))
            subscription = cur.fetchone()
            if subscription:
                return jsonify({"message": "User is already subscribed to this model"}), 400

            # Subscribe the user to the model
            cur.execute("INSERT INTO User_Model_Subscribe (Model_ID, User_ID) VALUES (%s, %s)",
                        (model_id, current_user_id))
            mysql.connection.commit()

            # Update subscribe count in Models table
            cur.execute("UPDATE Models SET Subscribe_Count = Subscribe_Count + 1 WHERE Model_ID = %s", (model_id,))
            mysql.connection.commit()

            return jsonify({"message": "Subscribed to model successfully"}), 200
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": "Failed to subscribe to model", "details": str(e)}), 500
        finally:
            cur.close()


    # Route for unsubscribing from a model
    # Route for unsubscribing from a model
    @subscription_blueprint.route('/unsubscribe/<int:model_id>', methods=['POST'])
    @jwt_required()
    def unsubscribe_from_model(model_id):
        current_user_id = get_jwt_identity()
        cur = mysql.connection.cursor()
        try:
            # Check if the user is subscribed to the model
            cur.execute("SELECT * FROM User_Model_Subscribe WHERE Model_ID = %s AND User_ID = %s",
                        (model_id, current_user_id))
            subscription = cur.fetchone()
            if not subscription:
                return jsonify({"message": "User is not subscribed to this model"}), 400

            # Unsubscribe the user from the model
            cur.execute("DELETE FROM User_Model_Subscribe WHERE Model_ID = %s AND User_ID = %s",
                        (model_id, current_user_id))
            mysql.connection.commit()

            # Update subscribe count in Models table
            cur.execute("UPDATE Models SET Subscribe_Count = GREATEST(Subscribe_Count - 1, 0) WHERE Model_ID = %s", (model_id,))
            mysql.connection.commit()

            return jsonify({"message": "Unsubscribed from model successfully"}), 200
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": "Failed to unsubscribe from model", "details": str(e)}), 500
        finally:
            cur.close()


    # Route for liking a model
    @subscription_blueprint.route('/like/<int:model_id>', methods=['POST'])
    @jwt_required()
    def like_model(model_id):
        current_user_id = get_jwt_identity()
        cur = mysql.connection.cursor()

        print("I am here inside like model")
        try:
            # Check if the user has already liked the model
            cur.execute("SELECT COUNT(*) FROM Likes WHERE Model_ID = %s AND User_ID = %s",
                        (model_id, current_user_id))

            like_count_row = cur.fetchone()
            print(like_count_row)
            
            # Check if a row was fetched and access its value
            if like_count_row:
                like_count = like_count_row['COUNT(*)']
                like_exists = like_count > 0
            else:
                # Handle the case where no row was fetched
                like_exists = False

            print("Check if like_exists" , like_exists)

            if like_exists:
                # Unlike the model
                cur.execute("DELETE FROM Likes WHERE Model_ID = %s AND User_ID = %s",
                            (model_id, current_user_id))
                mysql.connection.commit()

                # Decrease like count in Models table
                cur.execute("UPDATE Models SET Like_Count = GREATEST(Like_Count - 1, 0) WHERE Model_ID = %s", (model_id,))
                mysql.connection.commit()

                return jsonify({"message": "Unliked model successfully"}), 200
            else:
                # Like the model
                cur.execute("INSERT INTO Likes (Model_ID, User_ID) VALUES (%s, %s)",
                            (model_id, current_user_id))
                mysql.connection.commit()

                # Increase like count in Models table
                cur.execute("UPDATE Models SET Like_Count = Like_Count + 1 WHERE Model_ID = %s", (model_id,))
                mysql.connection.commit()

                return jsonify({"message": "Liked model successfully"}), 200
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": "Failed to like model", "details": str(e)}), 500
        finally:
            cur.close()


    return subscription_blueprint
