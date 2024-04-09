import requests
from datetime import datetime
import pytz
from pytz import timezone

# station = input('\nChoose station (KILN,KIWX,KGRR, etc): ')
lat = 39.167 #can replace these with any lat/lon
lon = -84.293

init_url = 'https://api.weather.gov/points/' + str(lat) + ',' + str(lon)
print(init_url)
init_call = requests.get(init_url)
i_json = init_call.json() # initial call to get the grid points for forecast data in certain WFO

current = requests.get('https://api.weather.gov/stations/' + 'KILN' + '/observations')

forecast_url = i_json['properties']['forecast']
print(forecast_url)
hourly_url = i_json['properties']['forecastHourly']
print(hourly_url)
alert_zone = i_json['properties']['forecastZone'] # returns omethings like 'https://api.weather.gov/zones/forecast/OHZ078'


forecast = requests.get(forecast_url)
forecast_hourly = requests.get(hourly_url)

utc_format = "%Y-%m-%d %H:%M:%S"

# Define UTC timezone
utc_timezone = pytz.utc

# Convert UTC time to Eastern Time (EDT)
eastern_timezone = pytz.timezone('America/New_York')

c_json = current.json() #most recent hour observation from WFO
f_json = forecast.json() #2-a-day forecast for given lat/lon and WFO
h_json = forecast_hourly.json()

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


def time_formatter(init_time_str, type):
    
    if type == 0: #format from utc time
        formatted_time = init_time_str.replace("+00:00", "") #replace +00:00 with nothing
        formatted_time = formatted_time.replace("T", " ") #replace T with a space
        utc_time = datetime.strptime(formatted_time, utc_format)
        
        edt_time = utc_timezone.localize(utc_time).astimezone(eastern_timezone)

        # Format the EDT time as string
        edt_format = "%Y-%m-%d %H:%M:%S"
        edt_time_str = edt_time.strftime(edt_format)
        return(edt_time_str)
    elif type == 1: #if time string is already in edt, then remove extra stuff, and remove the year and seconds at the end
        formatted_time = init_time_str.replace("-04:00", "") #replace +00:00 with nothing
        formatted_time = formatted_time.replace("T", " ") #replace T with a space
        formatted_time = formatted_time.replace("2024-", "") #replace T with a space
        formatted_time = formatted_time.replace(":00  ", " ") #replace T with a space

        return(formatted_time)


time = c_json["features"][0]["properties"]['timestamp']
c_cond = c_json["features"][0]["properties"]['textDescription'] #current conditions
c_wind = convert((c_json["features"][0]["properties"]['windSpeed']['value']), 'kmh') #current wind speed
c_dew = convert((c_json["features"][0]["properties"]['dewpoint']['value']), 'c')
# c_gust = convert((c_json["features"][0]["properties"]['windGust']['value']), 'kmh') #current wind gust (not working bc sometimes it is null and i dont want to fix it rn)
c_temp = convert((c_json["features"][0]["properties"]['temperature']['value']), 'c') #current temp
c_pressure = convert((c_json["features"][0]["properties"]['barometricPressure']['value']), 'pa') #current baro pressure


info_selector = input("Daily Forecast (d) | Hourly Forecast (h) | Active Alerts (a) : ")

print('\nLatest Obs: (' + time_formatter(time, 0) +') ' + c_cond + ' | ' +str(c_temp) + 'f | DP: '+ str(c_dew) + 'f | ' + str(c_wind) + 'mph | ' + str(c_pressure) + 'mb\n')

if info_selector == 'd':
    for x in range(14): #twelve day segments/ day and night
        temp = f_json["properties"]['periods'][x]['temperature']
        when = f_json['properties']['periods'][x]['name']
        desc = f_json['properties']['periods'][x]['detailedForecast']
        
        print(when + " temp " + str(temp) + "  " + desc + '\n')
elif info_selector == 'h':
    print('hourly')
    hourly_range = len(h_json['properties']['periods'])
    for x in range(hourly_range):
        h_starthour = time_formatter(h_json['properties']['periods'][x]['startTime'], 1)
        h_temp = h_json['properties']['periods'][x]['temperature']
        print(h_starthour + '  ' + str(h_temp))
    
elif info_selector == 'a':
    alert_zone = alert_zone.replace('https://api.weather.gov/zones/forecast/','') #replaces uneccsary part with nothing
    alerts_url = 'https://api.weather.gov/alerts/active?zone=' + alert_zone #appends zone code to the alert url
    print(alerts_url)   
    alerts = requests.get(alerts_url)
    a_json = alerts.json() #current alerts for given alert zone

    
    alert_count = len(a_json['features'])
    print('alert count: ' + str(alert_count))

    if alert_count != 0: #if there are alerts
        for x in range(alert_count): #cycle thru list of alerts
            alert_headline = (a_json['features'][x]['properties']['headline']) #alert headline, with issue date and expiry time
            alert_desc = (a_json['features'][x]['properties']['description']) #details about impacts, etc...
            print(alert_headline + '\n' + alert_desc + '\n')
else:
    print("ERROR!!!!!")