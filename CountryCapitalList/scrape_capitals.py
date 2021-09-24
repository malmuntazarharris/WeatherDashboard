import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
<<<<<<< HEAD
import numpy as np
import openpyxl

CAPITAL_TABLE_INDEX = 1 #the second table on the wikipedia page contains the capitals

html = requests.get('https://en.wikipedia.org/wiki/List_of_national_capitals').content 

soup = BeautifulSoup(html, 'lxml')

capitals_table = soup.findAll('table')[CAPITAL_TABLE_INDEX]

capitals_rows = capitals_table.findAll('tr') #find all rows in the table

#TODO: refactor below block, maybe replace the bool with the row span regex check???
sovereign_rows = []
two_capitals = False #bool to flag if a country has two capitals
for tr in capitals_rows:
    #only the bolded rows should be added, bolded capitals indicate that it's a sovereign state and/or recognized by the UN
    #also if two_capitals are set to True that means that the row it's iterating is the second capital of a country
    if len(tr.findAll('b')) > 0 or two_capitals == True: 
        if two_capitals == True: 
            two_capitals = False  
        bolded_row = []
        if len(re.findall(r'rowspan="[0-255]"', str(tr))) > 0: #rowspans indicate that a country has two capitals (e.g. Malaysia), set two_capitals bool to true if row contains rowspan
            two_capitals = True
        td = tr.find_all('td')
        for i in td:
            bolded_row.append(i.text) #add each cell to a list
        sovereign_rows.append(bolded_row) #add list representing row to the rows of sovereign nations

#convert soveign_rows (list of lists) into dataframe
sovereign_df = pd.DataFrame(sovereign_rows, columns=['Capital', 'Country', 'Footnote'])

#drop the footnotes
sovereign_df = pd.DataFrame(sovereign_rows, columns=['Capital', 'Country', 'Footnote'])
sovereign_df.drop(columns='Footnote', inplace=True)

#some of the webscraped lists have '\n' and other footnotes in the country 
sovereign_df.loc[sovereign_df['Country'].str.contains('\n').fillna(False), 'Country'] = np.nan
sovereign_df['Country'].ffill(inplace=True)

#remove all the text in parentheses
sovereign_df['Country'] = sovereign_df['Country'].str.replace(r"\(.*\)","", regex=True)
sovereign_df['Capital'] = sovereign_df['Capital'].str.replace(r"\(.*\)","", regex=True)

#remove the whitespaces in all strings of the dataframe
sovereign_df_obj = sovereign_df.select_dtypes(['object'])
sovereign_df[sovereign_df_obj.columns] = sovereign_df_obj.apply(lambda x: x.str.strip())

#output an excel file of the dataframe
sovereign_df.to_excel('C:/Users/Malcolm/Weather/WeatherDashboard/CountryCapitalList/countries_capitals.xlsx', index=False)
=======


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
>>>>>>> main
