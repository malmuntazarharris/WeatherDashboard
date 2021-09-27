DROP TABLE weather_data;
CREATE TABLE weather_data (
	city_name	varchar(50),
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
	sea_level	varchar(50),
	temperature	numeric,
	temp_min	numeric,
	temp_max	numeric,
	temp_feelslike	numeric,
	status	varchar(20),
	d_status varchar(20)
)