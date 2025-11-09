import os
from pathlib import Path
from PIL import Image
import unittest
from staticmap3 import StaticMap, CircleMarker

# ===============================
# 1. Функции работы с координатами
# ===============================

def get_coordinates(address: str):
    """
    Простейший пример: возвращает координаты по имени города или локации.
    Так как у нас нет API, можно сделать словарь с тестовыми адресами.
    """
    sample_coords = {
        "Красная площадь, Москва": (55.7540471, 37.620405),
        "Таллин, Эстония": (59.437, 24.7536)
    }
    coords = sample_coords.get(address)
    if coords:
        print(f"📍 Адрес: {address}")
        print(f"Координаты: {coords}")
        return coords
    else:
        print(f"❌ Координаты для '{address}' не найдены")
        return None

def get_address(lat: float, lng: float):
    """
    Обратное преобразование координат в адрес (только пример).
    """
    sample_addresses = {
        (55.7540471, 37.620405): "Красная площадь, Москва",
        (59.437, 24.7536): "Таллин, Эстония"
    }
    addr = sample_addresses.get((lat, lng))
    if addr:
        print(f"🌍 Координаты: {lat}, {lng}")
        print(f"Адрес: {addr}")
        return addr
    else:
        print(f"❌ Адрес для координат {lat}, {lng} не найден")
        return None

# ===============================
# 2. Класс StaticMapGenerator
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
        """
        Возвращает объект PIL.Image с картой.
        """
        lat, lng = coordinates
        m = StaticMap(self.width, self.height)
        marker = CircleMarker((lng, lat), 'red', 12)
        m.add_marker(marker)
        image = m.render()
        return image

    def save_map(self, coordinates, filename="map.png"):
        """
        Сохраняет карту в файл PNG.
        """
        img = self.get_map_image(coordinates)
        img.save(filename)
        return filename

# ===============================
# 3. Тесты для StaticMapGenerator
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
    # Получаем координаты из "адреса"
    coords = get_coordinates("Красная площадь, Москва")

    if coords:
        lat, lng = coords
        get_address(lat, lng)

        # Генерация карты
        print("\n🗺️ Генерация карты по координатам...")
        generator = StaticMapGenerator(width=400, height=300, zoom=14)
        filename = "moscow_map.png"
        generator.save_map(coords, filename)
        print(f"✅ Карта сохранена: {filename}")