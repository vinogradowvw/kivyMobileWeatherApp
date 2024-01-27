import android

droid = android.Android()
result = droid.startLocating()
if result.error is None:
    location = droid.readLocation()
    if location.error is None:
        latitude = location.result['network']['latitude']
        longitude = location.result['network']['longitude']
        print(f"Широта: {latitude}, Долгота: {longitude}")
    else:
        print(f"Ошибка при получении местоположения: {location.error}")
else:
    print(f"Ошибка при начале слежения за местоположением: {result.error}")
