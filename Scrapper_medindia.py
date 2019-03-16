from bs4 import BeautifulSoup
import urllib2
import pandas

def scrap_brandname(url):
  pass
  
df = pandas.DataFrame(columns=['Drug_name','brand_name','dosage'])
url="https://www.medindia.net/drug-price/index.asp?alpha=A"
html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html)

# the first argument to find tells it what tag to search for
# the second you can pass a dict of attr->value pairs to filter
# results that match the first tag
table = soup.find( "table", {"class":"table-bordered table"} )
drug_names=[]


rows=table.findAll("tr")[1:]
for td in rows :
      try:
          int(td.findAll("td")[0].get_text())
          drug_names.append(td.findAll("td")[1].get_text().strip())
          if td.findAll("td")[2].get_text()!='-':
            scrap_brandname()
          
      except:
          pass
    
