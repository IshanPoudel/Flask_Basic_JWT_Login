from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mysqldb import MySQL

# Define a blueprint for model reviews functionality
def review_blueprint(mysql):

    review_blueprint = Blueprint('review', __name__)

    @review_blueprint.route('/add_review', methods=['POST'])
    @jwt_required()
    def add_review():
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Check if required data is present in the request
        if 'model_id' not in data or 'comment' not in data:
            return jsonify({"error": "Missing required fields (model_id or comment)"}), 400
        
        model_id = data['model_id']
        comment = data['comment']

        cur = mysql.connection.cursor()
        try:
            # Check if the model exists
            cur.execute("SELECT * FROM Models WHERE Model_ID = %s", (model_id,))
            model = cur.fetchone()

            if not model:
                return jsonify({"error": "Model does not exist"}), 404

            # Add the review to the database
            cur.execute("INSERT INTO Reviews (UserID, Model_ID, Comment) VALUES (%s, %s, %s)",
                        (current_user_id, model_id, comment))
            review_id = cur.lastrowid  # Get the ID of the inserted review

            mysql.connection.commit()

            return jsonify({"message": "Review added successfully" , "review_id":review_id}), 200
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": "Failed to add review", "details": str(e)}), 500
        finally:
            cur.close()

    # Add other routes as needed...

    

    @review_blueprint.route('/delete_review/<int:review_id>', methods=['DELETE'])
    @jwt_required()
    def delete_review(review_id):

        print("i am here")
        current_user_id = get_jwt_identity()
        print(current_user_id)
        cur = mysql.connection.cursor()
        try:
            # Check if the review exists and if the current user is the author
            cur.execute("SELECT UserID FROM Reviews WHERE Review_ID = %s", (review_id,))
            review_author_id = cur.fetchone()['UserID']
            if not review_author_id == current_user_id:
                return jsonify({"error": "You are not authorized to delete this review"}), 403

            # Delete the review
            cur.execute("DELETE FROM Reviews WHERE Review_ID = %s", (review_id,))
            mysql.connection.commit()

            return jsonify({"message": "Review deleted successfully"}), 200
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": "Failed to delete review", "details": str(e)}), 500
        finally:
            cur.close()

    # @review_blueprint.route('/toggle_upvote/<int:review_id>', methods=['POST'])
    # @jwt_required()
    # def toggle_upvote(review_id):
    #     current_user_id = get_jwt_identity()
    #     cur = mysql.connection.cursor()
    #     try:
    #         # Check if the user has already upvoted the review
    #         cur.execute("SELECT COUNT(*) FROM Review_Upvotes WHERE Review_ID = %s AND User_ID = %s",
    #                     (review_id, current_user_id))
    #         upvote_count = cur.fetchone()['COUNT(*)']
    #         print(upvote_count)

            

    #         if upvote_count > 0:
    #             # User has already upvoted, remove the upvote
    #             cur.execute("DELETE FROM Review_Upvotes WHERE Review_ID = %s AND User_ID = %s",
    #                         (review_id, current_user_id))
    #             mysql.connection.commit()
    #             return jsonify({"message": "Upvote removed successfully"}), 200
    #         else:
    #             # User hasn't upvoted yet, add the upvote
    #             cur.execute("INSERT INTO Review_Upvotes (Review_ID, User_ID) VALUES (%s, %s)",
    #                         (review_id, current_user_id))
    #             mysql.connection.commit()
    #             return jsonify({"message": "Upvoted successfully"}), 200
    #     except Exception as e:
    #         mysql.connection.rollback()
    #         return jsonify({"error": "Failed to toggle upvote", "details": str(e)}), 500
    #     finally:
    #         cur.close()

    @review_blueprint.route('/toggle_upvote/<int:review_id>', methods=['POST'])
    @jwt_required()
    def toggle_upvote(review_id):
        current_user_id = get_jwt_identity()
        cur = mysql.connection.cursor()
        try:
            # Check if the user has already upvoted the review
            cur.execute("SELECT COUNT(*) FROM Review_Upvotes WHERE Review_ID = %s AND User_ID = %s",
                        (review_id, current_user_id))
            upvote_count = cur.fetchone()['COUNT(*)']

            print("Checking if user has already upvoted the review" , upvote_count)

            # Get the current upvote count of the review
            cur.execute("SELECT Upvote FROM Reviews WHERE Review_ID = %s", (review_id,))
            current_upvote_count = cur.fetchone()['Upvote']

            print("Checking current upvote count of the reveiw" , current_upvote_count)

            if upvote_count > 0:
                # User has already upvoted, remove the upvote
                cur.execute("DELETE FROM Review_Upvotes WHERE Review_ID = %s AND User_ID = %s",
                            (review_id, current_user_id))
                new_upvote_count = current_upvote_count - 1
                message = "Upvote removed successfully"
            else:
                # User hasn't upvoted yet, add the upvote
                cur.execute("INSERT INTO Review_Upvotes (Review_ID, User_ID) VALUES (%s, %s)",
                            (review_id, current_user_id))
                new_upvote_count = current_upvote_count + 1
                message = "Upvoted successfully"
            
            print("Upvote count of the reveiw" , new_upvote_count)
            # Update the Upvote column of the review with the new upvote count
            cur.execute("UPDATE Reviews SET Upvote = %s WHERE Review_ID = %s", (new_upvote_count, review_id))
            mysql.connection.commit()
            
            return jsonify({"message": message}), 200
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": "Failed to toggle upvote", "details": str(e)}), 500
        finally:
            cur.close()

    
    return review_blueprint
