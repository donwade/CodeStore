#importing the libraries needed 
import os  # for cls()
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint

# bot detection bypass.
import random

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]


#Declaring the headers if forcing english is required. 
#headers = {"Accept-Language": "en-US,en;q=0.5"}

#declaring the list of empty variables, So that we can append the data overall

SiteNumber = []
SiteName = []
SiteLocation = []
SiteFrequencies=[]
SiteDescription = []

# creating an array of values and passing it in the url for dynamic webpages
# range from 1 to 1000 counting by 100

RadioZoneHttp = 'https://www.radioreference.com/db/sid/2560'
RadioFileName = 'BellZone2Sites'
os.system('clear')

#the whole core of the script
try:
    print ("getting page ", RadioZoneHttp)
    page = requests.get( RadioZoneHttp, headers={'User-Agent': random.choice(user_agents_list)})
 
    page.raise_for_status()

    soup = BeautifulSoup(page.text, 'html.parser')
    #print (soup)
    # top of the area of interest where everything below is the movie
    aSite = soup.find('div', id ='sites_div')
    #print(aSite)

    siteTable = aSite.find('table', class_='table table-sm table-responsive table-bordered')
    #print ("siteTable = ", siteTable, "\n\n")

    # this is a list of td-'data-txt fit' objects.
    manySiteNums = siteTable.findAll('td', class_='data-text fit')
    
    print ("manySiteNums = ", manySiteNums, "\n\n")
    for aSite in manySiteNums:
        print ("------\n\taSite = ", aSite)
        print ("\taSite.text = ", aSite.text, "\n")
        SiteNumber.append(aSite.text)


    manyNames = siteTable.find_all('td', style='width: 100%', class_=None)
    print (manyNames)
    for aName in manyNames:
        print ("-----\n\taName = ", aName)
        print ("\taName.text = ", aName.text)
        SiteName.append(aName.text)

    manyLocations = siteTable.find_all('td', style='width: 100%', class_='noWrapTd')
    print (manyLocations)
    for aLocation in manyLocations:
        print ("-----\n\taName = ", aLocation)
        print ("\taName.text = ", aLocation.text)
        SiteLocation.append(aLocation.text)


    #creating a dataframe 
    site2List = pd.DataFrame({ "SiteNum": SiteNumber, "Site Name" : SiteName, "Location": SiteLocation } )

    site2List.head(5)

    print (site2List)   # this makes it pop up to display first and last 5 lines.


    # #saving the data in excel format
    site2List.to_excel(RadioFileName + str(".xlsx"))

    #If you want to save the data in csv format
    site2List.to_csv(RadioFileName + str(".csv"))

except Exception as e:
    print (e)



try:
    manyChannels = siteTable.findAll('td', class_='data-text')
    manyControls = siteTable.findAll('td', class_='data-text ctrl-pri')

    # the name of the site has no class, other entities with style tag do.
    manyNames = siteTable.findAll('td', style='width: 100%', class_=None)
    #print (manyNames)

    for aName in manyNames:
        theName = aName.a.text
        print ("Site name = ", theName)
       

    manyLocations  = siteTable.findAll('td', style='width: 100%', class_='noWrapTd')

    print(" ")

    voiceChans=''
    controlChans=''

    print( 'ssss = ', manyChannels[1].text)
    for channel in manyChannels:

        aChannel = channel.text

        if aChannel.find('c') != -1 :
            print ("CONTROL = ", aChannel)
            aChannel = aChannel[:-1]  # remove the 'c'
            controlChans = controlChans + str(aChannel) + ','

        elif aChannel.find('(') != -1 :

            # starting new site, barf out past sites channels
            print(" ")
            controlChans = controlChans[:-1]    # remove tailing comma
            voiceChans = voiceChans[:-1]        # remove tailing comma
            print ( controlChans)
            print ( voiceChans)

            print("\n====================")

            print ("SITE = ", aChannel)
            voiceChans = ''
            controlChans = ''
        
        else:
            voiceChans = voiceChans + str(aChannel) + ','
            print (aChannel)


    # no more sites left, dump the guts of the last site
    controlChans = controlChans[:-1]    # remove tailing comma
    voiceChans = voiceChans[:-1]        # remove tailing comma
    print ( controlChans)
    print ( voiceChans)
    print ("-----------------------------------\n")
#    for control in manyControls:
#        ctrlChan = control.text
#        print (ctrlChan)

#    for site in manySites:
#        print (site.text)
#        SiteNumber.append(site.text)

    for aname in manyNames:
        name = aname.a.text
        print ("Site Name = ", name)
        SiteName.append(name)

    quit()
    for aLocation in manyLocations:
        desc = aLocation.a.text
        print(desc)
        SiteLocation.append(desc)

    print ("SiteNumber =", len(SiteNumber), "Site Name = ", len(SiteName), "Site Locations = ", len (SiteLocation))


except Exception as e:
    print (e)
