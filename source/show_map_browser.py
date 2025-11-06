import webbrowser
from geolocator import get_coordinates  # твой модуль

place = "Cambridge"
coords_list = get_coordinates(place)

if coords_list:
    lat, lon = coords_list[0]["latitude"], coords_list[0]["longitude"]
    # Ссылка с маркером
    url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    webbrowser.open(url)
else:
    print(f"Место {place} не найдено")
