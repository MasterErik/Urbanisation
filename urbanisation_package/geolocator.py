from geopy.geocoders import Nominatim

geocoder = Nominatim(user_agent="rse-course")

def get_coordinates(place_name):
    try:
        location_list = geocoder.geocode(place_name, exactly_one=False, timeout=10)
        if not location_list:
            return []

        return [
            {
                'address': loc.address,
                'latitude': loc.latitude,
                'longitude': loc.longitude
            }
            for loc in location_list
        ]

    except Exception:
        return []