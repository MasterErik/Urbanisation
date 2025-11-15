import os

from urbanisation_package.geolocator import get_coordinates
from urbanisation_package.GeneratorMapPNG import get_PNG
from urbanisation_package.UrbanizationAnalyzer import UrbanizationAnalyzer


def main():
    place_name = input("Введите место: ")
    locations = get_coordinates(place_name)

    if locations:
        loc = locations[0]
        coords = (loc["latitude"], loc["longitude"])
        print(f"Найдено: {loc['address']}")
        print(f"Координаты: {coords}")
    else:
        print("Ничего не найдено")

    # 2. Генерируем PNG в папке tmp_test_maps
    filename = get_PNG(coords, place_name)
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
