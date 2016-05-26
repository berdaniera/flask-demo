from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
from bokeh.embed import components
import requests as req
import numpy as np
import pandas as pa
#import matplotlib.pyplot as plt
#import seaborn as sea

app = Flask(__name__)

app.nms = pa.read_csv('https://s3.amazonaws.com/static.quandl.com/tickers/SP500.csv')

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    names = app.nms.name
    if request.method == 'GET':
        return render_template('index.html',names = names)
    else: #requets is post
        name = request.form['option']
        stock = app.nms.ticker.where(app.nms.name==name).max()
        mykey = '3RbnxyoJSBxcXqhvNMa2'
        r = req.get('https://www.quandl.com/api/v3/datasets/WIKI/'+stock+'/data.json?api_key='+mykey)
        #r.headers['content-type']
        out = r.json()
        dat = pa.DataFrame(out['dataset_data']['data'],columns=out['dataset_data']['column_names'])
        dat.Date = pa.to_datetime(dat.Date)

        p1 = figure(x_axis_type = "datetime", responsive=True, plot_height=300, plot_width=900)
        p1.title = name+' daily high and low'
        # p1.grid.grid_line_alpha=0
        p1.xaxis.axis_label = 'Date'
        p1.yaxis.axis_label = 'Price'

        p1.line(dat.Date, dat.Low, color='#CA0020', legend='Low')
        p1.line(dat.Date, dat.High, color='#0571B0', legend='High')

        script, div = components(p1)
        # add bokeh stuff
        return render_template('next.html', script=script, div=div, names = names, nm = name)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=5555,debug=True)
