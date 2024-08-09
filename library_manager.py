import os
import csv
from library_item import LibraryItem

class LibraryManager:
    def __init__(self, data_file_path):
        self.csv_file_path = data_file_path
        self.library = []
        self.load_data_from_csv()

    def load_data_from_csv(self):
        if os.path.isfile(self.csv_file_path):
            print(f"Loading data from {self.csv_file_path}")
            try:
                with open(self.csv_file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    print(f"Headers: {reader.fieldnames}")
                    for row in reader:
                        print(f"Row data: {row}")
                        try:
                            item = LibraryItem(
                                int(row['number']),
                                row['name'],
                                row['director'],
                                int(row['rating']),
                                int(row['play_count'])
                            )
                            self.library.append(item)
                        except ValueError as e:
                            print(f"Error parsing row {row}: {e}")
            except Exception as e:
                print(f"Error reading {self.csv_file_path}: {e}")
        else:
            print(f"File {self.csv_file_path} not found. Starting with an empty library.")

    def save_library_to_csv(self):
        fieldnames = ['number', 'name', 'director', 'rating', 'play_count']
        try:
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for video in self.library:
                    writer.writerow({
                        'number': video.number,
                        'name': video.name,
                        'director': video.director,
                        'rating': video.rating,
                        'play_count': video.play_count
                    })
        except Exception as e:
            print(f"Error saving to {self.csv_file_path}: {e}")

    def get_item(self, number):
        return next((video for video in self.library if video.number == number), None)

    def add_item(self, item):
        if self.get_item(item.number) is not None:
            print(f"Item with number {item.number} already exists.")
            return False
        self.library.append(item)
        self.save_library_to_csv()
        return True

    def update_item(self, number, new_rating, new_play_count):
        video = self.get_item(number)
        if video:
            video.rating = new_rating
            video.play_count = new_play_count
            self.save_library_to_csv()
            return True
        return False

    def delete_item(self, number):
        video = self.get_item(number)
        if video:
            self.library.remove(video)
            self.save_library_to_csv()
            return True
        return False

    def list_all_videos(self):
        return [f"{video.number} {video.name} - {video.director} {'*' * video.rating} (Play Count: {video.play_count})" for video in self.library]

    def search_by_director(self, director_name):
        return [video for video in self.library if director_name.lower() in video.director.lower()]

    def search_by_name(self, video_name):
        return [video for video in self.library if video_name.lower() in video.name.lower()]
    
    def get_name(self, video_number):
        item = self.get_item(video_number)
        if item:
            return item.name
        return None
    
    def get_item_by_name(self, name):
        for item in self.items:  # Assuming `self.items` holds all LibraryItem instances
            if item.name == name:
                return item
        return None
