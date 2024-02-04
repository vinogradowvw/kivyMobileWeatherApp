from datetime import datetime
import requests
from .imgs import icon_mapping


def current_weather(config):
    print(config.get('main_config', 'apikey'))
    print(config.get('main_config', 'location_key'))
    params = {
        'apikey': config.get('main_config', 'apikey'),
        'language': config.get('main_config', 'language'),
        'details': 'true',
        'metric': 'true'
    }

    response = requests.get(
        'http://dataservice.accuweather.com/currentconditions/v1/' + config.get('main_config', 'location_key'),
        params=params
    )
    if response.status_code == 200:
        response = response.json()
    else:
        print('Error:', response.status_code)
        print(response)

    current_conditions = {
        'WeatherText': response[0]['WeatherText'] + ', ' + response[0]['RealFeelTemperature']['Metric']['Phrase'],
        'WeatherIcon': response[0]['WeatherIcon'],
        'IsDayTime': response[0]['IsDayTime'],
        'Temperature': str(response[0]['Temperature']['Metric']['Value']),
        'RealFeelTemperature': str(response[0]['RealFeelTemperature']['Metric']['Value']),
        'RelativeHumidity': str(response[0]['RelativeHumidity']),
        'Wind': (str(response[0]['Wind']['Speed']['Metric']['Value']), response[0]['Wind']['Direction']['Localized']),
        'Pressure': str(response[0]['Pressure']['Metric']['Value'])
    }

    return current_conditions


def hour12_forecast(config):
    params = {
        'apikey': config.get('main_config', 'apikey'),
        'language': config.get('main_config', 'language'),
        'details': 'true',
        'metrics': 'true'
    }

    response = requests.get(
        'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' + config.get('main_config', 'location_key'),
        params=params
    )
    if response.status_code == 200:
        response = response.json()
    else:
        print('Error:', response.status_code)
        print(response)

    temp = []
    precipitation = []
    wind = []
    humid = []
    uvindex = []
    timestamps = []
    icons = []

    for i in range(len(response)):
        uvindex.append(response[i]['UVIndex'])
        temp.append((response[i]['Temperature']['Value'] - 32) * 5 / 9)
        precipitation.append(response[i]['PrecipitationProbability'])
        wind.append(response[i]['Wind']['Speed']['Value'] * 1.609)
        humid.append(response[i]['RelativeHumidity'])
        datetime_object = datetime.fromisoformat(response[i]['DateTime'])
        timestamps.append(datetime_object.hour)
        icons.append(icon_mapping[response[i]['WeatherIcon']])

    return dict(temperature=temp, precipitation=precipitation, wind=wind, humid=humid, uvindex=uvindex,
                timestamps=timestamps, icons=icons)


def day5_forecast(config):

    params = {
        'apikey': config.get('main_config', 'apikey'),
        'language': config.get('main_config', 'language'),
        'details': 'true',
        'metrics': 'true'
    }

    response = requests.get(
        'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + config.get('main_config', 'location_key'),
        params=params
    )
    if response.status_code == 200:
        response = response.json()

    else:
        print('Error:', response.status_code)
        print(response)

    forecast_table_rows = []
    for i in range(5):
        print(response['DailyForecasts'][i])
        date_object = datetime.strptime(response['DailyForecasts'][i]['Date'], "%Y-%m-%dT%H:%M:%S%z")
        day_of_week = date_object.strftime("%A")

        forecast_table_rows.append(
            (
                day_of_week,
                [icon_mapping[response['DailyForecasts'][i]['Day']['Icon']], (0, 0, 0, 1), ''],
                response['DailyForecasts'][i]['Day']['ShortPhrase'],
                '{}°C'.format(response['DailyForecasts'][i]['Temperature']['Minimum']['Value']),
                '{}°C'.format(response['DailyForecasts'][i]['Temperature']['Maximum']['Value']),
                '{}%'.format(response['DailyForecasts'][i]['Day']['PrecipitationProbability'])
            )
        )

    return forecast_table_rows
