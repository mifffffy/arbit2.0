import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from indicators import patterns
import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as stats
from scipy.stats import skew, kurtosis, shapiro
import requests
from pip._internal import main as install
install(["install","ta-lib"])
import talib



option = st.sidebar.selectbox('Select Dashboard:', ('Technical', 'Portfolio & Risk Management', 'Social', 'Derivatives'))

st.header(option)

if option == 'Technical':
    st.subheader('Technical Dashboard logic')
    analysis = st.sidebar.selectbox('Select Analysis:', ('Momentum', 'Candlestick Patterns'))
    if analysis == 'Momentum':

        st.subheader('Momentum Dashboard')
        st.write("The Momentum Heatmap shows a variety of momentum indicators, which have then been normalised. This means that they are easier to compare. A score of 1, dark blue, means that indicator is at its maximum value, for the given time frame. Note that some indicators have negative values whilst others don't.")
        st.write("The final column shows the total, which is the sum of all the indicators, again normailised to it's maximum value. This is intended as a very quick summary of momentum broadly.")
        symbol = st.text_input('Enter Symbol:', value='BTC', max_chars=None, key=None, type='default')
        interval = st.selectbox(label='Select Interval:', options=('5m', '15m', '30m', '1h', '1d', '1wk'), args=None, key=None)
        if interval == '5m':
            data = yf.download(symbol + '-USD', period='7d', interval=interval)
        if interval == '15m':
            data = yf.download(symbol + '-USD', period='14d', interval=interval)
        else:
            start = st.date_input('Start Date', value=pd.to_datetime('today') - pd.to_timedelta('7 days'))
            data = yf.download(symbol + '-USD', start=start, end=None, interval=interval)
        

    #add momentum indicators to data 

        data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
        data['ADX'] = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=14)
        data['ADXR'] = talib.ADXR(data['High'], data['Low'], data['Close'], timeperiod=14)
        data['APO'] = talib.APO(data['Close'], fastperiod=12, slowperiod=26, matype=0)
        data['AROONOSC'] = talib.AROONOSC(data['High'], data['Low'], timeperiod=14)
        data['BOP'] = talib.BOP(data['Open'], data['High'], data['Low'], data['Close'])
        data['CCI'] = talib.CCI(data['High'], data['Low'], data['Close'], timeperiod=14)
        data['CMO'] = talib.CMO(data['Close'], timeperiod=14)
        data['DX'] = talib.DX(data['High'], data['Low'], data['Close'], timeperiod=14)
        data['MACD'], data['MACDsignal'], data['MACDhist'] = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        data['MFI'] = talib.MFI(data['High'], data['Low'], data['Close'], data['Volume'], timeperiod=14)
        data['MINUS_DI'] = talib.MINUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)
        data['MINUS_DM'] = talib.MINUS_DM(data['High'], data['Low'], timeperiod=14)
        data['MOM'] = talib.MOM(data['Close'], timeperiod=10)
        data['PLUS_DI'] = talib.PLUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)
        data['PLUS_DM'] = talib.PLUS_DM(data['High'], data['Low'], timeperiod=14)
        data['PPO'] = talib.PPO(data['Close'], fastperiod=12, slowperiod=26, matype=0)
        data['ROC'] = talib.ROC(data['Close'], timeperiod=10)
        data['ROCP'] = talib.ROCP(data['Close'], timeperiod=10)
        data['TRIX'] = talib.TRIX(data['Close'], timeperiod=30)
        data['ULTOSC'] = talib.ULTOSC(data['High'], data['Low'], data['Close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
        data['WILLR'] = talib.WILLR(data['High'], data['Low'], data['Close'], timeperiod=14)
        
    #convert to dataframe
        if interval == '5m':
            merge = 'Datetime'
        if interval == '15m':
            merge = 'Datetime'
        if interval == '30m':
            merge = 'Datetime'
        if interval == '1h':
            merge = 'Datetime'
        if interval == '1d':
            merge = 'Date'
        if interval == '3d':
            merge = 'Date'
        if interval == '1wk':
            merge = 'Date'
        data_df = pd.DataFrame(data)
        btc_mom_df = []
        btc_mom_df = data_df['RSI']
        btc_mom_df = pd.merge(btc_mom_df, data_df['ADX'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['ADXR'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['APO'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['AROONOSC'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['BOP'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['CCI'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['CMO'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['DX'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['MACD'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['MACDsignal'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['MACDhist'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['MFI'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['MINUS_DI'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['MINUS_DM'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['MOM'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['PLUS_DI'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['PLUS_DM'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['PPO'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['ROC'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['ROCP'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['TRIX'], on=merge)
        btc_mom_df = pd.merge(btc_mom_df, data_df['ULTOSC'], on=merge)
        
        #clear blank rows
        btc_mom_df = btc_mom_df.dropna()

        #normalize to 1
        btc_mom_df['RSI'] = btc_mom_df['RSI']/btc_mom_df['RSI'].max()
        btc_mom_df['ADX'] = btc_mom_df['ADX']/btc_mom_df['ADX'].max()
        btc_mom_df['ADXR'] = btc_mom_df['ADXR']/btc_mom_df['ADXR'].max()
        btc_mom_df['APO'] = btc_mom_df['APO']/btc_mom_df['APO'].max()
        btc_mom_df['AROONOSC'] = btc_mom_df['AROONOSC']/btc_mom_df['AROONOSC'].max()
        btc_mom_df['BOP'] = btc_mom_df['BOP']/btc_mom_df['BOP'].max()
        btc_mom_df['CCI'] = btc_mom_df['CCI']/btc_mom_df['CCI'].max()
        btc_mom_df['CMO'] = btc_mom_df['CMO']/btc_mom_df['CMO'].max()
        btc_mom_df['DX'] = btc_mom_df['DX']/btc_mom_df['DX'].max()
        btc_mom_df['MACD'] = btc_mom_df['MACD']/btc_mom_df['MACD'].max()
        btc_mom_df['MACDsignal'] = btc_mom_df['MACDsignal']/btc_mom_df['MACDsignal'].max()
        btc_mom_df['MACDhist'] = btc_mom_df['MACDhist']/btc_mom_df['MACDhist'].max()
        btc_mom_df['MFI'] = btc_mom_df['MFI']/btc_mom_df['MFI'].max()
        btc_mom_df['MINUS_DI'] = btc_mom_df['MINUS_DI']/btc_mom_df['MINUS_DI'].max()
        btc_mom_df['MINUS_DM'] = btc_mom_df['MINUS_DM']/btc_mom_df['MINUS_DM'].max()
        btc_mom_df['MOM'] = btc_mom_df['MOM']/btc_mom_df['MOM'].max()
        btc_mom_df['PLUS_DI'] = btc_mom_df['PLUS_DI']/btc_mom_df['PLUS_DI'].max()
        btc_mom_df['PLUS_DM'] = btc_mom_df['PLUS_DM']/btc_mom_df['PLUS_DM'].max()
        btc_mom_df['PPO'] = btc_mom_df['PPO']/btc_mom_df['PPO'].max()
        btc_mom_df['ROC'] = btc_mom_df['ROC']/btc_mom_df['ROC'].max()
        btc_mom_df['ROCP'] = btc_mom_df['ROCP']/btc_mom_df['ROCP'].max()
        btc_mom_df['TRIX'] = btc_mom_df['TRIX']/btc_mom_df['TRIX'].max()
        btc_mom_df['ULTOSC'] = btc_mom_df['ULTOSC']/btc_mom_df['ULTOSC'].max()
        
        #clear blank rows
        btc_mom_df = btc_mom_df.dropna()

        #create total column
        btc_mom_df['Total'] = btc_mom_df.sum(axis=1)
        btc_mom_df['Total'] = btc_mom_df['Total']/btc_mom_df['Total'].max()
        
        #create heatmap
        fig = px.imshow(btc_mom_df, color_continuous_scale='RdBu')
        st.plotly_chart(fig, theme='streamlit', use_container_width=True, size=2500)

        #show dataframe
        st.write(btc_mom_df)

    if analysis == 'Candlestick Patterns':
        symbol = st.sidebar.text_input('Enter Symbol:', value='BTC', max_chars=None, key=None, type='default')
        interval = st.selectbox(label='Select Interval:', options=('5m', '15m', '30m', '1h', '1d', '1wk'), args=None, key=None)
        if interval == '5m':
            data = yf.download(symbol + '-USD', period='7d', interval=interval)
        if interval == '15m':
            data = yf.download(symbol + '-USD', period='14d', interval=interval)
        else:
            start = st.date_input('Start Date', value=pd.to_datetime('today') - pd.to_timedelta('7 days'))
            data = yf.download(symbol + '-USD', start=start, end=None, interval=interval)
    
    #add patterns to data

        data['Two Crows'] = talib.CDL2CROWS(data['Open'], data['High'], data['Low'], data['Close'])
        data['Three Black Crows'] = talib.CDL3BLACKCROWS(data['Open'], data['High'], data['Low'], data['Close'])
        data['Three Inside Up/Down'] = talib.CDL3INSIDE(data['Open'], data['High'], data['Low'], data['Close'])
        data['Three-Line Strike'] = talib.CDL3LINESTRIKE(data['Open'], data['High'], data['Low'], data['Close'])
        data['Three Outside Up/Down'] = talib.CDL3OUTSIDE(data['Open'], data['High'], data['Low'], data['Close'])
        data['Three Stars In The South'] = talib.CDL3STARSINSOUTH(data['Open'], data['High'], data['Low'], data['Close'])
        data['Three Advancing White Soldiers'] = talib.CDL3WHITESOLDIERS(data['Open'], data['High'], data['Low'], data['Close'])
        data['Abandoned Baby'] = talib.CDLABANDONEDBABY(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
        data['Advance Block'] = talib.CDLADVANCEBLOCK(data['Open'], data['High'], data['Low'], data['Close'])
        data['Belt-hold'] = talib.CDLBELTHOLD(data['Open'], data['High'], data['Low'], data['Close'])
        data['Breakaway'] = talib.CDLBREAKAWAY(data['Open'], data['High'], data['Low'], data['Close'])
        data['Closing Marubozu'] = talib.CDLCLOSINGMARUBOZU(data['Open'], data['High'], data['Low'], data['Close'])
        data['Concealing Baby Swallow'] = talib.CDLCONCEALBABYSWALL(data['Open'], data['High'], data['Low'], data['Close'])
        data['Counterattack'] = talib.CDLCOUNTERATTACK(data['Open'], data['High'], data['Low'], data['Close'])
        data['Dark Cloud Cover'] = talib.CDLDARKCLOUDCOVER(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
        data['Doji'] = talib.CDLDOJI(data['Open'], data['High'], data['Low'], data['Close'])
        data['Doji Star'] = talib.CDLDOJISTAR(data['Open'], data['High'], data['Low'], data['Close'])
        data['Engulfing Pattern'] = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
        data['Evening Doji Star'] = talib.CDLEVENINGDOJISTAR(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
        data['Evening Star'] = talib.CDLEVENINGSTAR(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
        data['Gap Side-by-Side White Lines'] = talib.CDLGAPSIDESIDEWHITE(data['Open'], data['High'], data['Low'], data['Close'])
        data['Gravestone Doji'] = talib.CDLGRAVESTONEDOJI(data['Open'], data['High'], data['Low'], data['Close'])
        data['Hammer'] = talib.CDLHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
        data['Hanging Man'] = talib.CDLHANGINGMAN(data['Open'], data['High'], data['Low'], data['Close'])
        data['Harami Pattern'] = talib.CDLHARAMI(data['Open'], data['High'], data['Low'], data['Close'])
        data['Harami Cross Pattern'] = talib.CDLHARAMICROSS(data['Open'], data['High'], data['Low'], data['Close'])
        data['High-Wave Candle'] = talib.CDLHIGHWAVE(data['Open'], data['High'], data['Low'], data['Close'])
        data['Hikkake Pattern'] = talib.CDLHIKKAKE(data['Open'], data['High'], data['Low'], data['Close'])
        data['Modified Hikkake Pattern'] = talib.CDLHIKKAKEMOD(data['Open'], data['High'], data['Low'], data['Close'])
        data['Homing Pigeon'] = talib.CDLHOMINGPIGEON(data['Open'], data['High'], data['Low'], data['Close'])
        data['Identical Three Crows'] = talib.CDLIDENTICAL3CROWS(data['Open'], data['High'], data['Low'], data['Close'])
        data['In-Neck Pattern'] = talib.CDLINNECK(data['Open'], data['High'], data['Low'], data['Close'])
        data['Inverted Hammer'] = talib.CDLINVERTEDHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
        data['Kicking'] = talib.CDLKICKING(data['Open'], data['High'], data['Low'], data['Close'])
        data['Kicking - Bull/Bear'] = talib.CDLKICKINGBYLENGTH(data['Open'], data['High'], data['Low'], data['Close'])
        data['Ladder Bottom'] = talib.CDLLADDERBOTTOM(data['Open'], data['High'], data['Low'], data['Close'])
        data['Long Legged Doji'] = talib.CDLLONGLEGGEDDOJI(data['Open'], data['High'], data['Low'], data['Close'])
        data['Long Line Candle'] = talib.CDLLONGLINE(data['Open'], data['High'], data['Low'], data['Close'])
        data['Marubozu'] = talib.CDLMARUBOZU(data['Open'], data['High'], data['Low'], data['Close'])
        data['Matching Low'] = talib.CDLMATCHINGLOW(data['Open'], data['High'], data['Low'], data['Close'])
        data['Mat Hold'] = talib.CDLMATHOLD(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
        data['Morning Doji Star'] = talib.CDLMORNINGDOJISTAR(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
        data['Morning Star'] = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
        data['On-Neck Pattern'] = talib.CDLONNECK(data['Open'], data['High'], data['Low'], data['Close'])
        data['Piercing Pattern'] = talib.CDLPIERCING(data['Open'], data['High'], data['Low'], data['Close'])
        data['Rickshaw Man'] = talib.CDLRICKSHAWMAN(data['Open'], data['High'], data['Low'], data['Close'])
        data['Rising/Falling Three Methods'] = talib.CDLRISEFALL3METHODS(data['Open'], data['High'], data['Low'], data['Close'])
        data['Separating Lines'] = talib.CDLSEPARATINGLINES(data['Open'], data['High'], data['Low'], data['Close'])
        data['Shooting Star'] = talib.CDLSHOOTINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
        data['Short Line Candle'] = talib.CDLSHORTLINE(data['Open'], data['High'], data['Low'], data['Close'])
        data['Spinning Top'] = talib.CDLSPINNINGTOP(data['Open'], data['High'], data['Low'], data['Close'])
        data['Stalled Pattern'] = talib.CDLSTALLEDPATTERN(data['Open'], data['High'], data['Low'], data['Close'])
        data['Stick Sandwich'] = talib.CDLSTICKSANDWICH(data['Open'], data['High'], data['Low'], data['Close'])
        data['Takuri'] = talib.CDLTAKURI(data['Open'], data['High'], data['Low'], data['Close'])
        data['Tasuki Gap'] = talib.CDLTASUKIGAP(data['Open'], data['High'], data['Low'], data['Close'])
        data['Thrusting Pattern'] = talib.CDLTHRUSTING(data['Open'], data['High'], data['Low'], data['Close'])
        data['Tristar Pattern'] = talib.CDLTRISTAR(data['Open'], data['High'], data['Low'], data['Close'])
        data['Unique 3 River'] = talib.CDLUNIQUE3RIVER(data['Open'], data['High'], data['Low'], data['Close'])
        data['Upside Gap Two Crows'] = talib.CDLXSIDEGAP3METHODS(data['Open'], data['High'], data['Low'], data['Close'])
        data['Upside/Downside Gap Three Methods'] = talib.CDLXSIDEGAP3METHODS(data['Open'], data['High'], data['Low'], data['Close'])

        # pattern dataframe
        data_df = pd.DataFrame(data)
        pattern_df = []
        pattern_df = data_df['Two Crows']
        if interval == '5m':
            merge = 'Datetime'
        if interval == '15m':
            merge = 'Datetime'
        if interval == '30m':
            merge = 'Datetime'
        if interval == '1h':
            merge = 'Datetime'
        if interval == '1d':
            merge = 'Date'
        if interval == '3d':
            merge = 'Date'
        if interval == '1wk':
            merge = 'Date'
        pattern_df = pd.merge(pattern_df, data_df['Three Black Crows'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Three Inside Up/Down'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Three-Line Strike'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Three Outside Up/Down'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Three Stars In The South'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Three Advancing White Soldiers'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Abandoned Baby'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Advance Block'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Belt-hold'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Breakaway'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Closing Marubozu'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Concealing Baby Swallow'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Counterattack'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Dark Cloud Cover'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Doji'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Doji Star'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Engulfing Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Evening Doji Star'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Evening Star'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Gap Side-by-Side White Lines'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Gravestone Doji'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Hammer'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Hanging Man'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Harami Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Harami Cross Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['High-Wave Candle'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Hikkake Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Modified Hikkake Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Homing Pigeon'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Identical Three Crows'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['In-Neck Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Inverted Hammer'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Kicking'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Kicking - Bull/Bear'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Ladder Bottom'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Long Legged Doji'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Long Line Candle'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Marubozu'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Matching Low'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Mat Hold'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Morning Doji Star'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Morning Star'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['On-Neck Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Piercing Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Rickshaw Man'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Rising/Falling Three Methods'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Separating Lines'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Shooting Star'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Short Line Candle'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Spinning Top'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Stalled Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Stick Sandwich'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Takuri'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Tasuki Gap'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Thrusting Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Tristar Pattern'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Unique 3 River'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Upside Gap Two Crows'], on=merge)
        pattern_df = pd.merge(pattern_df, data_df['Upside/Downside Gap Three Methods'], on=merge)
        
        #days since pattern
        #show when pattern triggered
        st.write("Most recent patterns (last 7 days)")
        last = pattern_df[-1:]
        triggered_bullish = last.columns[(last.eq(100)).any()]
        triggered_bearish = last.columns[(last.eq(-100)).any()]
        bullish, bearish = st.columns(2)
        with bullish:
            st.header('Bullish Patterns')
            st.dataframe(triggered_bullish, use_container_width=True, hide_index=True)
        
        with bearish:
            st.header('Bearish Patterns')
            st.dataframe(triggered_bearish, use_container_width=True, hide_index=True)

        #candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                            open=data['Open'],
                                            high=data['High'],
                                            low=data['Low'],
                                            close=data['Close'],
                                            name=symbol)])
        fig.update_xaxes(type='category')
        fig.update_layout(height=1000)
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)
        
        last = pattern_df[-2:-1]
        triggered_bullish = last.columns[(last.eq(100)).any()]
        triggered_bearish = last.columns[(last.eq(-100)).any()]
        bullish, bearish = st.columns(2)
        with bullish:
            st.header('Bullish Patterns')
            st.write("Previous Candle (T-1)")
            st.dataframe(triggered_bullish, use_container_width=True, hide_index=True)
        
        with bearish:
            st.header('Bearish Patterns')
            st.write("T is the current candle, T-1 is the previous candle")
            st.dataframe(triggered_bearish, use_container_width=True, hide_index=True)
    
        st.write("(T-2)")
        last = pattern_df[-3:-2]
        triggered_bullish = last.columns[(last.eq(100)).any()]
        triggered_bearish = last.columns[(last.eq(-100)).any()]
        bullish, bearish = st.columns(2)
        with bullish:
            st.dataframe(triggered_bullish, use_container_width=True, hide_index=True)
        
        with bearish:
            st.dataframe(triggered_bearish, use_container_width=True, hide_index=True)

        st.write("(T-3)")
        last = pattern_df[-4:-3]
        triggered_bullish = last.columns[(last.eq(100)).any()]
        triggered_bearish = last.columns[(last.eq(-100)).any()]
        bullish, bearish = st.columns(2)
        with bullish:
            st.dataframe(triggered_bullish, use_container_width=True, hide_index=True)
        
        with bearish:
            st.dataframe(triggered_bearish, use_container_width=True, hide_index=True)

        st.write("(T-4)")
        last = pattern_df[-5:-4]
        triggered_bullish = last.columns[(last.eq(100)).any()]
        triggered_bearish = last.columns[(last.eq(-100)).any()]
        bullish, bearish = st.columns(2)
        with bullish:
            st.dataframe(triggered_bullish, use_container_width=True, hide_index=True)
        
        with bearish:
            st.dataframe(triggered_bearish, use_container_width=True, hide_index=True)

        st.write("(T-5)")
        last = pattern_df[-6:-5]
        triggered_bullish = last.columns[(last.eq(100)).any()]
        triggered_bearish = last.columns[(last.eq(-100)).any()]
        bullish, bearish = st.columns(2)
        with bullish:
            st.dataframe(triggered_bullish, use_container_width=True, hide_index=True)
        
        with bearish:
            st.dataframe(triggered_bearish, use_container_width=True, hide_index=True)

        st.write("(T-6)")
        last = pattern_df[-7:-6]
        triggered_bullish = last.columns[(last.eq(100)).any()]
        triggered_bearish = last.columns[(last.eq(-100)).any()]
        bullish, bearish = st.columns(2)
        with bullish:
            st.dataframe(triggered_bullish, use_container_width=True, hide_index=True)
        
        with bearish:
            st.dataframe(triggered_bearish, use_container_width=True, hide_index=True)

        st.dataframe(pattern_df, width = 2000)


if option == 'Portfolio & Risk Management':
    #get crypto data
    risk = st.sidebar.selectbox('Select Analysis:', ('Correlation', 'Performance'))
    if risk == 'Correlation':
        st.subheader('Top 10 Cryptoasset Correlation')
        start = st.date_input('Start Date', value=pd.to_datetime('2023-01-01'))
        end = st.date_input('End Date', value=pd.to_datetime('today'))
        top_10_options = st.multiselect('Select Cryptoassets to Compare:', ('BTC-USD','ETH-USD', 'BNB-USD', 'XRP-USD', 'SOL-USD', 'ADA-USD', 'DOT-USD', 'AVAX-USD', 'DOGE-USD', 'TRX-USD', 'MATIC-USD'), default=['BTC-USD', 'ETH-USD', 'BNB-USD'])
        top_10_data = yf.download(tickers= top_10_options, start=start, end=end)['Adj Close']
        top_10_data['Date'] = top_10_data.index
        top_10_data = top_10_data.set_index('Date')
        top_10_data_matrix = top_10_data.corr()
        fig = px.imshow(top_10_data_matrix,
                        x=top_10_data_matrix.columns,
                        y=top_10_data_matrix.columns,
                        color_continuous_scale='RdBu',
                        color_continuous_midpoint=1, range_color=(-1, 1),
                        title='Correlation Heatmap between Crypto Prices')

        size= st.slider('Select Size:', min_value=700, max_value=2000, value=1000, step=50)
        fig_corr = px.imshow(top_10_data_matrix, color_continuous_scale='RdBu', height = size, width=size,
                        color_continuous_midpoint=1, range_color=(-1, 1), text_auto=True)

        st.plotly_chart(fig_corr, theme='streamlit', use_container_width=True, size=10000)
        st.dataframe(top_10_data_matrix, width=2000)

    if risk == 'Performance':
        st.subheader('Compare Asset Performance')
        symbol1, symbol2 = st.columns(2)
        with symbol1:
            symbol_1 = st.text_input('Enter Symbol: (Include -USD for Crypto)', value='BTC-USD', max_chars=None, key=None, type='default')
            start = st.date_input('Start Date', value=pd.to_datetime('2023-01-01'))
            end = st.date_input('End Date', value=pd.to_datetime('today'))
        with symbol2:
            symbol_2 = st.text_input('Enter Symbol: (Include -USD for Crypto)', value='ETH-USD', max_chars=None, key=None, type='default', label_visibility='hidden')
            
        data = yf.download(tickers=(symbol_1, symbol_2), start=start, end=end)['Adj Close']
        
        relative = data.pct_change()
        cum_ret = (1 + relative).cumprod() -1
        cum_ret = cum_ret.fillna(0)
        st.subheader('Returns of {} vs {}'.format(symbol_1, symbol_2))
        st.line_chart(cum_ret)
        st.dataframe(relative, width=1000)

#returns histogram
        data_2 = yf.download(tickers=symbol_1, start=start, end=end)['Adj Close']
        df_2 = pd.Series.to_frame(data_2)
        returns = df_2.pct_change()
        pct_return = returns['Adj Close'] * 100
        returns_plot = pct_return.dropna()

        st.dataframe(returns_plot.head(), width=1000)
        fig = px.histogram(returns_plot, x="Adj Close", nbins=150)
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

        #mean returns
        mean_returns = returns['Adj Close'].mean()
        df_returns = pd.DataFrame(returns['Adj Close'])
        pct_mean_ret = mean_returns * 100
        st.write('Mean Returns: {}%'.format(pct_mean_ret))
        mean_annual_ret_cry = (((1+ mean_returns) ** 365) -1)
        mean_annual_ret_stock = (((1+ mean_returns) ** 252) -1)
        st.write('Mean Annual Return (Crypto): {}%'.format(mean_annual_ret_cry * 100))
        st.write('Mean Annual Return (Stocks): {}%'.format(mean_annual_ret_stock * 100))
        st.write('The mean return is different for Stocks and Crypto because the markets are open different days of the year. Crypto is open 365 days a year, while stocks are open 252 days a year.')
        #standard deviation and variance
        daily_sigma = np.std(returns['Adj Close'])
        st.write('Daily Standard Deviation: {}'.format(daily_sigma))
        daily_variance = daily_sigma ** 2
        st.write('Daily Variance: {}'.format(daily_variance))
        annual_sigma_cry = daily_sigma * np.sqrt(365)
        annual_sigma_stock = daily_sigma * np.sqrt(252)
        annual_variance_cry = annual_sigma_cry ** 2
        annual_variance_stock = annual_sigma_stock ** 2
        st.write('Annual Standard Deviation (Crypto): {}'.format(annual_sigma_cry))
        st.write('Annual Variance (Crypto): {}'.format(annual_variance_cry))
        st.write('The annual standard deviation and variance are different for Stocks and Crypto because the markets are open different days of the year. Crypto is open 365 days a year, while stocks are open 252 days a year.') 
        st.write('Annual Standard Deviation (Stocks): {}'.format(annual_sigma_stock))
        st.write('Annual Variance (Stocks): {}'.format(annual_variance_stock))

        #skew
        clean_returns = returns['Adj Close'].dropna()
        return_skew = skew(clean_returns)
        st.write('Skew')
        st.write(return_skew)
        excess_kurtosis = kurtosis(clean_returns.dropna())
        st.write('Excess Kurtosis')
        st.write(excess_kurtosis)
        fourth_moment = excess_kurtosis + 3
        st.write('Fourth Moment')
        st.write(fourth_moment)

        #shapiro-wilk test
        shapiro_results = shapiro(clean_returns)
        st.write('Shapiro-Wilk Test:', shapiro_results)
        p_value = shapiro_results[1]
        st.write('P-Value:', p_value)

    #top 10 line chart
        top_10_options = st.multiselect('Select Cryptoassets to Compare:', ('BTC-USD','ETH-USD', 'BNB-USD', 'XRP-USD', 'SOL-USD', 'ADA-USD', 'DOT-USD', 'AVAX-USD', 'DOGE-USD', 'TRX-USD', 'MATIC-USD'), default=['BTC-USD', 'ETH-USD', 'BNB-USD'])
        top_10_data = yf.download(tickers= top_10_options, start=start, end=end)['Adj Close']
        top_10_df = pd.DataFrame(top_10_data)
        top_10_relative = top_10_df.pct_change()
        top_10_cum_ret = (1 + top_10_relative).cumprod() -1
        top_10_cum_ret = top_10_cum_ret.fillna(0)
        st.subheader('Cumulative Percentage Returns')
        st.line_chart(top_10_cum_ret)
        

    #top 10 hist
        top_10_pct_return = top_10_relative[top_10_options] * 100
        top_10_returns_plot = top_10_pct_return.dropna()
        st.subheader('Recent Percentage Returns')
        day_select = st.slider('Select Number of Days:', min_value=1, max_value=365, value=10, step=1)
        st.dataframe(top_10_returns_plot.tail(day_select), width=2000)
        bins= st.slider('Resolution:', min_value=50, max_value=500, value=100, step=10)
        top_10_fig = px.histogram(top_10_returns_plot, x=top_10_options, nbins=bins, opacity=0.9, barmode='overlay')
        st.plotly_chart(top_10_fig, use_container_width=True, theme='streamlit')
        
        #top 10 mean returns
        top_10_mean_returns = top_10_relative[top_10_options].mean() * 100
        top_10_description_df = pd.DataFrame(top_10_mean_returns)
        top_10_description_df.rename(columns={0: 'Mean Daily Returns (%)'}, inplace=True)
        top_10_description_df['Daily Sigma'] = top_10_relative[top_10_options].std()
        top_10_description_df['Annual Sigma (Crypto)'] = top_10_description_df['Daily Sigma'] * np.sqrt(365)
        top_10_description_df['Daily Variance'] = top_10_description_df['Daily Sigma'] ** 2
        top_10_description_df['Annual Variance (Crypto)'] = top_10_description_df['Annual Sigma (Crypto)'] ** 2
        top_10_clean = top_10_relative[top_10_options].dropna()
        top_10_description_df['Skew'] = skew(top_10_clean)
        top_10_description_df['Excess Kurtosis'] = kurtosis(top_10_clean.dropna())
        top_10_description_df['Fourth Moment'] = top_10_description_df['Excess Kurtosis'] + 3
        numpy_arrays = [top_10_clean[column_name].to_numpy() for column_name in top_10_options]
        for column_name, numpy_array in zip(top_10_options, numpy_arrays):
            statistic, p_value = shapiro(numpy_array)
            top_10_description_df.at[column_name, 'Shapiro-Wilk Test Statistic'] = statistic
            top_10_description_df.at[column_name, 'Shapiro-Wilk Test P-Value'] = p_value
        st.subheader('Statistics & Ratios')
        st.dataframe(top_10_description_df, width=1500)
        st.write('Mean: The average value of a set of numbers')
        st.write('Standard Deviation (Sigma): A measure of how spread out numbers are')
        st.write('Variance: A measure of how far each number in a dataset is from the mean')
        st.write('Skew: Indicates whether a distribution is asymmetrically tails weighted. A positive skew has a longer, fatter tail to the right, while a negative skew has a longer, fatter tail to the left. In trading, we want a postive skew as this means the asset trends up over time.')
        st.write('Excess Kurtosis: A measure of how heavy-tailed a distribution is compared to a normal distribution - positive excess kurtosis indicates heavier tails and peakiness relative to a normal distribution, while negative excess kurtosis indicates lighter tails and flatness.')
        st.write('Fourth Moment: A high fourth moment value indicates that a distribution has heavier tails and a higher peak compared to a normal distribution. This is also known as positive excess kurtosis.')
        st.write('The Shapiro-Wilk statistic: A test statistic used in the Shapiro-Wilk test to check for normality of a data sample. It tests the null hypothesis that the data was drawn from a normally distributed population. The statistic W is calculated from the ordered sample values. If W is close to 1, it indicates the data is likely from a normal distribution. Small values of W indicate departure from normality.')
        #even weighted portfolio
        port_weights = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1 ,0.1, 0.1, 0.1, 0.1])
        #backtesting
        symbol = st.sidebar.text_input('Enter Symbol:', value='BTC', max_chars=None, key=None, type='default')
        data = yf.download(symbol + '-USD', period='1y', end=None)
    

        

if option == 'Social':
    st.subheader('Social Dashboard logic')

    import requests
    #pull ohlc direct from binance 
    market = 'BTCUSDT'
    tick_interval = '1h'

    url = 'https://api.binance.com/api/v3/klines?symbol=' + market + '&interval=' + tick_interval
    data = requests.get(url).json()
    df = pd.json_normalize(data)

    st.dataframe(data)

    eth_Ticker = yf.Ticker("ETH-USD")
    eth_Data = eth_Ticker.history(period="max")
    st.dataframe(eth_Data)
# Example usage:
# eth_data = get_binance_data_by_requests(ticker='ETHUSDT', interval='4h', start='2020-01-01 00:00:00', end='2023-07-01 00:00:00')

    data2 = yf.download('ETH' + '-USD', period='1y', end=None)
    df_2 = pd.DataFrame(data2)
    st.dataframe(df_2)
    st.dataframe(df_2['Adj Close'])
   

if option == 'Derivatives':
    st.subheader('Derivatives Dashboard logic')

    #initiate exchanges
    binance = ccxt.binance()
    upbit = ccxt.upbit()
    okx = ccxt.okx()
    coinbase = ccxt.coinbase()
    bybit = ccxt.bybit()
    bitget = ccxt.bitget()
    mexc = ccxt.mexc() 
    gate = ccxt.gateio()
    huobi = ccxt.huobi()
    kucoin = ccxt.kucoin()
    bitfinex = ccxt.bitfinex()
    bitmart = ccxt.bitmart()
    bingx = ccxt.bingx()
    coinex = ccxt.coinex()
    phemex = ccxt.phemex()
    ticker = st.text_input('Select Trading Pair:', value='BTC/USDT', max_chars=None, key=None, type='default')
    
    


    
    
    
    

#loop through csv files for price data
#def index():
#    pattern = request.arg.get('pattern', None) #get pattern from url
#    if pattern:
#        datafiles = os.listdir('datasets/daily')
#        for dataset in datafiles:
#            pd.read_csv('datasets/daily/{}'.format(filename))
#            print (df)
#            pattern_function = getattr(talib, pattern)
#            try:
#               result = talib.pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
#               last = result.tail(1).values[0]
#               print(last)
#               if last =! 0:
#               print("{} triggered {}".format(filename, pattern))
#            except:
#               pass
#    return render_template('index.html', patterns=patterns)    


# select a symbol symbol = st.sidebar.text_input('Enter Symbol:', value='BTC-USD', max_chars=None, key=None, type='default')
# create a candlestick chart in plotly     fig = go.Figure(data=[go.Candlestick(x=data.index,
#                    open=data['Open'],
#                   high=data['High'],
#                    low=data['Low'],
#                    close=data['Close'],
#                    name=symbol)])
#   fig.update_xaxes(type='category')
#    fig.update_layout(height=1000)

#   st.plotly_chart(fig, use_container_width=True)
#    st.write(data)
