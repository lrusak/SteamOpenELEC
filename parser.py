from bs4 import BeautifulSoup
import json

try:
    import urllib.request as urllib2
except:
    import urllib2
    
json_data = open('GAMES.json')
data = sorted(json.load(json_data), key=lambda x: [int(x)])

json_data2 = open('GAMES.json')
data2 = json.load(json_data2)

cookies = [['cookie', 'birthtime=28801'],
           ['cookie', 'path=/'],
           ['cookie', 'domain=store.steampowered.com']]

print('AppID\tWorks\tTitle')
print('---------------------------------------------------------------')

for i in data:
  try:
    if data2['%s' % i]['Hidden']:
      continue
  except (TypeError, KeyError) as e:
    url = 'http://store.steampowered.com/app/' + i
    req = urllib2.Request(url)
    req.add_header(cookies[0][0], cookies[0][1] + "; " + cookies[1][1] + ";" + cookies[2][1])
    res = urllib2.urlopen(req)
    soup = BeautifulSoup(res.read())
    title = soup.find('div', attrs={'class': 'apphub_AppName'})
    try:
      print(i + '\t' + str(data2['%s' % i]) + '\t' + title.contents[0])
    except AttributeError:
      print(i + '\tError')
json_data.close()
