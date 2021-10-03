"""
Extracting a table of names and capitals from a website, cleaning and replacing mispelled or alternate values and output in a csv
"""

import pandas as pd

# load dataframe of countries, capitals, regions, etc
country_df = pd.read_html('http://techslides.com/list-of-countries-and-capitals')[0]
country_df.rename(columns=country_df.iloc[0], inplace=True) # set top row as column headers
country_df.drop(index=0, inplace=True) # drop top row that had the columns

# update data column headers
columns = country_df.columns.to_list()
new_columns = [col.lower().replace(" ", "_") for col in columns]
country_df.columns = new_columns

# drop countries with null values
country_df.dropna(how='any', inplace=True)

# Several of the strings pulled from the website need to be replaced or dropped as the OpenWeather database
# either does not have data on the specific city or spelled differently in their API
country_df['capital_name'].replace('Brasilia', 'Brasília', inplace=True, regex=False)
country_df.drop(country_df[country_df['capital_name'] == 'Diego Garcia'].index, inplace=True)
country_df['capital_name'].replace('Yaounde', 'Yaoundé', inplace=True, regex=False)
country_df['capital_name'].replace('N’Djamena', "N'Djamena", inplace=True, regex=False)
country_df['capital_name'].replace('The Settlement', "Flying Fish Cove", inplace=True, regex=False)
country_df['capital_name'].replace('Bogota', 'Bogotá', inplace=True, regex=False)
country_df['capital_name'].replace('Torshavn', 'Tórshavn', inplace=True, regex=False)
country_df['country_name'].replace('CuraÃ§ao', 'Curaçao', inplace=True, regex=False)
country_df['capital_name'].replace('Port-aux-FranÃ§ais', 'Port-aux-Français', inplace=True, regex=False)
country_df['capital_name'].replace("Saint George’s", "Saint George's", inplace=True, regex=False)
country_df['capital_name'].replace('Astana', 'Nur-Sultan', inplace=True, regex=False)
country_df['country_code'].replace('KO', 'XK', inplace=True, regex=False)
country_df['capital_name'].replace('Rangoon', 'Yangon', inplace=True, regex=False)
country_df['capital_name'].replace('Noumea', 'Nouméa', inplace=True, regex=False)
country_df['capital_name'].replace('Panama City', 'Panamá', inplace=True, regex=False)
country_df['capital_name'].replace('Asuncion', 'Asunción', inplace=True, regex=False)
country_df.drop(country_df[country_df['capital_name'] == 'King Edward Point'].index, inplace=True)
country_df.drop(country_df[country_df['country_name'] == 'US Minor Outlying Islands'].index, inplace=True)
country_df['country_code'].replace('US', 'DC', inplace=True, regex=False) # openweather uses state codes for country codes for US cities
country_df['capital_name'].replace('Hanoi', 'Ha Noi', inplace=True, regex=False)
country_df['capital_name'].replace('El-AaiÃºn', 'Laayoune', inplace=True, regex=False)
country_df['capital_name'].replace('Lome', 'Lomé', inplace=True, regex=False)
country_df['capital_name'].replace('Grand Turk', 'Cockburn Town', inplace=True, regex=False) # lol
country_df['capital_name'].replace('Nuku’alofa', "Nuku'alofa", inplace=True, regex=False)

# load to csv
country_df.to_csv('WeatherDashboard/data/countries-capitals.csv', index=False, encoding='utf-8-sig')