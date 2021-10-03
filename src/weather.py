from pyowm.owm import OWM
from pyowm.commons import exceptions
import psycopg2 as pg
import time
import pandas as pd
from weatherclasses import Country, City, Weather
import os
import pickle # for testing without api pulls
from config import config

# get login dictionary and load login info
login = config() 
API_KEY = login['api_key']
HOST = login['host']
DATABASE = login['database']
USER = login['user']
PASSWORD = login['password']

# construct pyowm objects
owm = OWM(API_KEY)
mgr = owm.weather_manager() # object to pull weather data
reg = owm.city_id_registry() # object to pull city data

# load csv
country_df = pd.read_csv('WeatherDashboard/data/countries-capitals.csv')

# get names of countries
country_names = country_df['country_name']

# load pickle object with country and city objects
countries = []
cities = []
objects = None
if os.path.exists('C:/Users/Malcolm/Weather/WeatherDashboard/data/objects.pkl'):
    with open('C:/Users/Malcolm/Weather/WeatherDashboard/data/objects.pkl', 'rb') as handle:
        objects = pickle.load(handle)
    countries = objects[0]
    cities = objects[1]
else:
    # create country objects
    for name in country_names:
        cont = country_df.loc[country_df['country_name'] == name, 'continent_name'].iloc[0]
        code = country_df.loc[country_df['country_name'] == name, 'country_code'].iloc[0]
        countries.append(Country(name, code, cont))
    # create city objects
    for country in countries:
        name = country_df.loc[country_df['country_name'] == str(country), 'capital_name'].iloc[0]
        code = country_df.loc[country_df['country_name'] == str(country), 'country_code'].iloc[0]
        try:
            city_id = reg.ids_for(name, country=code, matching='like')[0][0]
        except IndexError:
            print((name, code, str(country)))
        lat = country_df.loc[country_df['country_name'] == str(country), 'capital_latitude'].iloc[0]
        lon = country_df.loc[country_df['country_name'] == str(country), 'capital_longitude'].iloc[0]
        cities.append(City(name, country, lat, lon, city_id))
    objects = (countries, cities)
    # dump pickle
    with open('C:/Users/Malcolm/Weather/WeatherDashboard/data/objects.pkl', 'wb') as handle:
        pickle.dump(objects, handle, protocol=pickle.HIGHEST_PROTOCOL)

# create weather objects
weathers = []
for city in cities:
    weatherobj = Weather(city)
    try:
        observation = mgr.weather_at_id(city.city_id)
        weather = observation.weather
    except exceptions.TimeoutError:
        time.sleep(60) # OpenWeatherAPI limits us to 60 calls/min. When a timeout error occurs, the function waits 60 secs and tries again
        observation = mgr.weather_at_id(city.city_id)
        weather = observation.weather

    weatherobj.weather_code = weather.weather_code
    weatherobj.ref_time = weather.reference_time('iso')
    weatherobj.sunset_time = weather.sunset_time('iso')
    weatherobj.sunrise_time = weather.sunrise_time('iso')
    weatherobj.cloud_per = weather.clouds
    if '1h' in weather.rain.keys():
        weatherobj.rain_1h = weather.rain['1h']
    else:
        weatherobj.rain_1h = 0
    if '1h' in weather.snow.keys():
        weatherobj.snow_1h = weather.snow['1h']
    else:
        weatherobj.snow_1h = 0
    weatherobj.w_ms = weather.wind()['speed']
    weatherobj.humid_per = weather.humidity
    weatherobj.press_hpa = weather.barometric_pressure()['press']
    weatherobj.temperature = weather.temperature('celsius')['temp']
    weatherobj.status = weather.status
    weatherobj.d_status = weather.detailed_status
    weathers.append(weatherobj)

# connect to weather database
conn = pg.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

# insert all weather data collected into the sql table
cur = conn.cursor() # create new cursor method

# sql query to insert an individual city into the postgres database
sql_query = """INSERT INTO 
weather_data("city_name","city_id","country_name","country_code","weather_code","ref_time","sunset_time","sunrise_time","cloud_per","rain_1h","snow_1h","w_ms",
"humid_per","press_hpa","temperature","status","d_status")
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

for obj in weathers:
    cur.execute(sql_query, obj.to_tuple())  # TODO: increase the length of all the tables
# commit sql transactions
conn.commit()

# close cursor
cur.close()

#close connection
conn.close()