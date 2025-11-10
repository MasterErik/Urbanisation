from PIL import Image
import numpy as np

class UrbanizationAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(self.image_path).convert("RGB")
        self.arr = np.array(self.image)

        # Категории зон
        self.categories = {
            "urban": [
                [0xd9, 0xd0, 0xc9],  # здания
                [0xf2, 0xda, 0xd9],  # внутренние территории
                [0xe0, 0xdf, 0xdf],
                [0xdd, 0xdd, 0xe8],  # дороги
                [0xf7, 0xfa, 0xbf],
                [0xff, 0xff, 0xff]
            ],
            "natural_green": "condition",  # проверка по каналу G
            "natural_blue": [
                [0xac, 0xd2, 0xde]  # водоёмы
            ],
            "exclude": [
                [255, 0, 0]  # красные маркеры
            ]
        }

    def mask_category(self, category):
        if category == "natural_green":
            R = self.arr[:,:,0]
            G = self.arr[:,:,1]
            B = self.arr[:,:,2]
            return (G > 100) & (G > R) & (G > B)
        else:
            mask = np.zeros((self.arr.shape[0], self.arr.shape[1]), dtype=bool)
            for color in self.categories[category]:
                mask |= np.all(self.arr == color, axis=2)
            return mask

    def analyze(self):
        masks = {cat: self.mask_category(cat) for cat in self.categories}

        # Исключаем маркеры
        exclude_mask = masks["exclude"]
        for cat in ["urban", "natural_green", "natural_blue"]:
            masks[cat][exclude_mask] = False

        total_pixels = self.arr.shape[0] * self.arr.shape[1]
        urban_pixels = np.sum(masks["urban"])
        natural_pixels = np.sum(masks["natural_green"] | masks["natural_blue"])
        other_pixels = total_pixels - (urban_pixels + natural_pixels)

        return {
            "image_path": self.image_path,
            "urban_percent": float(urban_pixels / total_pixels * 100),
            "natural_percent": float(natural_pixels / total_pixels * 100),
            "other_percent": float(other_pixels / total_pixels * 100)
        }

# Пример использования
if __name__ == "__main__":
    analyzer = UrbanizationAnalyzer("Tallinn.png")
    result = analyzer.analyze()
    print(f"Image: {result['image_path']}")
    print(f"Urbanization: {result['urban_percent']:.2f}%")
    print(f"Natural: {result['natural_percent']:.2f}%")
    print(f"Other: {result['other_percent']:.2f}%")
