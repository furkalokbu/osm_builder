import os
import asyncio
import aiohttp
import math
from io import BytesIO
from PIL import Image


TILE_SIZE = 256
MAX_CONCURRENT_DOWNLOADS = 10


def calculate_and_constrain_tile_coordinates(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    tile_x = int((lon + 180.0) / 360.0 * n)
    tile_y = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)

    tile_x = max(0, min(tile_x, int(n) - 1))
    tile_y = max(0, min(tile_y, int(n) - 1))

    return tile_x, tile_y


async def download_tile(session, sem, url):
    async with sem:
        async with session.get(url) as response:
            print(response)
            return await response.read()


async def download_tiles(tile_urls):
    sem = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)
    async with aiohttp.ClientSession() as session:
        tasks = [download_tile(session, sem, url) for url in tile_urls]
        return await asyncio.gather(*tasks)


def create_image_from_tiles(tiles, width, height):
    result_image = Image.new('RGB', (width * TILE_SIZE, height * TILE_SIZE))

    for idx, tile in enumerate(tiles):
        try:
            tile_image = Image.open(BytesIO(tile))
            x = (idx % width) * TILE_SIZE
            y = (idx // width) * TILE_SIZE
            result_image.paste(tile_image, (x, y))
        except Exception as e:
            print(f"Error processing tile {idx}: {e}")

    return result_image


def save_image(img, output_path):
    img.save(output_path, 'PNG')


def main(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        try:
            latitude1 = float(lines[0].strip())
            longitude1 = float(lines[1].strip())
            latitude2 = float(lines[2].strip())
            longitude2 = float(lines[3].strip())
            zoom_level = float(lines[4].strip())

        except ValueError as e:
            print(f"Error parsing input parameters: {e}")
            return

    tile_x1, tile_y1 = calculate_and_constrain_tile_coordinates(latitude1, longitude1, zoom_level)
    tile_x2, tile_y2 = calculate_and_constrain_tile_coordinates(latitude2, longitude2, zoom_level)

    tile_urls = [
        f'https://tile.openstreetmap.org/{zoom_level}/{x}/{y}.png'
        for x in range(tile_x1, tile_x2 + 1)
        for y in range(tile_y1, tile_y2 + 1)
    ]
    try:
        tiles = asyncio.run(download_tiles(tile_urls))
        if not tiles or len(tiles) != (tile_x2 - tile_x1 + 1) * (tile_y2 - tile_y1 + 1):
            print("Invalid dimensions. Check your input parameters.")
            return

        width = tile_x2 - tile_x1 + 1
        height = tile_y2 - tile_y1 + 1
        stitched_image = create_image_from_tiles(tiles, width, height)

        output_path = 'output_image.png'
        save_image(stitched_image, output_path)

        print(f"Image saved successfully at: {output_path}")

    except Exception as e:
        print(f"Error downloading or processing tiles: {e}")

def run_for_all_files_in_directory(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for file_name in files:
        input_file = os.path.join(directory, file_name)
        print(f"Running script for file: {input_file}")
        main(input_file)

if __name__ == "__main__":
    input_directory = 'inputs/'
    main('inputs/input_parameters_1.txt')
    # run_for_all_files_in_directory(input_directory)
