import os
import random


def delete_files_in_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def generate_input_parameters(index):
    map_id = f'map_{index}'
    min_lat = round(random.uniform(-90, 90), 4)
    min_lon = round(random.uniform(-180, 180), 4)
    max_lat = round(random.uniform(min_lat, 90), 4)
    max_lon = round(random.uniform(min_lon, 180), 4)

    zoom = random.randint(1, 18)

    return map_id, min_lat, min_lon, max_lat, max_lon, zoom


if __name__ == "__main__":

    input_path = 'inputs/'

    delete_files_in_directory(input_path)

    for i in range(1, 101):

        file_name = os.path.join(input_path, f"input_parameters_{i}.txt")
        parameters = generate_input_parameters(i)

        with open(file_name, "w") as file:
            file.write("\n".join(map(str, parameters)))
