from configparser import ConfigParser
import os

def config(filename='C:/Users/Malcolm/Weather/WeatherDashboard/WeatherApp/config.ini'):
    # create a parser
    cfg = ConfigParser()
    #create dict for params
    config = {}
    # read config file
    if os.path.exists(filename):
        cfg.read(filename)

        # write api_key
        config['api_key'] = cfg.get('keys','api_key')

        # write sql params
        config['host'] = cfg.get('postgresql','host')
        config['database'] = cfg.get('postgresql','database')
        config['user'] = cfg.get('postgresql','user')
        config['password'] = cfg.get('postgresql','password')
    else:
        raise FileNotFoundError('config.ini not found')

    # get api key, add to dict
    return config