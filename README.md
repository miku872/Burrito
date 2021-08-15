# Burrito

This is a technical helper for trading inspired from zerodha streak.
You can update daily data, run different scans on stock prices and volumes, you can write your strategies and backtest them, you can also compare strategies.
I have written some of the technical scans, strategies and backtests. 
They all have been extending to abstract classes so that you can add your own scans, strategies and techicals.
For fetching the data of course you'll need an Api provider, I have abstracted the functionalities of an api provider.
I have also written  2  api providers and their parsers and they are also abstracted out.
you'll need to write custom parser for each of your custom api provider so that data/timeseries structure can be maintained among all the providers.
Lastely you'll need to create Resources/ApiConfig.txt file under ApiProvider/<YourCustomApiProvider> and store all the keys, value in key=value\n format which are required to connect with api
  
You can clone and run Burrito-ui(separate repo) using npm start and then run Api/Server.py to do all these things from ui

Install the libraries given in requirements.txt

