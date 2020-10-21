import requests
#import json
#import datetime
#import time

from influxdb import InfluxDBClient

####Refresh token
url_token = "https://accounts.zoho.com/oauth/v2/token?client_id=1000.YQMJ00QKSDL62MGUGZR96JQIR0QYYO&client_secret=63658d6427ae6a316ff4f90adc16efaf5d334b4885&refresh_token=1000.cb8ceab5b9bb1c8705c0abbf3e593651.851d90e25bcc81dcdaf6fca1b09a440e&grant_type=refresh_token"

payload_token = {}
headers_token = {
}

response_token = (requests.request("POST", url_token, headers=headers_token, data=payload_token)).json()

access_token = (response_token['access_token'])

####Current Status

url_cs = "https://www.site24x7.com/api/current_status?locations_required=true&group_required=false"

payload_cs = {}
headers_cs = {
    'Authorization': 'Zoho-oauthtoken ' + access_token
}

response_cs = (requests.request("GET", url_cs, headers=headers_cs, data=payload_cs)).json()
points_list = []
akv_resptime = str('response_time')

for d in (((response_cs['data'])['monitors'])):
    try:
        attribute_key_key = (d['attribute_key'])
        if attribute_key_key == akv_resptime:
            name_key_key = (d['name'])
            e = (d['locations'])
            for f in e:
                time_offset = int(((f['last_polled_time'])[-3:-2]))
                time_str = ((f['last_polled_time'])[:-5]) + '-0400'
                point = {"measurement": 'site_status',
                         "tags": {
                             "website": name_key_key,
                             "location": (f['location_name'])
                         },
                         "time": time_str,
                         "fields": {
                             "status": (f['status']),
                             "response_time": int((f['attribute_value']))
                         }
                         }
                points_list.append(point)
        else:
            pass
    except:
        pass

###Influx connection
InfluxClient = InfluxDBClient(host='192.168.161.181', port=8086, database='site24x7_status_1')

#InfluxClient.write_points(points_list)
print(points_list)


###testing save####
