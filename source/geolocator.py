from geopy.geocoders import Nominatim

geocoder = Nominatim(user_agent="rse-course")

def get_coordinates(place_name):
    """
    Возвращает список найденных мест с полной информацией.
    Каждый элемент — словарь:
    {
        'address': полный адрес,
        'latitude': широта,
        'longitude': долгота
    }
    """
    try:
        location_list = geocoder.geocode(place_name, exactly_one=False, timeout=10)
        if not location_list:
            return []

        results = []
        for loc in location_list:
            results.append({
                'address': loc.address,
                'latitude': loc.latitude,
                'longitude': loc.longitude
            })
        return results

    except Exception as e:
        print("Ошибка геокодирования:", e)
        return []

# Тестовый запуск
if __name__ == "__main__":
    place = "Tallinn"
    coords = get_coordinates(place)
    for loc in coords:
        print(loc)
