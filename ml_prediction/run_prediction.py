import yfinance as yf
import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
import seaborn as sns

#Runs prediciton on all models

# Define the Central Time Zone (CDT)
central_timezone = pytz.timezone('America/Chicago')

# Get the current date in CDT
current_cdt_date = datetime.now(central_timezone).strftime('%Y-%m-%d')

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

def load_and_test_models(tickers, models_path='/home/ec2-user/stock_models/'):
    live_data = download_data_for_live_test(tickers)

    features = ['Open', 'High', 'Low', 'Volume']
    target = 'Close'

    model_names = [
        '1_AdaBoost',
        '1_DecisionTree',
        '1_GradientBoosting',
        '1_KNeighbors',
        '1_LGBMRegressor',
        '1_LinearRegression',
        '1_RandomForest',
        '1_SVR'
    ]    
    models = {model_name: joblib.load(f'{models_path}{model_name}.joblib') for model_name in model_names}

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

            for model_name, model in models.items():
                mse, actual_dates, actual_prices, predicted_prices = calculate_mse_for_timeframe(model, features, target, ticker_data, start_date, end_date)
                print(f"{model_name}: MSE - {mse:.4f}")

                #visualize_predictions(actual_dates, actual_prices, predicted_prices, model_name, timeframe_name)

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL']
    load_and_test_models(tickers)
