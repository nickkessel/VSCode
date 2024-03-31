import requests
from datetime import datetime
import pytz
from pytz import timezone

# station = input('\nChoose station (KILN,KIWX,KGRR, etc): ')
lat = 39
lon = 84
current = requests.get('https://api.weather.gov/stations/' + 'KILN' + '/observations')
forecast = requests.get('https://api.weather.gov/gridpoints/' + 'ILN/' + str(lat) + ',' + str(lon) + '/forecast')

utc_format = "%Y-%m-%d %H:%M:%S"

# Define UTC timezone
utc_timezone = pytz.utc

# Convert UTC time to Eastern Time (EDT)
eastern_timezone = pytz.timezone('America/New_York')

c_json = current.json() #most recent hour observation from WFO
f_json = forecast.json() #2-a-day forecast for given lat/lon and WFO

def ctf(c_val): #converts celsius to fahrenheit, and returns as a STRING
    f_val = (c_val * 1.8) + 32
    return str(f_val)


def utc_breakdown(utc_time_str):
    formatted_time = utc_time_str.replace("+00:00", "") #replace +00:00 with nothing
    formatted_time = formatted_time.replace("T", " ") #replace T with a space
    utc_time = datetime.strptime(formatted_time, utc_format)
    
    edt_time = utc_timezone.localize(utc_time).astimezone(eastern_timezone)

    # Format the EDT time as string
    edt_format = "%Y-%m-%d %H:%M:%S"
    edt_time_str = edt_time.strftime(edt_format)
    return(edt_time_str)


time = c_json["features"][0]["properties"]['timestamp']
c_temp = ctf(c_json["features"][0]["properties"]['temperature']['value']) #current temp

print('Latest Obs: (' + utc_breakdown(time) +') ' + c_temp + 'f \n')
for x in range(12):
    temp = f_json["properties"]['periods'][x]['temperature']
    when = f_json['properties']['periods'][x]['name']
    desc = f_json['properties']['periods'][x]['detailedForecast']
    
    print(when + " temp " + str(temp) + "  " + desc + '\n')