from PIL import Image
import numpy as np

class UrbanizationAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(self.image_path).convert("RGB")
        self.arr = np.array(self.image)

        # Урбанизация: здания, внутренние территории, дороги
        self.urban_colors = [
            [0xd9, 0xd0, 0xc9],  # здания
            [0xf2, 0xda, 0xd9],  # внутренние территории
            [0xe0, 0xdf, 0xdf],  # внутренние территории
            [0xdd, 0xdd, 0xe8],  # дороги
            [0xf7, 0xfa, 0xbf],  # дороги
            [0xff, 0xff, 0xff]   # дороги
        ]

        # Исключаем ярко-красные маркеры
        self.exclude_colors = [
            [255, 0, 0]  # если есть чисто красные
        ]

    def mask_natural(self):
        # Зеленые зоны: G>100, R,B<100
        green_mask = (self.arr[:,:,1] > 100) & (self.arr[:,:,0] < 100) & (self.arr[:,:,2] < 100)
        # Синие зоны: B>100, R,G<100
        blue_mask = (self.arr[:,:,2] > 100) & (self.arr[:,:,0] < 100) & (self.arr[:,:,1] < 100)
        return green_mask | blue_mask

    def mask_urban(self):
        mask = np.zeros((self.arr.shape[0], self.arr.shape[1]), dtype=bool)
        for color in self.urban_colors:
            mask |= np.all(self.arr == color, axis=2)
        return mask

    def mask_exclude(self):
        mask = np.zeros((self.arr.shape[0], self.arr.shape[1]), dtype=bool)
        for color in self.exclude_colors:
            mask |= np.all(self.arr == color, axis=2)
        return mask

    def analyze(self):
        natural_mask = self.mask_natural()
        urban_mask = self.mask_urban()
        exclude_mask = self.mask_exclude()

        # Исключаем маркеры
        natural_mask[exclude_mask] = False
        urban_mask[exclude_mask] = False

        total_pixels = self.arr.shape[0] * self.arr.shape[1]
        natural_pixels = np.sum(natural_mask)
        urban_pixels = np.sum(urban_mask)
        other_pixels = total_pixels - (natural_pixels + urban_pixels)

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
