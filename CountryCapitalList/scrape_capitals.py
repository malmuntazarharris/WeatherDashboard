import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


html = requests.get('https://en.wikipedia.org/wiki/List_of_national_capitals').content

soup = BeautifulSoup(html, 'lxml')

capitals_table = soup.findAll('table')[1]

capitals_rows = capitals_table.findAll('tr')
#TODO: refactor below block
sovereign_rows = []
two_capitals = False #bool to flag if a country has two capitals
for tr in capitals_rows:
    if len(tr.findAll('b')) > 0 or two_capitals == True: #only the bolded rows should be added, bolded capitals indicate that it's a sovereign state and/or recognized by the UN
            if two_capitals == True: 
                two_capitals = False  
            bolded_row = []
            if len(re.findall(r'rowspan="[0-255]"', str(tr))) > 0: #row span on this chart indicates that the
                two_capitals = True
            td = tr.find_all('td')
            for i in td:
                bolded_row.append(i.text)
            sovereign_rows.append(bolded_row)