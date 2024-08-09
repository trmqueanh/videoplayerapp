class LibraryItem:
    def __init__(self, number, name, director, rating, play_count=0):
        self.number = number
        self.name = name
        self.director = director
        self.rating = rating
        self.play_count = play_count
    
    def get_name(self):
        return self.name

    def get_director(self):
        return self.director

    def get_rating(self):
        return self.rating

    def set_rating(self, rating):
        self.rating = rating

    def get_play_count(self):
        return self.play_count

    def increment_play_count(self):
        self.play_count += 1
    