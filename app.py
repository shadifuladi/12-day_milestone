import requests
from flask import Flask, render_template, request, redirect


#########################
# get data:
#########################

def myFetch(ticker):
   API_KEY = 'JOLFH26C08JHRMJ8'
   stock_name = 'AAPL'
   r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock_name + '&apikey=' + API_KEY)
   result = r.json()	
   df = pd.DataFrame(result['Time Series (Daily)'])
   return df

#########################
# myPlot function, plots the data!
#########################

def myPlot(df, sel, ticker):
    p = figure(title="AAPL Prices", x_axis_type="datetime", x_axis_label="Date",
               y_axis_label="Stock price", plot_width=1000)
    mapping = {'open': 'open', 'adjOpen': 'adj. open', 'close': 'close', 'adjClose': 'adj. close'}
    colour = {'open': 'orange', 'adjOpen': 'red', 'close': 'blue', 'adjClose': 'green'}
    for s in sel:
        p.line(df.index, df[mapping[s]], color=colour[s], legend=ticker + ": " + mapping[s])
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
    sel = request.form.getlist('priceType')
    data = myFetch(ticker)
    plot = myPlot(data, sel, ticker)
    script, div = components(plot)
    reqUrl = "https://www.google.com/finance?q=" + ticker
    return render_template('graph.html', script=script, div=div, reqUrl=reqUrl)
if __name__ == '__main__':
  app.run(port=33507)
