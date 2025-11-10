import os
from pathlib import Path
from PIL import Image
from staticmap3 import StaticMap, CircleMarker


# ===============================
# 1. Класс генератора карт
# ===============================
class StaticMapGenerator:
    """Генератор статических карт с использованием staticmap3."""

    def __init__(self, width=400, height=300, zoom=12):
        self.width = width
        self.height = height
        self.zoom = zoom

    def get_map_image(self, coordinates):
        """Возвращает объект PIL.Image с картой и маркером."""
        lat, lng = coordinates
        m = StaticMap(self.width, self.height)
        marker = CircleMarker((lng, lat), 'red', 12)
        m.add_marker(marker)
        return m.render()

    def save_map(self, coordinates, filename="map.png"):
        """Сохраняет карту в файл PNG."""
        img = self.get_map_image(coordinates)
        img.save(filename)
        return filename


# ===============================
# 2. Словарь адресов
# ===============================
sample_addresses = {
    "Красная площадь, Москва": (55.7540471, 37.620405),
    "Tallinn": (59.437, 24.7536)
}

# Создаём словарь для обратного геокодирования: координаты → адрес
coords_to_address = {v: k for k, v in sample_addresses.items()}

# ===============================
# 3. Основной блок
# ===============================
if __name__ == "__main__":
    generator = StaticMapGenerator(width=400, height=300, zoom=14)

    for address, coords in sample_addresses.items():
        lat, lng = coords

        # Адрес → координаты
        print("\n📍 Адрес:", address)
        print(f"Координаты по адресу: широта={lat}, долгота={lng}")

        # Координаты → адрес (обратное геокодирование)
        addr_from_coords = coords_to_address.get(coords, "Адрес не найден")
        print(f"Адрес по координатам: {addr_from_coords}")

        # Генерация карты
        filename = f"{address.replace(',', '').replace(' ', '_')}.png"
        generator.save_map(coords, filename)
        print(f"🗺️ Карта сохранена: {filename}")