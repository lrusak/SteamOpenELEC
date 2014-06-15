from bs4 import BeautifulSoup
import json
import sys

try:
    import urllib.request as urllib2
except:
    import urllib2
    
json_data = open(sys.argv[1])
data = sorted(json.load(json_data), key=lambda x: [int(x)])

json_data2 = open(sys.argv[1])
data2 = json.load(json_data2)

cookies = [['cookie', 'birthtime=28801'],
           ['cookie', 'path=/'],
           ['cookie', 'domain=store.steampowered.com']]
           
layout = [["" for value in range(6)] for value in range(0,1000)]
# 0 index
# 1 appid
# 2 works
# 3 beta
# 4 title
# 5 comment

print('%5s %6s %5s %4s  %s %s' % ('Index','AppID','Works','Beta','{0: <70}'.format('Title'),'Comment'))
#print('Index\tAppID\tWorks\tBeta\tTitle\t\t\t\t\t\t\t\t\t\tComment')
print('-------------------------------------------------------------------------------------------------------')

j = 0

for i in data:
  try:
    if data2['%s' % i] is not None:
 
      url = 'http://store.steampowered.com/app/' + i
      req = urllib2.Request(url)
      req.add_header(cookies[0][0], cookies[0][1] + "; " + cookies[1][1] + ";" + cookies[2][1])
      res = urllib2.urlopen(req)
      soup = BeautifulSoup(res.read())
      title = soup.find('div', attrs={'class': 'apphub_AppName'})
      
      layout[j][0] = j
      layout[j][1] = i
      
      try:
        if title.contents[0] is not None:
          layout[j][4] = title.contents[0]
          
      except AttributeError as e:
        j = j + 1
        continue
      else:
        try:
          if data2['%s' % i]['Hidden'] is True:
            j = j + 1
            continue
        except (TypeError, KeyError) as e:
          layout[j][2] = str(data2['%s' % i])
          
        try:
          layout[j][3] = str(data2['%s' % i]['Beta'])
          layout[j][2] = ""
        except (TypeError, KeyError) as e:
          pass
          
        try:
          layout[j][5] = str(data2['%s' % i]['Comment'])
          layout[j][2] = ""
        except (TypeError, KeyError) as e:
          pass

    print('%5s %6s %5s %4s  %s %s' % (layout[j][0],layout[j][1],layout[j][2],layout[j][3],'{0: <70}'.format(layout[j][4]),layout[j][5]))
#    print("\t".join('%s' % x for x in layout[j]))
    j = j + 1
      
      #try:
        #if data2['%s' % i]['Beta'] is True:
          #print(i + '\tBeta\t' + title.contents[0])
      #except (TypeError, AttributeError) as e:
        #try:
          #print(i + '\t' + str(data2['%s' % i]) + '\t' + title.contents[0])
        #except (AttributeError) as e:
          #print(i + '\terror')
  except KeyError as e:
    pass
json_data.close()
