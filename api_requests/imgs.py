from PIL import Image, ImageStat

icon_mapping = {
        1: 'weather-sunny',
        2: 'weather-partly-cloudy',
        3: 'weather-partly-cloudy',
        4: 'weather-partly-cloudy',
        5: 'weather-partly-cloudy',
        6: 'weather-cloudy',
        7: 'weather-cloudy',
        8: 'weather-cloudy',
        11: 'weather-fog',
        12: 'weather-pouring',
        13: 'weather-rainy',
        14: 'weather-rainy',
        15: 'weather-lightning-rainy',
        16: 'weather-lightning-rainy',
        17: 'weather-lightning-rainy',
        18: 'weather-pouring',
        19: 'weather-snowy-heavy',
        20: 'weather-snowy-heavy',
        21: 'weather-partly-snowy',
        22: 'weather-snowy',
        23: 'weather-snowy',
        24: 'weather-snowy-heavy',
        25: 'weather-hail',
        26: 'weather-snowy-rainy',
        29: 'weather-snowy-rainy',
        30: 'thermometer-high',
        31: 'thermometer-low',
        32: 'weather-windy',
        33: 'weather-night',
        34: 'weather-night',
        35: 'weather-night-partly-cloudy',
        36: 'weather-night-partly-cloudy',
        37: 'weather-night-partly-cloudy',
        38: 'weather-cloudy',
        39: 'weather-pouring',
        40: 'weather-pouring',
        41: 'weather-lightning-rainy',
        42: 'weather-lightning-rainy',
        43: 'weather-snowy-heavy',
        44: 'weather-snowy'
    }


def get_proper_background():
    pass


def get_colour_theme(path):
    img = Image.open(path)
    mean_col = ImageStat.Stat(img).mean
    grey = [0.5, 0.5, 0.5, 0.5]
    colour = [round((mean_col[i]/255 - grey[i])/2) for i in range(4)]
    print(colour)
    return colour
