
"""
Algorithmic-Trading-Tick-Server-Backtester
==========================================

AlgoTradeMockServer
-------------------
Overview
~~~~~~~~
AlgoTradeMockServer is a backtesting mock ticker server designed to aid in the development and validation of algorithmic trading strategies.
The tool enables users, especially novices, to simulate real-world trading environments using historical stock data.
It employs ZeroMQ for message broadcasting, allowing algorithmic trading models to subscribe and interact with the server as if it were a live trading environment.

Installation
~~~~~~~~~~~~
Prerequisites
+++++++++++++
- Python 3.6 or later
- pip (Python package installer)

Dependencies
++++++++++++
Install the required packages using pip:
```bash
pip install zmq yfinance pandas numpy
```
To use the AlgoTradeMockServer, follow these steps:

1. Clone the Repository:
```bash
git clone https://github.com/your-username/AlgoTradeMockServer.git
cd AlgoTradeMockServer
```

2. Configuration:
   Open `server.py` and edit the configuration variables at the top of the file as needed. The configurable variables include:
   - TICKER_SYMBOL: The stock symbol for the data to be fetched. Default is "AAPL".
   - START_DATE_INPUT: The starting date for the historical data. The format should be "MM/DD/YYYY".
   - A: Amplitude of sinusoidal modulation for price variation. Default is 0.025.
   - FREQUENCY: Frequency of sinusoidal component for Bid and Ask prices. Default is 0.5.
   - PHASE: Phase of sinusoidal component for Bid and Ask prices. Default is 0.
   - MIN_SPREAD: Minimum spread between Bid and Ask prices. Default is 0.005.

3. Run the Server:
```bash
python server.py
```
   The server will start, fetch the historical data for the configured stock symbol, and then begin broadcasting intraday price ticks using the ZeroMQ PUB-SUB model.

4. Connect Your Trading Algorithm:
   Connect your trading algorithm to the server by subscribing to the tcp://localhost:5555 socket using ZeroMQ. You can then start receiving and processing the tick data as per your algorithm.

Example Subscriber
```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    message = socket.recv_string()
    print("Received tick:", message)
```
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.
"""
```
