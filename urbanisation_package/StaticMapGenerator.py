from staticmap3 import StaticMap, CircleMarker
from typing import Tuple, Optional
from PIL import Image


class StaticMapGenerator:
    """
    Генератор статических карт с меткой по координатам.
    Использует OpenStreetMap через библиотеку staticmap3.

    Пример:
        gen = StaticMapGenerator(width=800, height=600)
        img = gen.get_map_image((59.437, 24.7536), zoom=13)
        img.show()
    """

    def __init__(self, width: int = 400, height: int = 400, zoom: int = 12, tile_url: str = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
    ):
        self.zoom = zoom
        self.width = width
        self.height = height
        self.tile_url = tile_url

    def get_map_image(self, position: Tuple[float, float], marker_color: str = "red", marker_size: int = 12, ) -> Image.Image:
        """
        Возвращает PIL.Image карту с меткой по координатам (lat, lon).
        """
        lat, lon = position
        m = StaticMap(self.width, self.height, url_template=self.tile_url)
        marker = CircleMarker((lon, lat), marker_color, marker_size)
        m.add_marker(marker)
        return m.render(zoom=self.zoom)

    def save_map(self, position: Tuple[float, float], filename: str = "map.png", **kwargs, ) -> str:
        """
        Создает и сохраняет карту по координатам.
        Возвращает путь к файлу.
        """
        image = self.get_map_image(position, **kwargs)
        image.save(filename)
        return filename