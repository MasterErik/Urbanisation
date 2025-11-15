from geopy.geocoders import Nominatim

geocoder = Nominatim(user_agent="rse-course")

def get_coordinates(place_name):
    try:
        location_list = geocoder.geocode(place_name, exactly_one=False, timeout=10)

        if not location_list:  # этого достаточно!
            print("Место не найдено.")
            sys.exit(1)

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
        sys.exit(1)
