import pandas as pd
import numpy as np

def main():
    URL = 'https://en.wikipedia.org/wiki/List_of_national_capitals'

    capital_df = pd.read_html(URL)[1]

    # rename columns
    capital_df.rename(columns={'City/Town': 'Capital'}, inplace=True)

    # drop the notes
    capital_df.drop(columns='Notes', inplace=True)

    # some of the webscraped lists have '\n' and other footnotes in the country 
    capital_df.loc[capital_df['Country/Territory'].str.contains('\n').fillna(False), 'Country/Territory'] = np.nan
    capital_df['Country/Territory'].ffill(inplace=True)

    # remove all the text in parentheses and brackets
    capital_df['Country/Territory'] = capital_df['Country/Territory'].str.replace(r"\(.*\)", '', regex=True)
    capital_df['Capital'] = capital_df['Capital'].str.replace(r"\(.*\)", '', regex=True)
    capital_df['Country/Territory'] = capital_df['Country/Territory'].str.replace(r"\[.*?\]", '', regex=True)
    capital_df['Capital'] = capital_df['Capital'].str.replace(r"\[.*?\]", '', regex=True)

    # remove reverse single quotation marks
    capital_df['Capital'] = capital_df['Capital'].str.replace("ʻ", "'", regex=False)

    # remove the whitespaces in all strings of the dataframe
    capital_df_obj = capital_df.select_dtypes(['object'])
    capital_df[capital_df_obj.columns] = capital_df_obj.apply(lambda x: x.str.strip())

    # fix specific issue with capital of Palau: Ngerulmud does not have data in the openweather api, however the former capital Koror does
    capital_df["Capital"].replace('Ngerulmud', 'Koror', inplace=True, regex=False)

    # output an excel file of the dataframe
    capital_df.to_csv('C:/Users/Malcolm/Weather/WeatherDashboard/CountryCapitalList/countries_capitals.csv', index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()