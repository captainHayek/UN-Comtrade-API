import glob
import time
start = time.time()
import requests
import pandas as pd
import csv
import numpy as np
import tkinter
from tkinter import filedialog
from tkinter import *
from tkinter import Tk
import sys
import unicodedata
import os
import pip
import json
import random as rn
tkinter.Tk().withdraw()

try:
    from pip import main
except:
    from pip._internal import main
## The below section of code checks to see if your system has the "Selenium" package installed
try:
    ##from pip._internal import main ### for pip v19+
    ##pip.main(['install', '--proxy=https://webproxy.agdaff.gov.au:8080', 'pypyodbc']) ## for pip version 9
    import selenium
    from selenium.webdriver.common.proxy import *
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except:
    main(['install', '--proxy=https://webproxy.agdaff.gov.au:8080', 'selenium']) ## for pip version 19+
    import selenium
    from selenium.webdriver.common.proxy import *
    from selenium import webdriver
    from selenium.webdriver.common.by import By
try:
    ##from pip._internal import main ### for pip v19+
    ##pip.main(['install', '--proxy=https://webproxy.agdaff.gov.au:8080', 'pypyodbc']) ## for pip version 9
    import bs4
    from bs4 import BeautifulSoup
except:
    main(['install', '--proxy=https://webproxy.agdaff.gov.au:8080', 'bs4']) ## for pip version 19+
    import bs4
    from bs4 import BeautifulSoup

proxies = {"https":"webproxy.agdaff.gov.au:8080"}

def pause():
    sleep = rn.uniform(1,2)
    time.sleep(sleep)
    print("Waiting " + str(round(sleep,2)) + " seconds before next call")
#try:
#    color = sys.stdout.shell
#except AttributeError: raise RuntimeError("Use IDLE")

# You can add to this section below to request a direct input of the pest taxon from the user
#print ("Select the CSV file which contains your taxonomic names")
#print("")
#filename = filedialog.askopenfilename()
#print("You selected " + str(filename))
#print("")
#print ("Select the United Nations Country code and GeoCodes CSV file")
#print("")
## The line below sets the path to the Country Lat/Long file - this can be updated and maintained as necessary - not all countries appear to have UnComtrade codes
#UNandGeoCodesFile = r"\\act001cl04fs08\piaphdata$\Plant_Health_Policy\Nat_Prog\Surveillance\International Surveillance\Data\DistributionDataScript\CountryGeocodes.csv"
print("Select the folder to which you would like the output Distribution files saved to")
print("")
distributionFolder = filedialog.askdirectory()
distributionFolderStr=str(distributionFolder)
print("You selected " + distributionFolder + " as the storage folder for the Taxaas matched output CSV file.")
print("")

proxies = {"https":"webproxy.agdaff.gov.au:8080"}

# URL Parameter examples:
# http://comtrade.un.org/api/get/bulk/{type}/{freq}/{ps}/{r}/{px}?{token=}
#
# "r=598&freq=M&ps=2017&px=HS&type=C&token=?
# r=598   ---   This requests data for the "r"eporter country, 598 is the UnCode for Papua New Guinea
#               list of UN country codes is available at https://comtrade.un.org/Data/cache/reporterAreas.json
# freq=M  ---   This request "M"onthly or "A"nnual data series
# ps=2017 ---   Set the year for the data series
# px=HS   ---   Set the classification system for the data series,"HS" = Harmonized System as reported
#               list of classification codes is available at https://comtrade.un.org/Data/doc/api/bulk/
# type=C  ---   "C"ommodities or "S"ervices are the two options available
# token=? ---   Authentication token if available is optional

# "http://comtrade.un.org/api/get?max=50000&type=C&freq=A&px=HS&ps=2013&r=826&p=0&rg=all&cc=ALL&fmt=csv"
# "http://comtrade.un.org/api/get?max=50000&type=C&freq=A&px=HS&ps=2017&r=598&p=36&rg=all&cc=ALL&fmt=json"

    
citrusCodes = ['080510','080520','080530','080540','080550','080590']

fruitCodes = ['080000']

url = "https://comtrade.un.org/api//refs/da/bulk"

url2 = "https://comtrade.un.org/api/get?max=50000&type=C&freq=M&px=HS&ps=2017,2016,2015,2014,2013&r=36&p=all&rg=all&cc=" #080510&fmt=csv"
#url2 = "http://comtrade.un.org/api/get?max=50000&type=C&freq=A&px=HS&ps=2017&r=598&p=36&rg=all&cc="
url3 = "&fmt=json"

hsCodesFile = r"\\act001cl04fs08\piaphdata$\Plant_Health_Policy\Nat_Prog\Surveillance\International Surveillance\Data\DistributionDataScript\harmonisedCodes6D.csv"
hsCodesFrame = pd.read_csv(hsCodesFile, low_memory=False, na_filter=False, encoding="cp1252")
blankUNtradefile = r"\\act001cl04fs08\piaphdata$\Plant_Health_Policy\Nat_Prog\Surveillance\International Surveillance\Data\DistributionDataScript\comtradeMain.csv"
csvMainUNdata = pd.read_csv(blankUNtradefile, low_memory=False, na_filter=False)

for code in range(0,len(citrusCodes)):
    urlUn = url2 + str(citrusCodes[code]) + url3
    print(urlUn)
    #UNresponse = json.loads(requests.get(urlUn,proxies=proxies).text)
    pause()
    frame = pd.DataFrame(json.loads(requests.get(urlUn,proxies=proxies).text)['dataset'])
    if len(frame.columns) > 0:
        csvMainUNdata = pd.merge(csvMainUNdata,frame,on=['AltQuantity', 'CIFValue', 'FOBValue', 'GrossWeight', 'IsLeaf',
           'NetWeight', 'TradeQuantity', 'TradeValue', 'aggrLevel', 'cmdCode',
           'cmdDescE', 'cstCode', 'cstDesc', 'estCode', 'motCode', 'motDesc',
           'period', 'periodDesc', 'pfCode', 'pt3ISO', 'pt3ISO2', 'ptCode',
           'ptCode2', 'ptTitle', 'ptTitle2', 'qtAltCode', 'qtAltDesc', 'qtCode',
           'qtDesc', 'rgCode', 'rgDesc', 'rt3ISO', 'rtCode', 'rtTitle', 'yr'],how="outer")

csvMainUNdata.to_csv(distributionFolder + r"\Merged_UNcomtradeData.csv", index=False)
    
                      
      




## The below fram will be used to extract the  UN country code for passing to the api
#UNandGeoCodes = pd.read_csv(UNandGeoCodesFile, low_memory=False, na_filter=False,encoding="ISO-8859-1")
#csvTaxaData = pd.read_csv(filename, low_memory=False, na_filter=False)
#csvTaxaData.columns = csvTaxaData.columns.str.strip() ## strip white spaces at beginning and end of string in all columns


## This section checks the UNComtrade database
#print("")
#print("==================================")
#print("Checking the UNComtrade database")
#print("==================================")
#print("")


#pestDistributionDataFiles = glob.glob(str(distributionFolder) +"/*.csv")
#partnerCountryUNCodeList = [626]
#
#for pest in range(0,len(pestDistributionDataFiles)):
#    pestFile = pestDistributionDataFiles[pest]
#    pestFileSplit = pestFile.split('''\\''')
#    pestInt = (int(len(pestFileSplit))-1)
#    pName = pestFileSplit[pestInt].split("_")
#    pestName = pName[0]
#    csvPestData = pd.read_csv(pestDistributionDataFiles[pest], low_memory=False, na_filter=False)
#    ## Next step is to Construct api query to retrieve partner country trade with codes in partnerCountryUNCodeList   
#
### This section will be for UN ComTrade API data requests
###4dURL = r("https://comtrade.un.org/api/get?") ##r=36&px=HS&ps=2017&p=ALL&rg=2&cc=0601&type=C&freq=A", proxies=proxies)
#
### The code for the partner country list can be added to or alternatively changed to a user keyboard or CSV input field
#
#
#livePlants6dCodes
#
#partnerImport6dURL = r("https://comtrade.un.org/api/get?r=152&px=HS&ps=2017&p=ALL&cc=AG6&type=C&freq=A", proxies=proxies)
#partnerExport6dURL = r("https://comtrade.un.org/api/get?r=152&px=HS&ps=2017&p=ALL&cc=AG6&type=C&freq=A", proxies=proxies)
#
#ausImport6dURL = r("https://comtrade.un.org/api/get?r=152&px=HS&ps=2017&p=ALL&cc=AG6&type=C&freq=A", proxies=proxies)
#ausExport6dURL = r("https://comtrade.un.org/api/get?r=152&px=HS&ps=2017&p=ALL&cc=AG6&type=C&freq=A", proxies=proxies)



end = time.time()

print("")

seconds = end-start
minutes = seconds/60
hours = minutes/60
if hours >1:
	print("It took " + str(hours) + " hours to complete this task.")
else:
	print("It took " + str(minutes)[0:4] + " minutes to complete this task.")
