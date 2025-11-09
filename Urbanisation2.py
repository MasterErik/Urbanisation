import os
from pathlib import Path
from PIL import Image
import unittest
from staticmap3 import StaticMap, CircleMarker

# ===============================
# 1. Класс StaticMapGenerator
# ===============================
class StaticMapGenerator:
    """
    Генератор статических карт с использованием staticmap3.
    """
    def __init__(self, width=400, height=300, zoom=12):
        self.width = width
        self.height = height
        self.zoom = zoom

    def get_map_image(self, coordinates):
        lat, lng = coordinates
        m = StaticMap(self.width, self.height)
        marker = CircleMarker((lng, lat), 'red', 12)
        m.add_marker(marker)
        return m.render()

    def save_map(self, coordinates, filename="map.png"):
        img = self.get_map_image(coordinates)
        img.save(filename)
        return filename

# ===============================
# 2. Словарь адресов
# ===============================
sample_addresses = {
    "Красная площадь, Москва": (55.7540471, 37.620405),
    "Таллин, Эстония": (59.437, 24.7536)
}

# ===============================
# 3. Основной блок
# ===============================
if __name__ == "__main__":
    generator = StaticMapGenerator(width=400, height=300, zoom=14)

    for address, coords in sample_addresses.items():
        lat, lng = coords
        print("\n📍 Адрес:", address)
        print(f"Координаты: широта={lat}, долгота={lng}")

        # Генерация карты
        filename = f"{address.replace(',', '').replace(' ', '_')}.png"
        generator.save_map(coords, filename)
        print(f"🗺️ Карта сохранена: {filename}")

# ===============================
# 4. Тесты для StaticMapGenerator
# ===============================
class TestStaticMapGenerator(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path("tmp_test_maps")
        self.tmp_dir.mkdir(exist_ok=True)
        self.generator = StaticMapGenerator(width=400, height=300, zoom=12)

    def tearDown(self):
        for file in self.tmp_dir.glob("*.png"):
            file.unlink()
        self.tmp_dir.rmdir()

    def test_get_map_image_returns_image(self):
        coords = (59.437, 24.7536)
        img = self.generator.get_map_image(coords)
        self.assertIsInstance(img, Image.Image)
        self.assertGreater(img.size[0], 0)
        self.assertGreater(img.size[1], 0)

    def test_save_map_creates_file(self):
        filename = self.tmp_dir / "map.png"
        coords = (59.437, 24.7536)
        path = self.generator.save_map(coords, filename=str(filename))
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 100)

    def test_multiple_calls_do_not_overlap(self):
        file1 = self.tmp_dir / "map1.png"
        file2 = self.tmp_dir / "map2.png"
        self.generator.save_map((59.437, 24.7536), filename=str(file1))
        self.generator.save_map((59.44, 24.75), filename=str(file2))
        self.assertTrue(file1.exists())
        self.assertTrue(file2.exists())
        self.assertNotEqual(os.path.getsize(file1), os.path.getsize(file2))

# ===============================
# 4. Основной запуск
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

