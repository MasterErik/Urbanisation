import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
print("Используемый ключ:", API_KEY)

# Проверим, что ключ загружен
if not API_KEY:
    raise ValueError("❌ Не найден ключ GOOGLE_API_KEY в .env файле!")

# Инициализация клиента Google Maps
gmaps = googlemaps.Client(key=API_KEY)

# -------------------------------
# 1. Геокодирование (адрес → координаты)
# -------------------------------
def get_coordinates(address: str):
    result = gmaps.geocode(address)
    if result:
        location = result[0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]
        print(f"📍 Адрес: {address}")
        print(f"Координаты: широта={lat}, долгота={lng}")
        return lat, lng
    else:
        print("❌ Координаты не найдены")
        return None


# -------------------------------
# 2. Обратное геокодирование (координаты → адрес)
# -------------------------------
def get_address(lat: float, lng: float):
    result = gmaps.reverse_geocode((lat, lng))
    if result:
        address = result[0]["formatted_address"]
        print(f"🌍 Координаты: {lat}, {lng}")
        print(f"Адрес: {address}")
        return address
    else:
        print("❌ Адрес не найден")
        return None


# -------------------------------
# Пример использования
# -------------------------------
if __name__ == "__main__":
    # Пример 1 — из адреса в координаты
    coords = get_coordinates("Красная площадь, Москва")

    # Пример 2 — из координат в адрес
    if coords:
        lat, lng = coords
        get_address(lat, lng)