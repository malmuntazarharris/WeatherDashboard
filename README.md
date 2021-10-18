# Current World Weather Dashboard: Project Overview 
* Scraped a list of countries, capitals, continents and their coordinate locations
* Cleaned the data from the scraped website and replaced incorrect/mispelled values
* Created classes in Python to represent cities, countries and weather for the city
* Pulled weather data using OpenWeather.org API
* Stored weather data in PostgresSQL database
* Set a windows task to run python script daily
* Displayed data in PowerBI

## Code and Resources Used 
**Python Version:** Python 3.9.7
**Packages:** pandas, numpy, pickle, beautifulsoup, psycopg2, pyowm (OpenWeatherAPI python wrapper)
**Capital, Country, Continent and Coordinate Data:** http://techslides.com/list-of-countries-and-capitals

## Web Scraping
Developed a pandas web scraper to scrape country data from the list collected here: http://techslides.com/list-of-countries-and-capitals
With each country, we got the following:
* Country Name
* Capital Name
* Capital Latitude
* Capital Longitude
* Country Code
* Continent Name

## Data Cleaning
After scraping the data, I needed to clean it up so it'd be usable in a dashboard and to maintain consistency with the OpenWeatherAPI. I made the following changes:
* Replaced spellings of capitals with alternate spellings that the OpenWeatherAPI could recognize
* Fixed incorrect country codes, capital names, or country names
* Fixed mislabelled continents

## Class Creation
In order to better organize the data pulled from the API and to make the python files easier to update I created classes to hold city, country and weather data:
* Country - name, code, continent
* City - name, country, latitude, longitude, city id (for OpenWeather)
* Weather - city, country, weather code (code from OpenWeather representing weather status), reference time, sunset time, sunrise time, cloud percentage, rain within last hour, snow within last hour, wind speed, wind direction, humidity percentage, current temperature, max temperature, min temperature, feels like temperature, status, detailed status

## API Pull
I stored my API key in a config file that is pulled into a dictionary. From there, I created pyowm's weather manager and city id registry objects and loaded the country/city information from the csv I scraped.

The weather.py then creates the country and cities objects from the csv file. To save time, it pulls these objects from a pickle file as countries and capitals typically do not change.

The program then creates weather classes for each city by pulling from the API. This project was produced under the free tier of OpenWeather's API so in order to work around the 60 calls/min limit, I caught the timeout errors and paused the program for 60 secs.

## PostgresSQL Population
After pulling the database infomation from the config file, I connected to the PostgresSQL database using the psycopg2 module. The columns of the sql table contain the following:
* city_name
* city_id
* country_name
* country_code
* weather_code
* ref_time
* sunset_time
* sunrise_time
* cloud_per
* rain_1h
* snow_1h
* w_ms
* humid_per
* press_hpa
* temperature
* status
* d_status
* wind_dir
* max_temp
* min_temp
* feels_like

## Automation
Created a .bat file that contains the python file and weather.py and set a Windows task to run every day at 12:00 pm

## Dashboard Creation
Imported the SQL table and countries-capitals csv and created a dashboard. I also created two files with images of capitals and weather icons that could be pulled into the dashboard in the City Detail view.
![At A Glance](https://user-images.githubusercontent.com/29358953/137786552-aa9905d8-d548-408e-90e4-fa1e6afff7bb.png)
![City Detail](https://user-images.githubusercontent.com/29358953/137786556-9c9f9fc9-3002-4123-abef-174487025114.png)

