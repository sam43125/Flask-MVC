from app.model.Popularity import Popularity
from pytrends.request import TrendReq
import base64

from app import app, db
from flask import render_template

# Store dataframe in Flask session
df = None

@app.route('/')
def show_entries():
    return render_template('index.html')

@app.route('/list')
def _list():
    global df
    if not Popularity.query.filter_by(TSMC=20).first():
        pytrends = TrendReq(hl='zh-TW', tz=-480)
        kw_list = ["tsmc", "Applied Materials", "ASML", "SUMCO"]
        pytrends.build_payload(kw_list, cat=0, timeframe='all', geo='', gprop='')
        df = pytrends.interest_over_time()
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
    global df
    if isinstance(df, type(None)):
        _list()
    ax = df.plot(figsize=(15, 10), fontsize=20, title="Intrest over time", ylabel="Intrest")
    ax.figure.savefig('popularity.jpg')
    decoded = base64.b64encode(open('popularity.jpg', "rb").read()).decode('ascii')
    return render_template('plot.html', imagedata=decoded) 

@app.context_processor
def utility_processor():
    def byte_to_int(byte):
        # TODO: Check endianness of the running machine
        return int.from_bytes(byte, "little")
    return dict(byte_to_int=byte_to_int)
