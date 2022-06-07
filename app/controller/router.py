from app.model.Popularity import Popularity
from app import app, db
from flask import redirect, render_template, Response, url_for, request
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import prometheus_client
from prometheus_client import Counter
from pytrends.request import TrendReq
import nltk
import pandas as pd
import base64
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image
import wordcloud
import numpy

total_requests = Counter('request_count', 'Total webapp request count')
list_requests = Counter('list_request_count', 'Total list request count')
plot_requests = Counter('plot_request_count', 'Total plot request count')
nltk.download('punkt')
nltk.download('stopwords')

@app.route('/', methods=['GET','POST'])
def show_entries():
    total_requests.inc()
    if request.method == "POST":
        c = request.form.get('nm', '')
        f = request.form.get('from', '')
        t = request.form.get('to', '')
        if (f == '' or t == ''):
            return redirect(url_for("google_search",company=c))
        else:
            return redirect(url_for("google_search",company=c, _from=f, _to=t))
    else:
        return render_template('index.html')

@app.route('/metrics')
def requests_count():
    total_requests.inc()
    return Response(prometheus_client.generate_latest(), mimetype='text/plain')

def get_interest_over_time(keywords=["tsmc", "Applied Materials", "ASML", "SUMCO"], timeframe='all'):
    pytrends = TrendReq(hl='zh-TW', tz=-480)
    pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
    return pytrends.interest_over_time()

@app.route('/list')
def _list():
    list_requests.inc()
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
    total_requests.inc()
    plot_requests.inc()
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
        return int.from_bytes(byte, sys.byteorder)
    return dict(byte_to_int=byte_to_int)

class GoogleCrawler():
    def __init__(self):
        self.url = 'https://www.google.com/search?q='    

    def get_source(self,url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    def google_search(self,query,timeline='',page='0'):
        url = self.url + query + '&tbs={timeline}&start={page}&filter=0&lr=lang_en'.format(timeline=timeline,page=page)
        print('[Check][URL] URL : {url}'.format(url=url))
        response = self.get_source(url)
        return self.parse_googleResults(response)

    def parse_googleResults(self,response):
        css_identifier_result = "tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = "yuRUbf"
        css_identifier_text = "VwiC3b"
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.findAll("div", {"class": css_identifier_result})
        output = []
        for result in results:
            item = {
                'title': result.find(css_identifier_title).get_text(),
                'link': result.find("div", {"class": css_identifier_link}).find(href=True)['href'],
                'text': result.find("div", {"class": css_identifier_text}).get_text()
            }
            output.append(item)
        return output
    
    def html_parser(self,htmlText):
        soup = BeautifulSoup(htmlText, 'html.parser')
        return soup

    def html_getText(self,soup):
        orignal_text = ''
        for el in soup.find_all('p'):
            orignal_text += ''.join(el.find_all(text=True))
        return orignal_text
    
    def word_count(self, text):
        counts = dict()
        stop_words = set(stopwords.words('english'))
        List=["(", ")", "&", ".", "'", ":", "`", "—", ",", "%", "’", "'s", "The"]
        words = word_tokenize(text)
        #words = text.replace(',',' ').split()
        for word in words:
            if word not in stop_words and word not in List:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
        return counts



@app.route('/google_search/<company>', defaults={'_from':None, '_to':None})
@app.route('/google_search/<company>/<_from>/<_to>')
def google_search(company, _from, _to):
    '''
    _from : (MM.DD.YYYY)
    _to : (MM.DD.YYYY)
    '''
    crawler = GoogleCrawler()
    query = '\"{company}\"'.format(company=company)
    if _from and _to:
        timeline = f"cdr:1,cd_min:{_from.replace('.', '/')},cd_max:{_to.replace('.', '/')}"
    else:
        timeline = "qdr:h"
    results = crawler.google_search(query, timeline, '1')

    arr = []
    result_wordcount = {}

    for i in results:
        if ".pdf" not in i['link']:
            arr.append(i['link'])

    for url in arr:
        response = crawler.get_source(url)
        soup = crawler.html_parser(response.text)
        orignal_text = crawler.html_getText(soup)
        temp = crawler.word_count(orignal_text)

        if bool(result_wordcount) == False:
            result_wordcount = temp
        else:
            for i,j in temp.items():
                if (i in result_wordcount.keys()):
                    result_wordcount[i] += j
                else:
                    result_wordcount[i] = j

    #print(sorted(result_wordcount.items(), key=lambda x:x[1], reverse=True))

    if bool(result_wordcount) == False:
        decoded = base64.b64encode(open('wordcloud\Tsmc.svg.png', "rb").read()).decode('ascii')
    else:
        pic = numpy.array(Image.open('wordcloud\clouds.png'))
        pic = (pic==0)*255
        wc = wordcloud.WordCloud(background_color='white',
                        margin=2,
                        mask=pic,
                        #font_path = 'kaiu.ttf',
                        #max_words=50,
                        #width=1080, height=720,
                        # relative_scaling=0.5
                        )
        wc.generate_from_frequencies(result_wordcount)
        wc.to_file('wordcloud\wordcloud.jpg')
        decoded = base64.b64encode(open('wordcloud\wordcloud.jpg', "rb").read()).decode('ascii')
    return render_template('plot.html', imagedata=decoded) 