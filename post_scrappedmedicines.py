import urllib2
import pandas as pd

data = pd.read_csv('content/data_new.csv', index_col=0, header=None).T
print data
data=df.to_json(orient='records')
print data
url=' http://4d3becb0.ngrok.io/api/push_medicine_detail'
req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
f = urllib2.urlopen(req)
response = f.read()
f.close()
 
