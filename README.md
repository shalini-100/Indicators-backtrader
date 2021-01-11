# Indicators
## MACD +Bollinger Bands-
1.Uses Bollinger band to generate signal using MACD line instead of Simple Moving Average line.\

2.This strategy use MACD line to generate long(>0) or short(<0) position in Market.A need for increase in prices in market for long position is denoted by setting self.inc=True and self.dec=True for short position.\

3.For Exiting the position
###### Exit long - MACD<0 or Value >Upper Bollinger Band \
###### Exit Short- MACD>0 or Value <lower Bollinger Band 


## Oscillator -
Uses Crossover strategy between Aroon Oscillator and EXponential Moving Average of Aroon Oscillator.


## RSI -
Uses RSI for strategy with long and short position 
