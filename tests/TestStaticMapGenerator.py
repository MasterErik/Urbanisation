import os
import unittest
from pathlib import Path
from PIL import Image
from urbanisation_package.StaticMapGenerator import StaticMapGenerator


class TestStaticMapGenerator(unittest.TestCase):
    """Тесты для класса StaticMapGenerator."""

    def setUp(self):
        """Создает временную директорию и экземпляр генератора перед каждым тестом."""
        self.tmp_dir = Path("tmp_test_maps")
        self.tmp_dir.mkdir(exist_ok=True)
        self.generator = StaticMapGenerator(width=400, height=300, zoom=12)

    def tearDown(self):
        """Удаляет временные файлы после тестов."""
        for file in self.tmp_dir.glob("*.png"):
            file.unlink()
        self.tmp_dir.rmdir()
        # print(self.tmp_dir)

    def test_get_map_image_returns_image(self):
        """Метод get_map_image должен возвращать объект PIL.Image."""
        img = self.generator.get_map_image((59.437, 24.7536))
        self.assertIsInstance(img, Image.Image)
        self.assertGreater(img.size[0], 0)
        self.assertGreater(img.size[1], 0)

    def test_save_map_creates_file(self):
        """Метод save_map должен сохранять PNG-файл."""
        filename = self.tmp_dir / "map.png"
        path = self.generator.save_map((59.437, 24.7536), filename=str(filename))
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 1000)

    def test_multiple_calls_do_not_overlap(self):
        """Несколько вызовов save_map должны создавать разные файлы."""
        file1 = self.tmp_dir / "map1.png"
        file2 = self.tmp_dir / "map2.png"

        self.generator.save_map((59.437, 24.7536), filename=str(file1))
        self.generator.save_map((59.44, 24.75), filename=str(file2))

        self.assertTrue(file1.exists())
        self.assertTrue(file2.exists())
        self.assertNotEqual(os.path.getsize(file1), os.path.getsize(file2))


if __name__ == "__main__":
    unittest.main()

