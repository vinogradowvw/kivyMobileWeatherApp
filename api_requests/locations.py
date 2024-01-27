import requests


def location_suggestions(input, config):
    if not input:
        return dict(zip([], []))

    params = {
        'q': input,
        'apikey': config.get('main_config', 'apikey'),
        'language': config.get('main_config', 'language')
    }

    response = requests.get('http://dataservice.accuweather.com/locations/v1/cities/autocomplete',
                            params=params)
    if response.status_code == 200:
        response = response.json()
    else:
        print('Failed to get prediction:', response.status_code)

    suggestions = []
    keys = []

    for loc in response:
        suggestions.append(loc['LocalizedName'])
        keys.append(loc['Key'])

    return dict(zip(suggestions, keys))
