import feedparser
import requests
from urllib import request
from selenium import webdriver

brguge = webdriver.PhantomJS()
brguge.get('https://www.baidu.com')
print(brguge.current_url)
brguge.close()

rs = requests.get('https://www.podtrac.com/pts/redirect.mp3/streaming.stuffyoushouldknow.com/sysk/2018-02-29-sysk-ford-pinto-live-atlanta-2-final.mp3?awCollectionId=1003&awEpisodeId=930298')
    
http_headers = { 'Accept': '*/*','Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

feed = feedparser.parse('https://www.howstuffworks.com/podcasts/stuff-you-should-know.rss')
#feed = feedparser.parse('http://www.ifanr.com/feed')

titles = [e.title for e in feed.entries]
if 'mimi' in titles:
    print('got ychat')

buf = {}

def get_real_url(url):
    rs = requests.get('https://www.podtrac.com/pts/redirect.mp3/streaming.stuffyoushouldknow.com/sysk/2018-02-29-sysk-ford-pinto-live-atlanta-2-final.mp3?awCollectionId=1003&awEpisodeId=930298')
    if rs.status_code > 400:
        return 'error'
    return rs.url

for e in feed.entries:
    buf[e.title] = e.link

for t,u in buf.items():
    i = u.index('.mp3')
    if i<0:
        continue
    fu = get_real_url(str(u))
    print('download '+t+' at '+fu)
    with request.urlopen(u) as web:
        with open(t+'.mp3','wb') as outfile:
            outfile.write(web.read())
    break

print('hello, here is what i got')
print(buf)