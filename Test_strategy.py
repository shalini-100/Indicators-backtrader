from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')

import datetime  # For datetime objects
import os.path  # To manage paths
import matplotlib.pyplot as plt

# Import the backtrader platform
import backtrader as bt

from RSI import RSI
from Oscillator import Aroon_oscillator
from MACDBoll import MACDboll

# Create a cerebro entity
cerebro = bt.Cerebro()

# Add a strategy
# You may want to change the default cash for different strategy
cerebro.addstrategy(MACDboll)

    # Create a Data Feed
data = bt.feeds.YahooFinanceData(
    dataname='AAPL',
    # Do not pass values before this date
    fromdate=datetime.datetime(2018, 1, 1),
    # Do not pass values before this date
    todate=datetime.datetime(2019, 12, 31),
    # Do not pass values after this date
    reverse=False)

# Add the Data Feed to Cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(10000.0)

# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=100)

# Set the commission
cerebro.broker.setcommission(commission=0.0)

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
cerebro.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Plot the result
cerebro.plot()
