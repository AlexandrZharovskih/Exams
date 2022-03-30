import requests
import datetime


def timestamp_to_date(timestamp:str):
    return str(datetime.datetime.fromtimestamp(int(timestamp)).date())


def convert_millis(millis:int):
    millis *= 1000
    seconds = int(millis/1000%60)
    minutes = int(millis/(1000*60)%60)
    hours = int(millis/(1000*60*60)%24)
    return hours, minutes, seconds


api_url = 'https://api.openweathermap.org/data/2.5/onecall'
params = {
    'lat': '55.37',
    'lon': '37.92',
    'appid': '24d8742a4f9426ddeb257dc1cf883022',
    'exclude': 'alerts',
    'units': 'metric'
}
res = requests.get(api_url, params=params)
data = res.json()



the_same_temperature_day, temperature_diff, min_temperature_diff = '', 100, 100
for el in data['daily'][:5]:
    day = el['dt']
    temperature_diff = abs(el['temp']['night'] - el['feels_like']['night'])
    if temperature_diff < min_temperature_diff:
        the_same_temperature_day, min_temperature_diff = day, temperature_diff
print(f'Дата с самой маленькой разницей ночных температур: {timestamp_to_date(the_same_temperature_day)}.\n'
      f'Разница температур в этот день: {round(min_temperature_diff, 2)} градусов по Цельсию.')

print('-' * 70)


the_longest_day, daylight_hours, max_daylight_hours = '', 0, 0
for el in data['daily'][:5]:
    day = el['dt']
    daylight_hours = el['sunset'] - el['sunrise']
    if daylight_hours > max_daylight_hours:
        the_longest_day, max_daylight_hours = day, daylight_hours

hours, minutes, seconds = convert_millis(max_daylight_hours)
print(f'Дата с самым длинным световым днем в течение ближайших 5 дней: {timestamp_to_date(the_longest_day)}.\n'
      f'Продолжительность самого длинного светового дня: {hours} ч {minutes} мин {seconds} сек.')
