import os
from pathlib import Path
from urbanisation_package.geolocator import get_coordinates
from urbanisation_package.Urbanisation3 import StaticMapGenerator
from urbanisation_package.UrbanizationAnalyzer import UrbanizationAnalyzer

def main():
    place_name = input("Введите название места: ")

    # 1. Получаем координаты
    locations = get_coordinates(place_name)
    if not locations:
        print("Место не найдено.")
        return

    # Берём первую найденную точку
    loc = locations[0]
    coords = (loc["latitude"], loc["longitude"])
    print(f"Найдено: {loc['address']}")
    print(f"Координаты: {coords}")

    # 2. Генерируем PNG в папке tmp_test_maps
    output_dir = Path("tmp_test_maps")
    output_dir.mkdir(exist_ok=True)
    filename = output_dir / f"{place_name.replace(' ', '_')}.png"

    generator = StaticMapGenerator(width=600, height=450, zoom=14)
    generator.save_map(coords, filename)
    print(f"Файл карты сохранён: {filename}")

    # 3. Анализируем PNG
    analyzer = UrbanizationAnalyzer(filename)
    result = analyzer.analyze()

    print("\nРезультаты анализа:")
    print(f"  Урбанизация: {result['urban_percent']:.2f}%")
    print(f"  Природные зоны: {result['natural_percent']:.2f}%")
    print(f"  Остальное: {result['other_percent']:.2f}%")

    # 4. Удаляем PNG после анализа
    try:
        filename.unlink()  # то же, что os.remove()
        print(f"\nФайл {filename.name} удалён после анализа.")
    except OSError as e:
        print(f"Ошибка при удалении {filename.name}: {e}")


if __name__ == "__main__":
    main()
