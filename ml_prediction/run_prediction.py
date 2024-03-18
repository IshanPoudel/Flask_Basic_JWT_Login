import yfinance as yf
import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from mysql.connector import Error
import json

#Runs prediciton on all models

# Define the Central Time Zone (CDT)
central_timezone = pytz.timezone('America/Chicago')



# Get the current date in CDT
current_cdt_date = datetime.now(central_timezone).strftime('%Y-%m-%d')


#Get global mysql access
# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'user': 'ishan',
    'password': 'ishan',
    'database': 'trademind_dev'
}


def download_data_for_live_test(tickers, start_date='2023-01-01', end_date=current_cdt_date):
    live_data = pd.DataFrame()
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        data['Ticker'] = ticker
        print(data)
        print("Hello world")
        # live_data = live_data.append(data)
        live_data = pd.concat([live_data, data])

    return live_data

def calculate_mse_for_timeframe(model, features, target, data, start_date, end_date):
    subset_data = data[(data.index >= start_date) & (data.index <= end_date)]
    predictions = model.predict(subset_data[features])
    mse = mean_squared_error(subset_data[target], predictions)
    return mse, subset_data.index, subset_data[target], predictions

def visualize_predictions(actual_dates, actual_prices, predicted_prices, model_name, timeframe_name):
    plt.figure(figsize=(12, 6))
    plt.plot(actual_dates, actual_prices, label='Actual Prices', marker='o')
    plt.plot(actual_dates, predicted_prices, label='Predicted Prices', marker='o')
    plt.title(f'{model_name} Predicted vs Actual Prices ({timeframe_name})')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    #plt.savefig(f"{actual_dates}-{actual_prices}-{model_name}-{timeframe_name}{predicted_prices}.png")

def load_and_test_models(tickers_map, models_path='/home/ec2-user/stock_models/'):
    #Convert the incoming map and get the list of tickers
    tickers = list(tickers_map.keys())

    #The reason we are using ticker_map object is to get the stock_id which we need to store in the database in MSE_Results Table
    live_data = download_data_for_live_test(tickers)

    features = ['Open', 'High', 'Low', 'Volume']
    target = 'Close'

    # model_names = [
    #     '1_AdaBoost',
    #     '1_DecisionTree',
    #     '1_GradientBoosting',
    #     '1_KNeighbors',
    #     '1_LGBMRegressor',
    #     '1_LinearRegression',
    #     '1_RandomForest',
    #     '1_SVR'
    # ]    
    # models = {model_name: joblib.load(f'{models_path}{model_name}.joblib') for model_name in model_names}
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor(dictionary=True)

        models= []


        cursor.execute("SELECT Model_ID, Model_File_Path FROM Models")
        for row in cursor.fetchall():
            model_id = row['Model_ID']
            model_file_path = row['Model_File_Path']
            #model = joblib.load(model_file_path)
            #models[model_name] = model
            models.append({"model_id": model_id , "model_file_path": model_file_path})
    except mysql.connector.Error as error:
        print(f"Error while connecting to MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    print(models)



    timeframes = {
        'Previous 1 Day': 1,
        'Previous Week': 7,
        'Previous Month': 30,
        'Previous Year': 365
    }

    for ticker in tickers:
        ticker_data = live_data[live_data['Ticker'] == ticker]
        print(f"\nEvaluating {ticker}:")

        for timeframe_name, num_days in timeframes.items():
            start_date = ticker_data.index[-1] - timedelta(days=num_days)
            end_date = ticker_data.index[-1]

            print(f"\nEvaluating {timeframe_name}:")

            #models = {model_name: joblib.load(f'{models_path}{model_name}.joblib') for model_name in model_names}


            for model_json in models:
                
                model_id = model_json['model_id']
                model_file_path = model_json['model_file_path']
                actual_model = joblib.load(model_file_path)
                mse, actual_dates, actual_prices, predicted_prices = calculate_mse_for_timeframe(actual_model, features, target, ticker_data, start_date, end_date)
                print(f"{model_id}: MSE - {mse:.4f}")


                raw_data = {
                    "actual_dates": [str(date) for date in actual_dates],
                    "actual_prices": actual_prices.tolist(),
                    "predicted_prices": predicted_prices.tolist()
                }

                print(raw_data)
                raw_data_json = json.dumps(raw_data)
                # Insert MSE results and raw data into database
                try:
                    connection = mysql.connector.connect(**mysql_config)
                    cursor = connection.cursor()
                    insert_query = "INSERT INTO MSE_Results (Stock_ID, Timeframe_Name, Model_ID, MSE_Value, Evaluation_Date, Raw_Data) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(insert_query, (tickers_map[ticker], timeframe_name, model_id, mse, current_cdt_date, raw_data_json))
                    connection.commit()
                except mysql.connector.Error as error:
                    print(f"Error while inserting data into MySQL: {error}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()

                #visualize_predictions(actual_dates, actual_prices, predicted_prices, model_id, timeframe_name)

def insert_tickers_into_database(tickers):
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        for ticker in tickers:
            insert_query = "INSERT IGNORE INTO Stocks (Ticker) VALUES (%s)"
            cursor.execute(insert_query, (ticker,))
        connection.commit()
    except mysql.connector.Error as error:
        print(f"Error while inserting tickers into MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_tickers_from_database():
    tickers = {}
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        select_query = "SELECT * FROM Stocks"
        cursor.execute(select_query)
        for row in cursor.fetchall():
            tickers[row[1]]=row[0]
    except mysql.connector.Error as error:
        print(f"Error while retrieving tickers from MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return tickers

#Insert defined tickers here in python file
if __name__ == "__main__":
    tickers_to_store = ['AAPL', 'MSFT', 'AMZN', 'GOOGL']
    insert_tickers_into_database(tickers_to_store)
    tickers_map = get_tickers_from_database()
    print(tickers_map)

    load_and_test_models(tickers_map)
