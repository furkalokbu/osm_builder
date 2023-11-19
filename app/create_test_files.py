import os, sys
import random


def delete_existing_files():
    for i in range(1, 101):
        file_path = f"inputs/input_{i}.txt"
        if os.path.exists(file_path):
            os.remove(file_path)


def generate_test_input_file(file_index, country_name):
    if country_name.lower() == 'ukraine':
        latitude1 = random.uniform(44.4, 52.2)
        longitude1 = random.uniform(22.1, 40.2)
        latitude2 = random.uniform(44.4, 52.2)
        longitude2 = random.uniform(22.1, 40.2)
    else:
        latitude1 = random.uniform(0, 90)
        longitude1 = random.uniform(0, 180)
        latitude2 = random.uniform(0, 90)
        longitude2 = random.uniform(0, 180)

    map_id = f"map_{file_index}"
    zoom_level = random.randint(8, 15)

    with open(f"inputs/input_{file_index}.txt", 'w') as file:
        file.write(f"{latitude1},{longitude1},{latitude2},{longitude2},{map_id},{zoom_level}")


def main():
    delete_existing_files()
    country_name = sys.argv[1] if len(sys.argv) > 1 else 'another_country'
    for i in range(1, 101):
        generate_test_input_file(i, country_name)


if __name__ == "__main__":
    main()
