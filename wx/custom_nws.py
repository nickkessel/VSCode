import requests
from datetime import datetime
import pytz
from pytz import timezone

# station = input('\nChoose station (KILN,KIWX,KGRR, etc): ')
lat = 39.10 #can replace these with any lat/lon
lon = -84.1735
init_call = requests.get('https://api.weather.gov/points/' + str(lat) + ',' + str(lon)) 
current = requests.get('https://api.weather.gov/stations/' + 'KILN' + '/observations')

i_json = init_call.json()
forecast_url = i_json['properties']['forecast']
hourly_url = i_json['properties']['forecastHourly']
alert_zone = i_json['properties']['forecastZone']

alerts_url = requests.get('https://api.weather.gov/alerts/active?zone=' + alert_zone)
forecast = requests.get(forecast_url)
forecast_hourly = requests.get(hourly_url)
alerts = requests.get('https://api.weather.gov/alerts/active/area/OH')

utc_format = "%Y-%m-%d %H:%M:%S"

# Define UTC timezone
utc_timezone = pytz.utc

# Convert UTC time to Eastern Time (EDT)
eastern_timezone = pytz.timezone('America/New_York')

c_json = current.json() #most recent hour observation from WFO
f_json = forecast.json() #2-a-day forecast for given lat/lon and WFO
a_json = alerts.json() #current alerts for given state

print(a_json['features'][0]['properties']['event'])

def convert(val, type): #converts various metric values into imperial ones
    if type == 'c': #celsius to fahrentheit
        f_val = round((val * 1.8) + 32, 1)
        return(f_val)
    elif type == 'kmh': #kmh to mph
        mph_val = round((val / 1.609), 1)
        return(mph_val)
    elif type == 'pa': #converts pascals to mb/hpa
        hpa_val = round((val/100), 2)
        return(hpa_val)
    else:
        return('Oh no! conversion error...')


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
c_cond = c_json["features"][0]["properties"]['textDescription'] #current conditions
c_wind = convert((c_json["features"][0]["properties"]['windSpeed']['value']), 'kmh') #current wind speed
c_dew = convert((c_json["features"][0]["properties"]['dewpoint']['value']), 'c')
# c_gust = convert((c_json["features"][0]["properties"]['windGust']['value']), 'kmh') #current wind gust (not working bc sometimes it is null and i dont want to fix it rn)
c_temp = convert((c_json["features"][0]["properties"]['temperature']['value']), 'c') #current temp
c_pressure = convert((c_json["features"][0]["properties"]['barometricPressure']['value']), 'pa') #current baro pressure

daily_or_hourly = input("Daily Forecast (d) or Hourly Forecast (h)? : ")

print('Latest Obs: (' + utc_breakdown(time) +') ' + c_cond + ' | ' +str(c_temp) + 'f | DP: '+ str(c_dew) + 'f | ' + str(c_wind) + 'mph | ' + str(c_pressure) + 'mb\n')

if daily_or_hourly == 'd':
    for x in range(14): #twelve day segments/ day and night
        temp = f_json["properties"]['periods'][x]['temperature']
        when = f_json['properties']['periods'][x]['name']
        desc = f_json['properties']['periods'][x]['detailedForecast']
        
        print(when + " temp " + str(temp) + "  " + desc + '\n')
elif daily_or_hourly == 'h':
    print('hourly')
else:
    print("ERROR!!!!!")