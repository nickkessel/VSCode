import requests

# station = input('\nChoose station (KILN,KIWX,KGRR, etc): ')
lat = 39
lon = 84
current = requests.get('https://api.weather.gov/stations/' + 'KILN' + '/observations')
forecast = requests.get('https://api.weather.gov/gridpoints/' + 'ILN/' + str(lat) + ',' + str(lon) + '/forecast')

c_json = current.json() #most recent hour observation from WFO
f_json = forecast.json() #2-a-day forecast for given lat/lon and WFO

def ctf(c_val): #converts celsius to fahrenheit, and returns as a STRING
    f_val = (c_val * 1.8) + 32
    return str(f_val)

time = c_json["features"][0]["properties"]['timestamp']
temp0 = ctf(c_json["features"][0]["properties"]['temperature']['value'])

for x in range(12):
    temp = f_json["properties"]['periods'][x]['temperature']
    day_desc = f_json['properties']['periods'][x]['name']
    
    print(day_desc + " temp " + str(temp))