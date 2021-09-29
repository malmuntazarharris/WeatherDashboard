from pyowm.owm import OWM
from pyowm.commons import exceptions
import openpyxl as xl
import psycopg2 as pg
import time
import datetime as dt
import pickle # for testing without api pulls
from config import config

# list of weather data needed
WEATHER_INFO = ('weather_code', 
                'reference_time',
                'sunset_time',
                'sunrise_time',
                'clouds',
                'rain',
                'snow',
                'wind',
                'humidity',
                'pressure',
                'temperature',
                'status',
                'detailed_status')

# get login dictionary and load login info
login = config()
API_KEY = login['api_key']
HOST = login['host']
DATABASE = login['database']
USER = login['user']
PASSWORD = login['password']

# get names of cities
ws = xl.load_workbook('C:/Users/Malcolm/Weather/WeatherDashboard/CountryCapitalList/countries_capitals.xlsx').active
first_column = ws['A'] # column with the capitals
capitals = [first_column[value].value for value in range(1, len(first_column))]

# construct weather manager
owm = OWM(API_KEY)
mgr = owm.weather_manager()

def get_weather_dict(city):
    """Returns the weather dictionary for a given city

    :param city: the name of the city
    :type city: str
    :returns: dictionary with weather information per OpenWeatherAPI
    """
    try:
        observation = mgr.weather_at_place(city)
        weather = observation.weather
        weather_dict = weather.to_dict()
        current_weathers[city] = weather_dict
    except exceptions.NotFoundError:
        # pass if city weather not found
        print(city)
        return {}
    except exceptions.TimeoutError:
        time.sleep(60) # OpenWeatherAPI limits us to 60 calls/min. When a timeout error occurs, the function waits 60 secs and tries again
        observation = mgr.weather_at_place(city)
        weather = observation.weather
        weather_dict = weather.to_dict()
    return weather_dict

# get weather dictionary for each capital and save pickle


current_weathers = {}
#f=open('p.pickle', 'wb')
#with open('C:/Users/Malcolm/Weather/WeatherDashboard/WeatherApp/p.pickle', 'rb') as f:
#    current_weathers = pickle.load(f)
for city in capitals:
    current_weathers[city] = get_weather_dict(city)

#pickle.dump(current_weathers, f)
#f.close()
# connect to weather database
conn = pg.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

# insert all weather data collected into the sql table
cur = conn.cursor() # create new cursor method

# sql query to insert an individual city into the postgres database
sql_query = """INSERT INTO 
weather_data("city_name","weather_code","ref_time","sunset_time","sunrise_time","cloud_per","rain_1h","snow_1h","w_ms","w_deg",\
"humid_per","press_hpa","sea_level","temperature","temp_min","temp_max","temp_feelslike","status","d_status")
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

for city in current_weathers.keys():
    if len(current_weathers[city]) == 0:
        pass
    weather_params = []
    weather_params.append(city)
    weather_dict = current_weathers[city]
    for item in WEATHER_INFO:
        try:
            if 'time' in item: # condition for time conversion from unix epoch time to iso format
                weather_params.append(dt.datetime.utcfromtimestamp(weather_dict[item]).isoformat())
            elif item == 'rain':
                weather_params.append(str(weather_dict[item]['1h']))
            elif item == 'snow':
                weather_params.append(str(weather_dict[item]['1h']))
            elif item == 'wind':
                weather_params.append(str(weather_dict[item]['speed']))
                weather_params.append(str(weather_dict[item]['deg']))
            elif item == 'pressure':
                weather_params.append(str(weather_dict[item]['press']))
                weather_params.append(str(weather_dict[item]['sea_level']))
            elif item == 'temperature':
                weather_params.append(str(weather_dict[item]['temp']))
                weather_params.append(str(weather_dict[item]['temp_min']))
                weather_params.append(str(weather_dict[item]['temp_max']))
                weather_params.append(str(weather_dict['temperature']['feels_like']))
            else:
                weather_params.append(str(weather_dict[item]))

        except KeyError:
            weather_params.append("0")
    cur.execute(sql_query, tuple(weather_params))
        
# commit sql transactions
conn.commit()

# close cursor
cur.close()

#close connection
conn.close()