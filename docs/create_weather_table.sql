DROP TABLE weather_data;
CREATE TABLE weather_data (
	city_name	varchar(50),
	city_id		int,
	country_name varchar(50),
	country_code varchar(2),
	weather_code int,
	ref_time	timestamp,
	sunset_time	timestamp,
	sunrise_time timestamp,
	cloud_per	int,
	rain_1h		numeric,
	snow_1h		numeric,
	w_ms		numeric,
	w_deg		int,
	humid_per	int,
	press_hpa	int,
	temperature	numeric,
	status	varchar(20),
	d_status varchar(20)
)