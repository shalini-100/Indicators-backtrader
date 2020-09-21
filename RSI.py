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

# Create a Stratey
class RSI(bt.Strategy):
    params = (
        ('maperiod', 15),('low_RSI',30),('high_RSI',70)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.RSI = bt.indicators.RSI_SMA(
            self.datas[0], period=self.params.maperiod)
        
        self.inc_=None
        self.dec_=None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.RSI < self.params.low_RSI :

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.inc_=True
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

            if self.RSI > self.params.high_RSI :
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.dec_=True
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

        else:

            if self.RSI > self.params.high_RSI and self.inc_ :
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.inc_=None
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
            if self.RSI < self.params.low_RSI and self.dec_:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self_dec=None
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()