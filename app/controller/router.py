from app.model.Popularity import Popularity
from pytrends.request import TrendReq
import pandas as pd
import base64

from app import app, db
from flask import render_template

@app.route('/')
def show_entries():
    return render_template('index.html')

def get_interest_over_time(keywords=["tsmc", "Applied Materials", "ASML", "SUMCO"], timeframe='all'):
    pytrends = TrendReq(hl='zh-TW', tz=-480)
    pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
    return pytrends.interest_over_time()

@app.route('/list')
def _list():
    if not Popularity.query.filter_by(id=1).first():
        df = get_interest_over_time()
        for row in range(len(df)):
            date = df.iloc[row].name
            tsmc = df.iloc[row, 0]
            appliedMaterials = df.iloc[row, 1]
            asml = df.iloc[row, 2]
            sumco = df.iloc[row, 3]
            popularity = Popularity(date, tsmc, appliedMaterials, asml, sumco)
            db.session.add(popularity)
        db.session.commit()
    return render_template('list.html', entries=Popularity.query.all())

@app.route('/plot')
def plot():
    if not Popularity.query.filter_by(id=1).first():
        _list()
    df = popularity_to_dataframe(Popularity.query.all())
    ax = df.plot(figsize=(15, 10), fontsize=20, title="Interest over time", ylabel="Interest")
    ax.figure.savefig('popularity.jpg')
    decoded = base64.b64encode(open('popularity.jpg', "rb").read()).decode('ascii')
    return render_template('plot.html', imagedata=decoded) 

def popularity_to_dataframe(popularities):
    byte_to_int = utility_processor()["byte_to_int"]
    df = pd.DataFrame([(d.date, byte_to_int(d.TSMC), byte_to_int(d.AppliedMaterials), byte_to_int(d.ASML), byte_to_int(d.SUMCO)) for d in popularities], 
                      columns=['date', 'TSMC', 'Applied Materials', 'ASML', 'SUMCO'])
    df.set_index('date', inplace=True)
    return df

@app.context_processor
def utility_processor():
    def byte_to_int(byte):
        # TODO: Check endianness of the running machine
        return int.from_bytes(byte, "little")
    return dict(byte_to_int=byte_to_int)
