from app.model.Popularity import Popularity
from pytrends.request import TrendReq
import base64

from app import app, db
from flask import render_template,Response
import prometheus_client
from prometheus_client import Counter

# Store dataframe in Flask session
df = None

total_requests = Counter('request_count', 'Total webapp request count')
list_requests = Counter('list_request_count', 'Total list request count')
plot_requests = Counter('plot_request_count', 'Total plot request count')

@app.route('/')
def show_entries():
    total_requests.inc()
    return render_template('index.html')

@app.route('/metrics')
def requests_count():
    total_requests.inc()
    return Response(prometheus_client.generate_latest(), mimetype='text/plain')



@app.route('/list')
def _list():
    list_requests.inc()
    total_requests.inc()
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
    total_requests.inc()
    plot_requests.inc()
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
