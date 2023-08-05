#importing the libraries needed 
import os  # for cls()
import pandas as pd
import numpy as np
import requests
import pickle
import pprint

from bs4 import BeautifulSoup
from time import sleep
from random import randint

# use pickle instead of json, pickle supports data types like dicts and tuples
#from json import loads, dumps
from pickle import loads, dumps

# bot detection bypass.
import random

# clear console screen
os.system('clear')

#-------------------------------------------------------------------------

op25GoldenDefaultObj = {
    "channels": [
        {
            "name": "control channel", 
            "trunking_sysname": "Example",
            "device": "rtl0",
            "raw_output": "",
            "demod_type": "fsk", 
            "destination": "smartnet", 
            "excess_bw": 0.35, 
            "filter_type": "fsk2", 
            "if_rate": 18000, 
            "enable_analog": "off",
            "symbol_rate": 3600
        }
    ], 
    "devices": [
        {
            "args": "airspy=0", 
            "frequency": 987654321, 
            "gains": "LNA:39", 
            "name": "rtl0", 
            "offset": 0, 
            "ppm": 0.0, 
            "rate": 3000000, 
            "tunable": True
        }
    ],
    "trunking": {
        "module": "tk_smartnet.py",
        "chans": [
            {
                "sysname": "Example",
                "control_channel_list": "987.654321",
                "tgid_tags_file": "",
                "tgid_hold_time": 2.0,
                "blacklist": "",
                "whitelist": "",
                "bandplan_comment": "OPP https://www.radioreference.com/apps/db/?sid=2560",
                "bandplan": "400",
                "bp_comment": "The bp_ parameters are only used by the 400 bandplan",
                "bp_spacing": 0.015,
                "bp_base": 141.015,
                "bp_base_offset": 380,
                "bp_mid": 151.730,
                "bp_mid_offset": 579,
                "bp_high": 154.320,
                "bp_high_offset": 632
            }
        ]
    },
    "audio": {
        "module": "sockaudio.py",
        "instances": [
            {
                "instance_name": "audio0",
                "device_name": "default",
                "udp_port": 23456,
                "audio_gain": 1.0,
                "number_channels": 1
            }
        ]
    },
    "terminal": {
        "module": "terminal.py",
        "terminal_type": "curses",
        "#terminal_type": "http:127.0.0.1:8080",
        "curses_plot_interval": 0.2,
        "http_plot_interval": 1.0,
        "http_plot_directory": "../www/images",
        "tuning_step_large": 1200,
        "tuning_step_small": 100
    }
}

#-------------------------------------------------------------------------
def setupDefaultJason():
    # op25 files are in an obj format? 
    # python works wants a json file in dictionary format.
    # calling above default.json will fault as json.load wants strings not DICTS

    # 1) take op25 dict and convert into json string.
    # 2) convert json string from 1) to jason.dict
    # 3) use json.dict format from 2) for manipulating data
    # notice slight diff b/n op25 dict and the local dict

    op25JsonString = dumps(op25GoldenDefaultObj)  #takes a json dict and makes a string
    #print ("result of converting op25 json obj into json string\n\n", op25JsonString, "\n")

    # an op25 obj is not compatible with a python3 obj. So we had to convert
    # from oj25 obj to string, string to python obj to allow python to manipulate dict members of obj
    global workingJsonObj
    workingJsonObj = loads(op25JsonString)
    #print ("result of converting op25 string (python object of type = ", type(tempJsonObj)," )\n")
    #print ("tempJsonObj *** ", tempJsonObj, "\n\n")


#-------------------------------------------------------------------------
def getValueOfKeyInList(list_of_keys, keyName):
    try:
        res = [d.get(keyName, None) for d in list_of_keys]  # res is a list []
        print ("\nkey ", keyName, " = " + str(res))
        return res
    
    except StopIteration:
        raise ValueError("No matching record for ", keyName," found")

def setValueOfKeyInList(list_of_keys, keyName, value):
    try:
         for d in list_of_keys:
            res = d.get(keyName, None)  # does d have our keys name?
            old = d.get(keyName, None)
            if ( res != None):
                d[keyName] = value
                print("keyname ", keyName, " was ", old, "now is ", d.get(keyName, None))

    except StopIteration:
        raise ValueError("No dictionary record for ", keyName, " was found")
    
def setValueOfKeyInDict(dictName, keyName, value):
    try:
        list = workingJsonObj[dictName]
        setValueOfKeyInList(list, keyName, value)    
    except:
        raise ValueError("No dictionary record for ", keyName, " was found")
        
def getValueOfKeyInDict(dictName, keyName):
    try:
        list = workingJsonObj[dictName]
        return getValueOfKeyInList(list, keyName)    
    except:
        raise ValueError("No dictionary record for ", keyName, " was found")
        

def testModifyJson():
    # modify simple and complicated values

    print ("demod_type = ", getValueOfKeyInDict('channels', 'demod_type'))
    setValueOfKeyInDict('channels', 'demod_type', 'testing' )
    print ("demod_type = ", getValueOfKeyInDict('channels', 'demod_type'))

    print("\n eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee\n")

    quit()

    #print ("results of modifying some obj entries are ...\n\n", workingJsonObj,"\n\n")

def    printWorkingJson():
    #ttps://stackoverflow.com/questions/55944758/read-a-pickled-dictionary-python
    # make a python data pretty printer.
    print ("pppppppppppppppppppppppppppppppp \n\n")
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(workingJsonObj)


#-------------------------------------------------------------------------
user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]


#Declaring the headers if forcing english is required. 
#headers = {"Accept-Language": "en-US,en;q=0.5"}

#declaring the list of empty variables, So that we can append the data overall
SiteTable = []
SiteNumbers = []
SiteNameLong = []
SiteNameShort = []
DisplayNames = []
SiteLocations = []
SiteFrequencies=[]
SiteDescriptions = []

# creating an array of values and passing it in the url for dynamic webpages
# range from 1 to 1000 counting by 100

RadioZoneHttp = 'https://www.radioreference.com/db/sid/2560'
RadioFileName = 'BellZone2Sites'


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

    SiteTable = aSite.find('table', class_='table table-sm table-responsive table-bordered')
    #print ("siteTable = ", siteTable, "\n\n")

    # this is a list of td-'data-txt fit' objects.
    manySiteNums = SiteTable.findAll('td', class_='data-text fit')
    #print ("manySiteNums = ", manySiteNums, "\n\n")

    for aSite in manySiteNums:
        #print ("------\n\taSite = ", aSite)
        #print ("\taSite.text = ", aSite.text, "\n")
        SiteNumbers.append(aSite.text)


    manyNames = SiteTable.find_all('td', style='width: 100%', class_=None)
    #print (manyNames)

    for aName in manyNames:
        #print ("-----\n\taName = ", aName)
        #print ("\taName.text = ", aName.text)
        longDisplayName = aName.text.split('(')[0] # long display name is left of (blah)
        #print ("long Display", longDisplay)
        SiteNameLong.append(longDisplayName)

        shortDispName = aName.text.split('(')[1].split(')')[0]  # display name is inside (blah)
        SiteNameShort.append(shortDispName)
        #print ("short Display Name", shortDispName)

    manyLocations = SiteTable.find_all('td', style='width: 100%', class_='noWrapTd')
    #print (manyLocations)

    for aLocation in manyLocations:
        #print ("-----\n\taName = ", aLocation)
        #print ("\taName.text = ", aLocation.text)
        SiteLocations.append(aLocation.text)


    #creating a dataframe 
    site2List = pd.DataFrame({ "SiteNum": SiteNumbers, "Long Name" : SiteNameLong, "Short Name" : SiteNameShort, "Location": SiteLocations } )

    # if this is ever printed, print only first and last 5 entries
    site2List.head(5)

    # this makes the console display the table.
    # It is required for python3 but not for python2
    print (site2List)   
    

    # #saving the data in excel format
    site2List.to_excel(RadioFileName + str(".xlsx"))

    #If you want to save the data in csv format
    site2List.to_csv(RadioFileName + str(".csv"))

except Exception as e:
    print (e)

# ======================= get frequencies ==============================================

try:
    manyChannels = SiteTable.findAll('td', class_='data-text')
    manyControls = SiteTable.findAll('td', class_='data-text ctrl-pri')

    # the name of the site has no class, other entities with style tag do.
    manyNames = SiteTable.findAll('td', style='width: 100%', class_=None)
    #print (manyNames)

    #for aName in manyNames:
    #    theName = aName.a.text
    #    print ("Site name = ", theName)
       

    voiceChans=''
    controlChans=''
    siteIndex = 0

    print( 'ssss = ', manyChannels[1].text)
    for channel in manyChannels:

        aChannel = channel.text

        if aChannel.find('c') != -1 :
            print ("CONTROL = ", aChannel)
            aChannel = aChannel[:-1]  # remove the 'c'
            controlChans = controlChans + str(aChannel) + ','

        elif aChannel.find('(') != -1 :

            # detected start of a  new site, barf out current site channels
            print(" ")

            controlChans = controlChans[:-1]    # remove tailing comma
            voiceChans = voiceChans[:-1]        # remove tailing comma
            print (SiteNumbers[siteIndex])
            siteIndex = siteIndex + 1
        

            print ( controlChans)
            print ( voiceChans)

            print("\n====================")

            print ("SITE = ", aChannel)
            voiceChans = ''
            controlChans = ''
        
        else:
            voiceChans = voiceChans + str(aChannel) + ','
            print (aChannel)


    # no more frequencies left, dump the guts of the last site
    controlChans = controlChans[:-1]    # remove tailing comma
    voiceChans = voiceChans[:-1]        # remove tailing comma


    print ( controlChans)
    print ( voiceChans)

    setupDefaultJason()
    printWorkingJson()
    testModifyJson()
    printWorkingJson()

    print ("-----------------------------------\n")
    
    print ("SiteNumber =", len(SiteNumbers), "Long Name = ", len(SiteNameLong),"Short Name = ", len(SiteNameShort), "Site Locations = ", len (SiteLocations))
 

except Exception as e:
    print (e)
