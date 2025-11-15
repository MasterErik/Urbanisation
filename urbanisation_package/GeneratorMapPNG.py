from pathlib import Path
from urbanisation_package.StaticMapGenerator import StaticMapGenerator



def get_PNG(coords,place_name) -> str:


    # 2. Генерируем PNG в папке tmp_test_maps
    output_dir = Path("tmp_test_maps")
    output_dir.mkdir(exist_ok=True)
    filename = output_dir / f"{place_name.replace(' ', '_')}.png"

    generator = StaticMapGenerator(width=600, height=450, zoom=14)
    generator.save_map(coords, filename)


    return filename