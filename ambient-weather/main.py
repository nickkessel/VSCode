from ambient_api.ambientapi import AmbientAPI
import time
from urllib3 import request
import urllib3

endpoint= 'https://api.ambientweather.net/v1'
api_key='47920d81820947199710d843bc624257328d689b65c74bcc81bc2b94b0f391c0'
app_key='3abc1d7d9a604ba6acea3b40bd836ac7078d323cc748473a8edf89eaa1d75d30'

http = urllib3.PoolManager()
#rq = request('https://rt.ambientweather.net/v1/devices?' + app_key + '=&' + api_key + '=')
rq = request('https://rt.ambientweather.net/v1/devices?3abc1d7d9a604ba6acea3b40bd836ac7078d323cc748473a8edf89eaa1d75d30=&47920d81820947199710d843bc624257328d689b65c74bcc81bc2b94b0f391c0=')

response_body = http.request('GET', 'https://rt.ambientweather.net/v1/devices?3abc1d7d9a604ba6acea3b40bd836ac7078d323cc748473a8edf89eaa1d75d30=&47920d81820947199710d843bc624257328d689b65c74bcc81bc2b94b0f391c0=')
print(response_body)
# api = AmbientAPI()
# devices = api.get_devices()
# device1 = devices[0]

# time.sleep(1)
# print(device1.get_data())