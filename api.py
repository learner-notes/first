from urllib.request import urlopen
import json
from datetime import datetime,timedelta


today=datetime.now()
tomorrow=today+timedelta(1)
today=today.date()
tomorrow=tomorrow.date()

response=urlopen("http://api.openweathermap.org/data/2.5/weather?zip=641008,IN&appid=710833e8507eaccc99e34ceaf6d24884")
data=json.loads(response.read())

cw={}
cw={"weather":data["weather"][0]["description"],"temp":data["main"]["temp"]-273.15,"humidity":data["main"]["humidity"],"wind_speed":data["wind"]["speed"]}
print(cw)

tw={}

tw_weather=[]
tw_temp=0
tw_humidity=0
tw_wind_speed=0

response=urlopen("http://api.openweathermap.org/data/2.5/forecast?zip=638002,IN&appid=710833e8507eaccc99e34ceaf6d24884")
data=json.loads(response.read())

for i in data['list']:
    iter=datetime.fromtimestamp(i['dt'])
    if iter.date()==today:
        continue
    elif iter.date()==tomorrow:

        tw_weather.append(i['weather'][0]["description"])
        tw_temp+=i["main"]["temp"]-273.15
        tw_humidity+=i["main"]["humidity"]
        tw_wind_speed+=i["wind"]["speed"]
        continue
    break

tw_weather_str=" & ".join(set(tw_weather))
tw={"weather":tw_weather_str,"temp":tw_temp/8,"humidity":tw_humidity/8,"wind_speed":tw_wind_speed/8}

print(tw)
