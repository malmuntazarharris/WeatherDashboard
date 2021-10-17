class Country:
    """
    A class to represent a Country.

    ...

    Attributes
    ----------
    name : str
        name of the country
    code : str
        the alpha 2 code for the country
    continent : str
        continent in which the country
    """
    def __init__(self, name, code, continent):
        self.name = name
        self.code = code
        self.continent = continent

    def __str__(self) -> str:
        return self.name

class City:
    """
    A class to represent a City.

    ...

    Attributes
    ----------
    name : str
        name of the city
    country : Country class
        the country that the city is located in
    lat: float
        the latitude coordinate
    long: float
        the longitude coordinate
    """
    def __init__(self, name, country, lat, lon, id):
        self.name = name
        self.country = country
        self.lat = lat
        self.lon = lon
        self.city_id = id

    def __str__(self) -> str:
        return self.name

class Weather:
    """
    A class to represent weather

    ...

    Attributes
    ----------
    city: City class
        city where the weather is
    country: Country class
        country where the weather is
    """
    def __init__(self, city):
        self.city = city
        self.country = city.country
        self.weather_code = None
        self.ref_time = None
        self.sunset_time = None
        self.sunrise_time = None
        self.cloud_per = None
        self.rain_1h = None
        self.snow_1h = None
        self.w_ms = None
        self.humid_per = None
        self.press_hpa = None
        self.temperature = None
        self.status = None
        self.d_status = None
        self.wind_dir = None
        self.max_temp = None
        self.min_temp = None
        self.feels_like = None

    def to_tuple(self):
        return (
            str(self.city.name),
            str(self.city.city_id),
            str(self.country.name),
            str(self.country.code),
            str(self.weather_code),
            str(self.ref_time),
            str(self.sunset_time),
            str(self.sunrise_time),
            str(self.cloud_per),
            str(self.rain_1h),
            str(self.snow_1h),
            str(self.w_ms),
            str(self.humid_per),
            str(self.press_hpa),
            str(self.temperature),
            str(self.status),
            str(self.d_status),
            str(self.wind_dir),
            str(self.max_temp),
            str(self.min_temp),
            str(self.feels_like),
        )