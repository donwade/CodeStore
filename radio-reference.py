from bs4 import BeautifulSoup
import requests, openpyxl
import random
user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

'''
excel = openpyxl.Workbook()
print(excel.sheetnames)             # print all current sheets available on start

sheet = excel.active                # if above has many sheet names, then pick one that has the focus
sheet.title = 'top rated movies'    # rename the sheet

#add some headers to the FIRST/TOP row. It is a list so use [string, string string ]
sheet.append(['Movie Rank','Movie Name','Year of Relese','IMDB Rating'])

# global comments in python (like c /* blah */)  is  ....   triple single quotes for start AND finish
'''


try:
    source = requests.get('https://www.radioreference.com/db/sid/2560', headers={'User-Agent': random.choice(user_agents_list)})

    source.raise_for_status()
    #print (source.text)  # big

    soup = BeautifulSoup(source.text, 'html.parser')
    #print (soup)
    
    #1) 'class' is a python reserved word, we get around that by using 'class_'
    #2) 'find_all - find all 'tr' objects under the 'tbody/lister-list' tag and make a LIST

    groupCount = 0

    for talkgroup in  soup.findAll('tbody', class_='data-text'):
        print (groupCount, "------------------------------")
        count = groupCount + 1
        #print (talkgroup)
        
        #1)  find tag td with class titleColumn, then find tag 'a' it has the name, convert to text
        decTG = talkgroup.find('td', class_='noWrapTd').text
        print ("decimal TG= ", decTG)


        next = talkgroup.find("td", id=False, class_=False).find_next_sibling('td')
        print ("hexTG = ", )

        type = talkgroup.find("td", id=False, class_=False).find_next_sibling('td').text
        print ("TYPE =" ,type)

        shortName = talkgroup.find("td", id=False, class_=False).find_next_sibling('td').find_next_sibling('td').text
        print ("SHORT NAME = ", shortName)

        longName = talkgroup.find("td", id=False, class_=False).find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').text
        print ("LONG NAME = ", longName)

        group = talkgroup.find("td", id=False, class_=False).find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').text
        print ("GROUP = ", group)

    

        # time to retrieve the rank. It is a piece of simple text inside the td-titleColumn
        # BUT asking for the text fo td-titleColumn will return ALL the text of ALL the sub-tags
        # within the td tag. We only want the first line of text, not all the sub tags text

        #name = movie.find('td', class_='titleColumn').text # 'text' returns all text and text of sub-tags YUK

        #instead put all the text from td-title column into one line, strip out all cr-lfs...
        #rank = movie.find('td', class_='titleColumn').get_text(strip=True)
        #print (rank)

        # looking a the big string of text, make a list with the 'cut delimiter' being a period
        #rank = movie.find('td', class_='titleColumn').get_text(strip=True).split('.')
        
        # we only want the first item in our list of strings... use indexing
        #rank = talkgroup.find('td', class_='titleColumn').get_text(strip=True).split('.')[0]
        #print (rank)

        # get the year
        # this time, don't use find('span') for the span tag, just use span directly, it will make it a tagname
        # Get the 'text' of the tag but the tag name has paranthesis, remove () chars.
        #year = talkgroup.find('td', class_='titleColumn').span.text.strip('()')
        #print (year)

        # get the rating. the use the tag name td again, BUT its a different class name.
        #rating = talkgroup.find('td', class_='ratingColumn imdbRating').strong.text
        #print (rating)

        #print (rank, name, year, rating )
        #sheet.append([rank, name, year, rating])
        #break      #if print only one entry is needed (aka testing)
            
        
 
except Exception as e:
    print (e)

#  '''
 
#excel.save('IMDB_movie_ratings.xlsx')
