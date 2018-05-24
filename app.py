from flask import Flask, render_template, request, redirect

import quandl
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components, file_html


app = Flask(__name__)

def stock_data(stock_ticker):
    quandl.ApiConfig.api_key = 'T4z6hhaw3bnHxCm7Z-xh'
    data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['date', 'close'] }, ticker = stock_ticker, date = { 'gte': '2018-02-27', 'lte': '2018-03-27' })

    return data
@app.route('/', methods=['POST', 'GET'])
def main():
    return redirect('/form')


@app.route('/form', methods=['POST', 'GET'])
def index():

  if request.method == "POST":
      stock_ticker = request.form['Stock ticker']
      closing_price_month = stock_data(stock_ticker)

      p = figure(title="Last month closing price", x_axis_label='Date', y_axis_label='Price', x_axis_type='datetime')
      p.line(closing_price_month['date'], closing_price_month['close'], line_width=6, line_color='#0f9d58')
      script, div = components(p)
      #show(p)


      return render_template('plot.html', script=script, div=div, stock_ticker=stock_ticker, closing_price_month=closing_price_month.head())
  else:

      return render_template("form.html")


@app.route('/about')
def about():
  return render_template('about.html')

# With debug=True, Flask server will auto-reload

if __name__ == '__main__':
  app.run(port=33507)
