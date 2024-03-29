import yfinance as yf
from datetime import datetime, timedelta
import mysql.connector

# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'user': 'ishan',
    'password': 'ishan',
    'database': 'trademind_dev'
}

def update_nasdaq_data():
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        nasdaq = yf.Ticker("^IXIC")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=60)
        nasdaq_hist = nasdaq.history(start=start_date, end=end_date)
        
        for date, row in nasdaq_hist.iterrows():
            cursor.execute("""
                INSERT INTO trademinds_nasdaqdata (date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                open = VALUES(open),
                high = VALUES(high),
                low = VALUES(low),
                close = VALUES(close),
                volume = VALUES(volume)
            """, (date.date(), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

        connection.commit()
        print('Successfully updated NASDAQ data.')

    except Exception as e:
        connection.rollback()
        print(f'Error: {e}')

    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    update_nasdaq_data()
