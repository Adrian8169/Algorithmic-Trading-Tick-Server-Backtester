import time
import zmq
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import json
import math

# Configuration variables
TICKER_SYMBOL = "AAPL"  # The stock ticker symbol for Apple Inc.
START_DATE_INPUT = "08/20/2023"  # The starting date for fetching historical stock data, in MM/DD/YYYY format.
A = 0.025  # Amplitude of sinusoidal modulation, used to add variability to the simulated intraday prices.
FREQUENCY = 0.5  # Frequency of sinusoidal component for Bid and Ask prices.
PHASE = 0  # Phase of sinusoidal component for Bid and Ask prices.
MIN_SPREAD = 0.005  # Minimum Spread between Bid and Ask prices.

# Calculating the end date and start date for fetching historical stock data
end_date = datetime.datetime.strptime(START_DATE_INPUT, "%m/%d/%Y") + datetime.timedelta(days=19)
start_date = end_date - datetime.timedelta(days=19)

# Setting up a ZeroMQ context and a PUB socket to send messages
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5555')

def get_stock_data(ticker_symbol, start_date, end_date):
    """
    Fetch historical stock data for a given ticker symbol within a date range.
    """
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
    return stock_data

def simulate_intraday_prices(stock_data, A):
    """
    Simulate and send intraday stock prices based on historical open and close prices.
    """
    dt = 1 / 390 / 60 / 60  # 1 second in a trading day of 6.5 hours (390 minutes)

    # Loop through each day in the stock data
    for i in range(1, len(stock_data)):
        day = stock_data.index[i]
        S_t = stock_data['Open'].iloc[i]
        mu = np.log(stock_data['Close'].iloc[i] / S_t) / 390
        sigma = stock_data['Close'].pct_change().iloc[i]

        # Simulate prices for each second of the trading day
        for t in range(int(390 * 60 * 60)):
            time.sleep(1)  # Send a tick every second
            time_in_day = t * dt  # Calculate the proportion of the day that has passed
            modulated_sigma = sigma * (1 + A * math.cos(2 * math.pi * (time_in_day - 0.25)))
            W_t = np.random.normal(0, math.sqrt(dt))
            S_t = S_t * np.exp((mu - 0.5 * modulated_sigma ** 2) * dt + modulated_sigma * W_t)

            # Calculate Bid and Ask prices
            bid_ask_amplitude = A * math.sin(2 * math.pi * FREQUENCY * time_in_day + PHASE) + (MIN_SPREAD / 2)
            bid = S_t - bid_ask_amplitude
            ask = S_t + bid_ask_amplitude

            # Construct the timestamp for the current tick
            timestamp = day.replace(hour=9, minute=30) + datetime.timedelta(seconds=t)

            # Creating and sending the message in JSON format
            msg_dict = {
                'timestamp': timestamp.strftime("%Y%m%d %H:%M:%S"),
                'price': f"{S_t:.6f}",
                'bid': f"{bid:.6f}",
                'ask': f"{ask:.6f}"
            }
            msg_json = json.dumps(msg_dict)
            socket.send_string(msg_json)

def main():
    """
    Main function to execute the simulation.
    """
    stock_data = get_stock_data(TICKER_SYMBOL, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    stock_data = stock_data.iloc[1:]  # Dropping the first day as it's incomplete
    simulate_intraday_prices(stock_data, A)

if __name__ == "__main__":
    main()
