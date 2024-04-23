from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

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
    

# NASDAQ data Route
    @general_blueprint.route('/nasdaq_data', methods=['GET'])
    def get_nasdaq_data():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT date, open, high, low, close, volume FROM trademinds_nasdaqdata")
            nasdaq_data = cur.fetchall()
            print("i am here")

            print(nasdaq_data)
            

            nasdaq_data_list = []
            for row in nasdaq_data:
                row['date'] = row['date'].strftime('%Y-%m-%d')  # Convert date to string
                nasdaq_data_list.append(row)


            return jsonify({'nasdaq_data': nasdaq_data_list}), 200

        except Exception as e:
            print("Error occurred:", e)

            return jsonify({'error': str(e)}), 500

        finally:
            cur.close()
            

# GET MODEL TAGS BY MODEL ID
    @general_blueprint.route('/modeltags', methods=['GET'])
    @general_blueprint.route('/modeltags/<int:model_id>', methods=['GET'])
    def get_model_tags(model_id=None):
     try:
      cur = mysql.connection.cursor()
      # Check if model_id is provided
      if model_id is not None:
            # Get tags associated with the specific model
            cur.execute("""
                  SELECT 
                    mt.Model_ID,
                      t.TagID,
                    t.Name
                FROM 
                    Tags t
                JOIN 
                    Model_Tags mt ON t.TagID = mt.TagID
                WHERE 
                    mt.Model_ID = %s;
              """, (model_id,))
      else:
            # Get all tags associated with all models
              cur.execute("""
                  SELECT 
                    mt.Model_ID,
                    t.TagID,
                    t.Name
                FROM 
                    Tags t
                JOIN 
                    Model_Tags mt ON t.TagID = mt.TagID;
               """)

      tags = cur.fetchall()

      cur.close()

      return jsonify(tags), 200
     except Exception as e:
          return jsonify({"error": "Failed to fetch model tags", "details": str(e)}), 500


# ALL MODELS ROUTE
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

#Get Reviews of models
    @general_blueprint.route('/models/<int:model_id>/reviews', methods=['GET'])
    def get_reviews_by_model_id(model_id):
        try:
            cur = mysql.connection.cursor()
            # SQL query to fetch reviews and their upvoter IDs for a specific model
            cur.execute("""
                SELECT 
                    r.Review_ID, 
                    r.UserID AS Reviewer_ID, 
                    u.User AS Reviewer_Name,
                    u.Profile_Picture_Path AS Reviewer_Profile_Pic,
                    r.Comment,
                    r.Upvote, 
                    GROUP_CONCAT(ru.User_ID SEPARATOR ', ') AS Upvoter_IDs
                FROM 
                    Reviews r
                JOIN 
                    Users u ON r.UserID = u.User_ID
                LEFT JOIN 
                    Review_Upvotes ru ON r.Review_ID = ru.Review_ID
                WHERE 
                    r.Model_ID = %s
                GROUP BY 
                    r.Review_ID;
            """, (model_id,))
            reviews = cur.fetchall()


            if not reviews:
                return jsonify({"error": "No reviews found for this model"}), 404

            cur.close()
            return jsonify(reviews), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch reviews", "details": str(e)}), 500


#GET USER DETAILS
    @general_blueprint.route('/userdetails', methods=['GET'])
    @jwt_required()  # Requires a valid JWT token to access this route
    def user_details():
        current_user_id = get_jwt_identity()  # Extract user ID from the JWT token
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    User_ID,
                    User AS Name,
                    Email,
                    Profile_Picture_Path
                FROM 
                    Users
                WHERE 
                    User_ID = %s;
            """, (current_user_id,))
            user_info = cur.fetchone()  # Using fetchone() since we expect only one row
            cur.close()
            if not user_info:
                return jsonify({"message": "User not found"}), 404
            return jsonify(user_info), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch user details", "details": str(e)}), 500

# Get User Liked Models
    @general_blueprint.route('/userlikes', methods=['GET'])
    @jwt_required()  # Require the JWT token for this route
    def get_user_model_likes():
        user_id = get_jwt_identity()  # Extracts the user ID from the JWT token
        try:
            cur = mysql.connection.cursor()
            # Updated query to fetch full model details for liked models
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
                JOIN
                    Likes l ON m.Model_ID = l.Model_ID
                WHERE 
                    l.User_ID = %s;
            """, (user_id,))
            models = cur.fetchall()
            cur.close()
            return jsonify(models), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch user liked models", "likes": str(e)}), 500

# Get User Created Models
    @general_blueprint.route('/usermodels', methods=['GET'])
    @jwt_required()  # Require the JWT token for this route
    def get_user_created_models():
        user_id = get_jwt_identity()  # Extracts the user ID from the JWT token
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
                    Users u ON m.UserID = u.User_ID
                WHERE 
                    u.User_ID = %s
                ORDER BY 
                    m.Model_ID;
            """, (user_id,))
            models = cur.fetchall()
            cur.close()
            return jsonify(models), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch user liked models", "likes": str(e)}), 500

# ALL REVIEWS ROUTE 
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


# ALL REVIEW UPVOTE ROUTE
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


# ALL USERS WHO LIKED MODELS
    @general_blueprint.route('/model_likes', methods=['GET'])
    def get_all_models_likes():
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    m.Model_ID, 
                    l.User_ID
                FROM 
                    Models m
                LEFT JOIN 
                    Likes l ON m.Model_ID = l.Model_ID
                ORDER BY 
                    m.Model_ID;
            """)
            results = cur.fetchall()
            cur.close()

            # Format the result into a structured dictionary
            models_likes = {}
            for row in results:
                model_id = row['Model_ID']
                if model_id not in models_likes:
                    models_likes[model_id] = {
                        'Model_ID': model_id,
                        'Liked_By': []
                    }
                if row['User_ID']:  # Only add user ID if not None (i.e., there is a like)
                    models_likes[model_id]['Liked_By'].append(row['User_ID'])

            return jsonify(list(models_likes.values())), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch model likes", "details": str(e)}), 500



# LIKES OF MODEL BY USERS
    @general_blueprint.route('/model_likes/<int:user_id>', methods=['GET'])
    
    def get_models_liked_by_user(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    m.Model_ID,
                    m.Name AS Model_Name
                FROM 
                    Likes l
                JOIN 
                    Models m ON m.Model_ID = l.Model_ID
                WHERE 
                    l.User_ID = %s
                ORDER BY 
                    m.Model_ID;
            """, (user_id,))
            models_liked = cur.fetchall()
            cur.close()

            # Format the result into a structured list
            liked_models = [
                {'Model_ID': model['Model_ID'], 'Model_Name': model['Model_Name']}
                for model in models_liked
            ]

            if liked_models:
                return jsonify(liked_models), 200
            else:
                return jsonify({"message": "No models found or invalid user ID"}), 200

        except Exception as e:
            return jsonify({"error": "Failed to fetch liked models for user", "details": str(e)}), 500

# MODEL BY ID ROUTE
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

    
# MODEL BY USER ROUTE
    @general_blueprint.route('/models/user/<int:user_id>', methods=['GET'])
    def get_models_by_user_id(user_id):
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
                    Users u ON m.UserID = u.User_ID
                WHERE 
                    u.User_ID = %s;
            """, (user_id,))
            models = cur.fetchall()
            cur.close()
            if not models:
                return jsonify({"error": "No models found for the specified user"}), 404
            return jsonify(models), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch models", "details": str(e)}), 500


# SPECIFIC REVIEW ROUTE
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


# MODEL SUBSCRIBERS
    @general_blueprint.route('/models/<int:model_id>/subscribers', methods=['GET'])
    def get_model_subscribers(model_id):
        try:
            cur = mysql.connection.cursor()

            # Get subscriber count for the model
            cur.execute("""
                SELECT 
                    COUNT(User_ID) AS Subscriber_Count
                FROM 
                    User_Model_Subscribe
                WHERE 
                    Model_ID = %s;
            """, (model_id,))
            subscriber_count = cur.fetchone()['Subscriber_Count']

            # Get details of users who subscribed to the model
            cur.execute("""
                SELECT 
                    u.User_ID,
                    u.User AS User_Name,
                    
                    u.Profile_Picture_Path AS User_Profile_Picture
                FROM 
                    Users u
                JOIN 
                    User_Model_Subscribe um ON u.User_ID = um.User_ID
                WHERE 
                    um.Model_ID = %s;
            """, (model_id,))
            subscribers = cur.fetchall()

            cur.close()

            subscriber_info = {
                "subscriber_count": subscriber_count,
                "subscribers": subscribers
            }
            return jsonify(subscriber_info), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch subscribers for the model", "details": str(e)}), 500

    
        # Define a route to get the latest MSE results


# LATEST MSE DATA ROUTE
    @general_blueprint.route('/models/latest_mse_results', methods=['GET'])
    def get_latest_mse_results():
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    r.Result_ID,
                    r.Stock_ID,
                    s.Ticker,
                    r.Model_ID,
                    r.Timeframe_Name,
                    r.MSE_Value,
                    r.Evaluation_Date,
                    r.Raw_Data
                FROM 
                    MSE_Results r
                JOIN 
                    (SELECT 
                        MAX(Evaluation_Date) AS Latest_Evaluation_Date,
                        Stock_ID,
                        Model_ID
                     FROM 
                        MSE_Results
                     GROUP BY 
                        Stock_ID, Model_ID) latest
                ON 
                    r.Evaluation_Date = latest.Latest_Evaluation_Date
                AND 
                    r.Stock_ID = latest.Stock_ID
                AND 
                    r.Model_ID = latest.Model_ID
                JOIN 
                    Stocks s ON r.Stock_ID = s.Stock_ID 
                 WHERE r.Model_ID= 1;
            """)
            latest_mse_results = cur.fetchall()
            cur.close()
            return jsonify(latest_mse_results), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch latest MSE results", "details": str(e)}), 500
    

# MSE FOR SPECIFIC STOCK ROUTE
    #Sorts by timeframe and gives models based on their MSE for a specific stock
    @general_blueprint.route('/stocks/<string:ticker>/mse_rankings', methods=['GET'])
    def get_mse_rankings_by_stock_ticker(ticker):
        try:
            cur = mysql.connection.cursor()

            # Dictionary to store MSE rankings for each time frame
            mse_rankings = {}

            # List of time frames
            time_frames = ['Previous 1 Day', 'Previous Week', 'Previous Month', 'Previous Year']

            for time_frame in time_frames:
                # Query to get MSE results for the specified stock ticker and time frame
                cur.execute("""
                    SELECT 
                        r.Result_ID,
                        r.Model_ID,
                        r.MSE_Value
                    FROM 
                        MSE_Results r
                    JOIN 
                        Stocks s ON r.Stock_ID = s.Stock_ID
                    WHERE 
                        s.Ticker = %s
                    AND 
                        r.Timeframe_Name = %s
                    AND 
                        r.Evaluation_Date = (
                            SELECT MAX(Evaluation_Date)
                            FROM MSE_Results
                            WHERE Stock_ID = r.Stock_ID AND Model_ID = r.Model_ID AND Timeframe_Name = r.Timeframe_Name
                        )
                    ORDER BY 
                        r.MSE_Value ASC; -- or DESC for descending order
                """, (ticker, time_frame))

                mse_results = cur.fetchall()
                mse_rankings[time_frame] = mse_results

            cur.close()

            return jsonify(mse_rankings), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch MSE rankings for the stock ticker", "details": str(e)}), 500
    

# RESULTS BY RESULT ID ROUTE
    @general_blueprint.route('/results/<int:result_id>', methods=['GET'])
    def get_result_by_id(result_id):
        try:
            cur = mysql.connection.cursor()

            # Query to fetch result by Result_ID
            cur.execute("""
                SELECT 
                    r.Result_ID,
                    r.Stock_ID,
                    s.Ticker,
                    r.Model_ID,
                    r.MSE_Value,
                    r.Evaluation_Date,
                    r.Timeframe_Name,
                    r.Raw_Data
                FROM 
                    MSE_Results r
                JOIN 
                    Stocks s ON r.Stock_ID = s.Stock_ID
                WHERE 
                    r.Result_ID = %s;
            """, (result_id,))

            result = cur.fetchone()

            cur.close()

            if result:
                return jsonify(result), 200
            else:
                return jsonify({"error": "Result not found"}), 404
        except Exception as e:
            return jsonify({"error": "Failed to fetch result by Result_ID", "details": str(e)}), 500


# AVERAGE MSE BY MODEL AND TIMEFRAME ROUTE
    @general_blueprint.route('/models/average_mse_by_model_and_timeframe', methods=['GET'])
    def get_average_mse_by_model_and_timeframe():
        try:
            cur = mysql.connection.cursor()

            # Dictionary to store the average MSE for each model and time frame
            average_mse_by_model_and_timeframe = {}

            # List of time frames
            time_frames = ['Previous 1 Day', 'Previous Week', 'Previous Month', 'Previous Year']

            for time_frame in time_frames:
                # Query to get the average MSE for each model and time frame
                cur.execute("""
                    SELECT 
                        r.Model_ID,
                        AVG(r.MSE_Value) AS Average_MSE
                    FROM 
                        MSE_Results r
                    WHERE 
                        r.Timeframe_Name = %s
                    GROUP BY 
                        r.Model_ID;
                """, (time_frame,))

                mse_results = cur.fetchall()

                # Update average_mse_by_model_and_timeframe dictionary with the average MSE for each model and time frame
                for result in mse_results:
                    model_id = result['Model_ID']
                    average_mse = result['Average_MSE']
                    
                    # Check if model_id already exists in the dictionary, if not, initialize it
                    if model_id not in average_mse_by_model_and_timeframe:
                        average_mse_by_model_and_timeframe[model_id] = {}
                    
                    # Add the average MSE for the current time frame to the dictionary
                    average_mse_by_model_and_timeframe[model_id][time_frame] = average_mse

            cur.close()

            return jsonify(average_mse_by_model_and_timeframe), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch average MSE for each model and time frame", "details": str(e)}), 500


        try:
            cur = mysql.connection.cursor()

            # Query to get the review IDs for the specified model ID and stock ticker on the latest evaluation date
            cur.execute("""
                SELECT 
                    r.Review_ID
                FROM 
                    Reviews r
                JOIN 
                    MSE_Results m ON r.Model_ID = m.Model_ID
                JOIN 
                    Stocks s ON m.Stock_ID = s.Stock_ID
                WHERE 
                    r.Model_ID = %s
                AND 
                    s.Ticker = %s
                AND 
                    m.Evaluation_Date = (
                        SELECT MAX(Evaluation_Date)
                        FROM MSE_Results
                        WHERE Model_ID = m.Model_ID AND Stock_ID = m.Stock_ID
                    );
            """, (model_id, ticker))

            review_ids = [review['Review_ID'] for review in cur.fetchall()]

            cur.close()

            return jsonify({"model_id": model_id, "ticker": ticker, "review_ids": review_ids}), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch review IDs for the model and stock ticker", "details": str(e)}), 500
    

# GET MSE RESULTS FOR SPECIFIC STOCK AND MODEL
    #SO for mod1l 1 for apple , gets all four results and mse
    @general_blueprint.route('/models/<int:model_id>/stock/<string:stock_ticker>/result_info', methods=['GET'])
    def get_result_info_for_model_and_ticker(model_id, stock_ticker):
        try:
            cur = mysql.connection.cursor()

            # List of time frames
            time_frames = ['Previous 1 Day', 'Previous Week', 'Previous Month', 'Previous Year']

            result_info_list = []

            for time_frame in time_frames:
                # Query to get the result ID and timeframe for the specified model ID, stock ticker, and time frame
                cur.execute("""
                    SELECT 
                        Result_ID,
                        Timeframe_Name
                    FROM 
                        MSE_Results
                    WHERE 
                        Model_ID = %s
                    AND 
                        Stock_ID = (
                            SELECT Stock_ID
                            FROM Stocks
                            WHERE Ticker = %s
                        )
                    AND 
                        Timeframe_Name = %s
                    AND 
                        Evaluation_Date = (
                            SELECT MAX(Evaluation_Date)
                            FROM MSE_Results
                            WHERE Model_ID = %s AND Stock_ID = (
                                SELECT Stock_ID
                                FROM Stocks
                                WHERE Ticker = %s
                            ) AND Timeframe_Name = %s
                        );
                """, (model_id, stock_ticker, time_frame, model_id, stock_ticker, time_frame))

                result_info = cur.fetchone()

                if result_info:
                    result_info_list.append({"timeframe": result_info['Timeframe_Name'], "result_id": result_info['Result_ID']})
                else:
                    result_info_list.append({"timeframe": time_frame, "result_id": None})

            cur.close()

            return jsonify({"model_id": model_id, "stock_ticker": stock_ticker, "result_info": result_info_list}), 200

        except Exception as e:
            return jsonify({"error": "Failed to fetch result info for the model and stock ticker", "details": str(e)}), 500


# GET MSE RESULTS FOR ALL STOCKS GROUPED BY MODEL
    @general_blueprint.route('/models/latest_mse_results_grouped/<int:model_id>', methods=['GET'])
    def get_latest_mse_results_grouped(model_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT 
                    r.Result_ID,
                    r.Stock_ID,
                    s.Ticker,
                    r.Model_ID,
                    r.Timeframe_Name,
                    r.MSE_Value,
                    r.Evaluation_Date,
                    r.Raw_Data
                FROM 
                    MSE_Results r
                JOIN 
                    (SELECT 
                        MAX(Evaluation_Date) AS Latest_Evaluation_Date,
                        Stock_ID,
                        Model_ID
                    FROM 
                        MSE_Results
                    GROUP BY 
                        Stock_ID, Model_ID) latest
                ON 
                    r.Evaluation_Date = latest.Latest_Evaluation_Date
                AND 
                    r.Stock_ID = latest.Stock_ID
                AND 
                    r.Model_ID = latest.Model_ID
                JOIN               
                    Stocks s ON r.Stock_ID = s.Stock_ID
                WHERE 
                    r.Model_ID = %s;
                """, (model_id,))
            results = cur.fetchall()
            cur.close()

            # Reformatting the results by ticker
            ticker_grouped_results = {}
            for result in results:
                ticker = result['Ticker']
                if ticker not in ticker_grouped_results:
                    ticker_grouped_results[ticker] = []
                ticker_grouped_results[ticker].append({
                    'Result_ID': result['Result_ID'],
                    'Stock_ID': result['Stock_ID'],
                    'Model_ID': result['Model_ID'],
                    'Timeframe_Name': result['Timeframe_Name'],
                    'MSE_Value': result['MSE_Value'],
                    'Evaluation_Date': result['Evaluation_Date'],
                    'Raw_Data': result['Raw_Data']
                })

            return jsonify(ticker_grouped_results), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch latest MSE results", "details": str(e)}), 500
     

    return general_blueprint
