"""
@author:mythreyi.k
Created on:16/03/2019
Last Update:17/03/2019
"""
from bs4 import BeautifulSoup
import urllib2
import pandas
from string import ascii_uppercase
import re
from urlparse import  urljoin
import csv


class MediNetScrapper:
   
    def __init__(self):
        
        self.site_url="https://www.medindia.net/drug-price/"
        self.base_url="https://www.medindia.net/drug-price/index.asp?alpha="
        self.drug_names=['drug_name']
        self.dosages=['dosage']
        self.brand_names=['brand_name']
        self.manufacturer_names=['brand_name']
        self.cost=['price']
        self.type=['type']
        self.MedDataFrame=pandas.DataFrame()
      
    def scrapBrandNameandType(self,url):
        
        html = urllib2.urlopen(url).read()
        bd_ty_soup_obj = BeautifulSoup(html)
        bd_ty_table= bd_ty_soup_obj.find( "table", {"class":"table-bordered table table-hide-5 table-hide-1 table-font-md"} )
        rows=bd_ty_table.findAll("tr")[1:]
        for td in rows :
            try:
                int(td.findAll("td")[0].get_text())
                import pdb;pdb.set_trace()
                self.brand_names.append(td.findAll("td")[1].get_text().strip())
                self.manufacturer_names.append(td.findAll("td")[2].get_text().strip())
                self.type.append(td.findAll("td")[3].get_text().strip())
                self.dosages.append(td.findAll("td")[4].get_text().strip())
                cost_and_dosage_page_url=td.findAll("td")[5].find('a', attrs={'href': re.compile("^https://")}).get('href')
                self.cost.append(self.scrapCostperunit(cost_and_dosage_page_url))
                
            except Exception,e:
                print e
                pass  
              
    def scrapCostperunit(self,url):
      
        html = urllib2.urlopen(url).read()
        dose_cost_soup_obj = BeautifulSoup(html)
        values=dose_cost_soup_obj.find( "div", {"class":"ybox"})
        value_list=values.get_text().strip().split()
        cost=float(value_list[0].strip().replace(',',''))
        
        try:
          qty=int(re.search('([0-9]+)',value_list[2]).group())
        except:
          try:
            qty=int(re.search('([0-9]+)',value_list[-1]).group())
          except:
            qty=None
          
        cost_per_unit=cost/qty if qty else cost
        return cost_per_unit
      
    def populateDataFrame(self):
       print self.drug_names
       print self.brand_names
       print self.dosages
       print self.type
       print self.cost
       with open('data.csv', 'wb') as myfile:
          wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
          wr.writerow(self.drug_names)
          wr.writerow(self.brand_names)
          wr.writerow(self.dosages)
          wr.writerow(self.type)
          wr.writerow(self.cost)
       

     
          
        
    def start_scrapping(self):
      
        for alphabet in ascii_uppercase:
            html = urllib2.urlopen((self.base_url+alphabet)).read()
            root_soup_obj = BeautifulSoup(html)
            base_table= root_soup_obj.find( "table", {"class":"table-bordered table"} )
            rows=base_table.findAll("tr")[1:2]
            count=0
            for td in rows :
              try:
                  int(td.findAll("td")[0].get_text())
                  self.drug_names.extend([td.findAll("td")[1].get_text().strip()]*int(td.findAll("td")[2].get_text()))
                
                   
                  if td.findAll("td")[3].get_text().strip()!='-':
                      
                      self.drug_names.append(td.findAll("td")[1].get_text().strip())
                      branch_and_type_page_url=urljoin(self.site_url,td.findAll("td")[3].find('a', attrs={'href': re.compile("\.htm$")}).get('href'))
                      self.scrapBrandNameandType(branch_and_type_page_url)
                      
                      #if td.findAll("td")[4].get_text().strip()!='-':
                  #    branch_and_type_page_url=urljoin(self.site_url,td.findAll("td")[4].find('a', attrs={'href': re.compile("\.htm$")}).get('href'))
                 
              except Exception,e:
                  print e
                  
        self.populateDataFrame()  
       
              
if __name__=="__main__":
   
    medicine_scrapper_obj=MediNetScrapper()
    medicine_scrapper_obj.start_scrapping()
