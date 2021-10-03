"""This file are my attempts to scrape the country and capital details from multiple websites
These attempts ran into a series of issues mainly because due to the vague and political definition of what
exactly is a 'country' or a 'capital.' I've opted to pull from a singular source
for consistency: http://techslides.com/list-of-countries-and-capitals

The CSV's that were produced by this script are in the repository as:
- WeatherDashboard/data/cont_names.csv
- WeatherDashboard/data/alt_names.csv
- WeatherDashboard/data/country_codes.csv
- WeatherDashboard/data/capitals.csv
"""

import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
from urllib import request
import ssl


def remove_parens(df, columns):
    for col in columns:
        df[col] = df[col].str.replace(r"\(.*\)", '', regex=True) # remove '()'
        df[col] = df[col].str.replace(r"\[.*?\]", '', regex=True) # remove '[]'

def scrape_cont():
    continents = ('Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania')

    url = 'https://simple.wikipedia.org/wiki/List_of_countries_by_continents'

    html = requests.get(url).content 

    soup = BeautifulSoup(html, 'lxml')

    header2_list = soup.findAll('h2') # the tag <h2> contain all the continent names
    region_dict = {}

    for h2 in header2_list: 
        header_text = h2.text
        ol = h2.findNext('ol') # find the ordered list next to the header
        if ol != None: # only include in countries list if it has a result for a next ol
            countries = [li.text for li in ol.find_all('li')]
            region_dict[header_text] = countries

    # clean keys
    for old_key in list(region_dict.keys()):
        new_key = re.sub(r'\[.*?\]', '', old_key) # remove text in brackets
        region_dict[new_key] = region_dict.pop(old_key) # replace with new key
        if new_key not in continents: # remove any keys that isn't a continent
            del region_dict[new_key] 

    # clean values
    for value_list in list(region_dict.values()):
        for index, country in enumerate(value_list):
            country = country.split(' - ')[0] # split at hyphen
            country = re.sub(r'\[.*?\]', '', country) # remove brackets
            country = re.sub(r'\(.*?\)', '', country) # remove parentheses
            country = country.replace('*','').strip() # remove askterisk
            value_list[index] = country

    # create df and create csv 
    cont_df = pd.DataFrame([(continent, country) for (continent, l) in region_dict.items() for country in l], 
                 columns=['continent', 'country'])

    # replace empty strings with nan
    cont_df['country'].replace('', np.nan, inplace=True) 

    # replace certain values to match other dataframes
    cont_df['country'].replace("Côte d'Ivoire", 'Ivory Coast', inplace=True, regex=False)
    cont_df['country'].replace('The Gambia', 'Gambia', inplace=True, regex=False)
    cont_df['country'].replace('São Tomé and Príncipe', 'Sao Tome and Principe', inplace=True, regex=False)
    cont_df['country'].replace('Republic of Ireland', 'Ireland', inplace=True, regex=False)
    cont_df['country'].replace('North Macedonia', 'Macedonia', inplace=True, regex=False)
    cont_df['country'].replace('Vatican City', 'Vatican', inplace=True, regex=False)
    cont_df['country'].replace('US Virgin Islands', 'U.S. Virgin Islands', inplace=True, regex=False)
    cont_df['country'].replace('Federated States of Micronesia', 'Micronesia', inplace=True, regex=False)

    # drop nan and problem values
    cont_df.dropna(inplace=True)
    cont_df.drop(cont_df[cont_df['country'] == 'Russia Moscow'].index, inplace=True)
    cont_df.drop(cont_df[cont_df['country'] == 'Navassa Island'].index, inplace=True)
    cont_df.drop(cont_df[cont_df['country'] == 'French Guiana'].index, inplace=True)
    cont_df.drop(cont_df[cont_df['country'] == 'South Georgia and the South Sandwich Islands'].index, inplace=True)

    cont_df.to_csv('WeatherDashboard/data/cont_names.csv', index=False, encoding='utf-8-sig')

def scrape_alt_names():
    def list_replace(l):
        for x in range(len(l)):
            l[x] = l[x].replace(', ', '')
        return l

    def list_strip(l):
        for x in range(len(l)):
            l[x] = l[x].strip()
        return l

    url = 'https://en.wikipedia.org/wiki/List_of_alternative_country_names'

    # TODO: delete once testing is complete, replace with proper verified SSL context https://stackoverflow.com/questions/50969583/pandas-raises-ssl-certificateerror-when-using-method-read-html-for-https-resourc/50970844
    context = ssl._create_unverified_context()
    response = request.urlopen(url, context=context)
    html = response.read()

    alt_dfs = pd.read_html(html)
    
    # the wiki page has several tables that contain all the alternative names
    alt_df = pd.concat(alt_dfs)

    # replace columns
    alt_df.rename(columns={'Alpha-3 code':'alpha_3_code', 'Description':'common_name', 'Other name(s) or older name(s)':'other_names'}, inplace=True)

    # the cells have a string in this format "Name (type, language), Name (type, language), etc" so the below line splits removes the parenthesis and splits them at the parenthesis
    alt_df['other_names'] = alt_df['other_names'].str.split(r"\(.*?\)")

    # the items in the list contain an additional comma and  whitespace connected to each item. The below line cleans them
    alt_df['other_names'] = alt_df['other_names'].apply(list_replace)
    alt_df['other_names'] = alt_df['other_names'].apply(list_strip)

    # remove parentheses in common_name
    remove_parens(alt_df, ['common_name']) 

    alt_df.to_csv('WeatherDashboard/data/alt_names.csv', index=False, encoding='utf-8-sig')

def scrape_country_codes():
    url = 'https://countrycode.org/'

    # TODO: delete once testing is complete, replace with proper verified SSL context https://stackoverflow.com/questions/50969583/pandas-raises-ssl-certificateerror-when-using-method-read-html-for-https-resourc/50970844
    context = ssl._create_unverified_context()
    response = request.urlopen(url, context=context)
    html = response.read()

    code_df = pd.read_html(html)[0]

    # drop last two columns
    code_df.drop(columns=['AREA KM2', 'GDP $USD'], inplace=True)

    # rename columns
    code_df.rename(columns={'COUNTRY':'country', 'COUNTRY CODE':'num_code', 'ISO CODES':'alpha_code', 'POPULATION':'population'}, inplace=True)

    # split different country codes
    code_df[['alpha_2_code','alpha_3_code']] = code_df.alpha_code.str.split("/",expand=True)
    code_df.drop(columns='alpha_code', inplace=True)

    # clean whitespace
    code_df['alpha_2_code'] = code_df['alpha_2_code'].str.strip()
    code_df['alpha_3_code'] = code_df['alpha_3_code'].str.strip()

    # replace certain values
    code_df['country'].replace('United States', 'United States of America', inplace=True, regex=False)

    code_df.to_csv('WeatherDashboard/data/country_codes.csv', index=False, encoding='utf-8-sig')

def scrape_capitals():
    url = 'https://en.wikipedia.org/wiki/List_of_national_capitals'

    # TODO: delete once testing is complete, replace with proper verified SSL context https://stackoverflow.com/questions/50969583/pandas-raises-ssl-certificateerror-when-using-method-read-html-for-https-resourc/50970844
    context = ssl._create_unverified_context()
    response = request.urlopen(url, context=context)
    html = response.read()

    capital_df = pd.read_html(html)[1]

    # rename columns
    capital_df.rename(columns={'City/Town': 'capital', 'Country/Territory': 'country'}, inplace=True)

    # drop the notes
    capital_df.drop(columns='Notes', inplace=True)

    # remove all the text in parentheses and brackets
    remove_parens(capital_df, capital_df.columns)

    # remove reverse single quotation marks
    capital_df['capital'] = capital_df['capital'].str.replace("ʻ", "'", regex=False)

    # remove the whitespaces in all strings of the dataframe
    capital_df_obj = capital_df.select_dtypes(['object'])
    capital_df[capital_df_obj.columns] = capital_df_obj.apply(lambda x: x.str.strip())

    # replace capitals that do not have data on OpenWeather or are spelled differently
    capital_df['capital'].replace('Ngerulmud', 'Koror', inplace=True, regex=False)
    capital_df['capital'].replace("Sana'a", 'Sanaa', inplace=True, regex=False)

    # drop countries that are not in other dataframes
    capital_df.drop(capital_df[capital_df['capital'] == 'Adamstown'].index, inplace=True)
    capital_df.drop(capital_df[capital_df['country'] == 'Alofi'].index, inplace=True)

    # output an excel file of the dataframe
    capital_df.to_csv('WeatherDashboard/data/capitals.csv', index=False, encoding='utf-8-sig')

def main():
    scrape_cont()
    scrape_alt_names()
    scrape_country_codes()
    scrape_capitals()

if __name__ == "__main__":
    main()