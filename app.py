import requests
from flask import Flask, render_template, request, redirect
import json
import pandas as pd
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource

#########################
# get data:
#########################

def getURL(ticker, key = 'XXX'):
  url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
  response = requests.get(url)
  return response

def processing(response, price):
  df = pd.read_json(response)
  df_sub = df[5:]
  df_sub.reset_index(inplace=True)
  df_sub['index'] = pd.to_datetime(df_sub['index'])
  df_sub['Time Series (Daily)'].apply(pd.Series)
  df_sub = pd.concat([df_sub, df_sub['Time Series (Daily)'].apply(pd.Series)], axis=1)
  df_final = df_sub[['price']]
  return df_final

#########################
# myPlot function, plots the data!
#########################

def make_graph(df):
  p = figure(x_axis_type='datetime')
  p.line(x='index', y='price',
       source=source,
       line_width=2, color='green')
  p.title.text = ticker
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price in USD'
  return p

#########################
# build the app via flask
#########################

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    ticker = request.form['ticker']
    ticker = ticker.upper()
    price = request.form.getlist('priceType')
    
    response = getURL(ticker)
    df = processing(response, price)
    p = make_graph(df)
    
    script, div = components(p)
    reqUrl = "https://www.google.com/finance?q=" + ticker
    return render_template('graph.html', script=script, div=div, reqUrl=reqUrl)

if __name__ == '__main__':
  app.run(port=33507)
