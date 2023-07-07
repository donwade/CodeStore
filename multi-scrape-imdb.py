# %%
"""
## Scraping Multiples pages of IMDB at a time to fetch top 1000 movies data.
"""

# %%
"""
_*If you have any doubts, you may reach me out on <b>hustlewithzidd@gmail.com<b>*_
"""

# %%
"""
_*<b>Edit: Added the Description part of Movie in the Dataframe (July-15-2021)<b>*_
"""

# %%
"""
_*<b>Kindly support me by subscribing my channel and <b>endorsing my skills in linkedIn : https://www.linkedin.com/in/sivasahukar95/<b>*_
"""

# %%
#importing the libraries needed 
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint

#Declaring the headers 
headers = {"Accept-Language": "en-US,en;q=0.5"}

#declaring the list of empty variables, So that we can append the data overall

movie_name = []
year = []
time=[]
rating=[]
metascore =[]
votes = []
gross = []
description = []

#creating an array of values and passing it in the url for dynamic webpages
pages = np.arange(1,1000,100)

#the whole core of the script
for page in pages:
    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(page)+"&ref_=adv_nxt")
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_data = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})
    sleep(randint(2,8))
    for store in movie_data:
        name = store.h3.a.text
        movie_name.append(name)
        
        year_of_release = store.h3.find('span', class_ = "lister-item-year text-muted unbold").text
        year.append(year_of_release)
        
        runtime = store.p.find("span", class_ = 'runtime').text
        time.append(runtime)
        
        rate = store.find('div', class_ = "inline-block ratings-imdb-rating").text.replace('\n', '')
        rating.append(rate)
        
        meta = store.find('span', class_ = "metascore").text if store.find('span', class_ = "metascore") else "****"
        metascore.append(meta)
        
        
        value = store.find_all('span', attrs = {'name': "nv"})
        
        vote = value[0].text
        votes.append(vote)
        
        grosses = value[1].text if len(value)>1 else '%^%^%^'
        gross.append(grosses)
        
        # Description of the Movies -- Not explained in the Video, But you will figure it out. 
        describe = store.find_all('p', class_ = 'text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) >1 else '*****'
        description.append(description_)
        
#creating a dataframe 
movie_list = pd.DataFrame({ "Movie Name": movie_name, "Year of Release" : year, "Watch Time": time,"Movie Rating": rating, "Meatscore of movie": metascore, "Votes" : votes, "Gross": gross, "Description": description  })



# %%
movie_list.head(5)

# %%
# #saving the data in excel format
movie_list.to_excel("Top 1000 IMDb movies.xlsx")

# #If you want to save the data in csv format
movie_list.to_csv("Top 1000 IMDb movies.csv")

# %%
