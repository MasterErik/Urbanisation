from geopy.geocoders import Nominatim

# Создаем объект геокодера один раз
geocoder = Nominatim(user_agent="rse-course")

def get_coordinates(place_name):
    """
    Возвращает список координат для переданного названия места.
    """
    location_list = geocoder.geocode(place_name, exactly_one=False)
    if not location_list:
        return []
    # Составляем список координат (широта, долгота)
    return [(loc.latitude, loc.longitude) for loc in location_list]

# Пример использования при запуске напрямую
if __name__ == "__main__":
    place = "Tallinn"
    coords = get_coordinates(place)
    print(f"Координаты для {place}: {coords}")
