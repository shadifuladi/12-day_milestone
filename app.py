from bokeh.plotting import figure
from bokeh.embed import components
import pandas as pd
import requests
from flask import Flask, render_template, request, redirect
from alpha_vantage.timeseries import TimeSeries


def myFetch(ticker, price):
   API_KEY = 'JOLFH26C08JHRMJ8'
   # stock_name = 'AAPL'
   r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=' + API_KEY)
   
   #ts = TimeSeries(API_KEY, output_format="pandas", indexing_type="integer)
   #data, meta_data = ts.get_monthly_adjusted(symbol=ticker.upper())

   result = r.json()	
   df = pd.DataFrame(result['Time Series (Daily)'])
   return df

def myPlot(df, price, ticker):
    p = figure(title="This is the plot!", x_axis_type="datetime", x_axis_label="Date",
               y_axis_label="Stock price", plot_width=1000)

    mapping = {'open': 'open', 'adjOpen': 'adj. open', 'close': 'close', 'adjClose': 'adj. close'}
    colour = {'open': 'orange', 'adjOpen': 'red', 'close': 'blue', 'adjClose': 'green'}

    for p in price:
        p.line(df.index, df[mapping[s]], color=colour[s], legend=ticker + ": " + mapping[s])
    return p

app = Flask(__name__)
app.vars = {}

@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
# if request.method == 'GET':
    return render_template('index.html')
# else:

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    app.vars['ticker'] = request.form['ticker']
    #ticker = ticker.upper()
    app.vars['price'] = request.form.getlist('priceType')

    data = myFetch(ticker)
    plot = myPlot(data, price, ticker)

    script, div = components(plot)
    reqUrl = "https://www.google.com/finance?q=" + ticker
    return render_template('graph.html', script=script, div=div, reqUrl=reqUrl)


if __name__ == '__main__':
  app.run(port=33507)
