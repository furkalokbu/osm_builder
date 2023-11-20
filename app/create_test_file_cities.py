import os, random


cities = {
    'Kyiv': (50.4501, 30.5234),
    'New York': (40.7128, -74.0060),
    'Los Angeles': (34.0522, -118.2437),
    'Chicago': (41.8781, -87.6298),
    'San Francisco': (37.7749, -122.4194),
    'Tokyo': (35.6895, 139.6917),
    'London': (51.5099, -0.1180),
    'Sydney': (-33.8688, 151.2093),
}


def generate_random_coordinates(city_coordinates):
    lat_range = (city_coordinates[0] - 1, city_coordinates[0] + 1)
    lon_range = (city_coordinates[1] - 1, city_coordinates[1] + 1)
    return (
        round(random.uniform(lat_range[0], lat_range[1]), 4),
        round(random.uniform(lon_range[0], lon_range[1]), 4)
    )


def create_input_file(city, output_path):
    city_coordinates = cities[city]
    random_coordinates = generate_random_coordinates(city_coordinates)
    zoom_level = random.randint(10, 15)
    map_id = f"map_{random.randint(1, 100)}"  # Example: Assign a random map_id

    with open(output_path, 'w') as file:
        file.write(f"{map_id}\n")
        file.write(f"{random_coordinates[0]}\n{random_coordinates[1]}\n")
        file.write(f"{city_coordinates[0]}\n{city_coordinates[1]}\n")
        file.write(f"{zoom_level}\n")


def delete_files_in_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")


if __name__ == "__main__":

    input_path = 'inputs/'
    delete_files_in_directory(input_path)

    for i in range(1, 101):
        file_name = os.path.join(input_path, f"input_parameters_{i}.txt")
        city = random.choice(list(cities.keys()))
        create_input_file(city, file_name)
        print(f"File created: {file_name}")
