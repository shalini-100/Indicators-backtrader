from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import matplotlib.pyplot as plt

# Import the backtrader platform
import backtrader as bt

class MACDboll(bt.Strategy):
  params=(('fast_LBP',14),('slow_LBP',26),('BBands_LBP',20))

  def log(self, txt, dt=None):
    dt = dt or self.datas[0].datetime.date(0)
    print('%s, %s' % (dt.isoformat(), txt))

  def __init__(self):
    self.dataclose = self.datas[0].close
    self.fast_EMA =  bt.indicators.ExponentialMovingAverage(self.data, period=self.params.fast_LBP)
    self.slow_EMA = bt.indicators.ExponentialMovingAverage(self.data, period=self.params.slow_LBP)

    self.MACD=self.fast_EMA-self.slow_EMA
    self.bband = bt.indicators.BBands(self.datas[0], period=self.params.BBands_LBP)
    self.order = None
    self.inc_=None
    self.dec_=None

  def notify_order(self, order):
    if order.status in [order.Submitted, order.Accepted]:
      return
    if order.status in [order.Completed]:
      if order.isbuy():
        self.log('BUY EXECUTED, %.2f' % order.executed.price)
      elif order.issell():
        self.log('SELL EXECUTED, %.2f' % order.executed.price)

      self.bar_executed = len(self)
    elif order.status in [order.Canceled, order.Margin, order.Rejected]:
      self.log('Order Canceled/Margin/Rejected')

    self.order = None
  def next(self):
    if not self.order and not self.position:
      if self.MACD > 0:
        self.log('LONG -BUY, %.2f' % self.dataclose[0])
        self.inc_=True
        self.order = self.buy()
      elif self.MACD < 0:
        self.log('SHORT-SELL, %.2f' % self.dataclose[0])
        self.dec_=True
        self.order = self.sell()

    elif not self.order and  self.position :
      if self.MACD > 0 and self.dec_:
        self.log('BUY, %.2f' % self.dataclose[0])
        self.dec_=None
        self.order = self.buy()
      elif self.MACD < 0 and self.inc_:
        self.log('SELL, %.2f' % self.dataclose[0])
        self.inc_=None
        self.order = self.sell()
      if self.dataclose[0] > self.bband.lines.top and self.inc_ :
        self.log('SELL, %.2f' % self.dataclose[0])
        self.inc_=None
        self.order = self.sell()
      elif self.dataclose[0] < self.bband.lines.bot and  self.dec_:
        self.log('BUY, %.2f' % self.dataclose[0])
        self.dec_=None
        self.order = self.buy()