import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from library_manager import LibraryManager
from library_item import LibraryItem

class VideoPlayerApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.video_list = None
        self.video_number_entry = None
        self.director_name_entry = None
        self.video_name_entry = None
        self.blank_box = None
        self.status_label = None
        self.create_video_number_entry = None
        self.create_video_name_entry = None
        self.create_video_director_entry = None
        self.create_video_rating_entry = None
        self.create_video_play_count_entry = None
        self.update_video_number_entry = None
        self.update_video_rating_entry = None
        self.update_video_play_count_entry = None
        self.delete_video_number_entry = None
        self.playlist = []  # Initialize playlist
        self.create_main_window()

    def set_text(self, widget, content):
        if isinstance(widget, Label):
           widget.config(text=content)
        elif isinstance(widget, Text):
           widget.delete(1.0, tk.END)
           widget.insert(tk.END, content)


    def list_all_videos(self):
        self.video_list.delete(0, tk.END)
        for title in self.manager.list_all_videos():
            self.video_list.insert(tk.END, title)
        self.set_text(self.status_label, "Listed all videos!")

    def check_video(self):
        video_number = self.video_number_entry.get()
        director_name = self.director_name_entry.get()
        video_name = self.video_name_entry.get()

        if video_number:
            try:
                video_number = int(video_number)
                item = self.manager.get_item(video_number)
                if item:
                    details = f"Name: {item.name}\nDirector: {item.director}\nRating: {item.rating}\nPlay Count: {item.play_count}"
                else:
                    details = "Invalid video number."
            except ValueError:
                details = "Please enter a valid number."
        elif director_name:
            items = self.manager.search_by_director(director_name)
            if items:
                details = "\n\n".join([f"Name: {item.name}\nDirector: {item.director}\nRating: {item.rating}\nPlay Count: {item.play_count}" for item in items])
            else:
                details = "No videos found for the given director."
        elif video_name:
            items = self.manager.search_by_name(video_name)
            if items:
                details = "\n\n".join([f"Name: {item.name}\nDirector: {item.director}\nRating: {item.rating}\nPlay Count: {item.play_count}" for item in items])
            else:
                details = "No videos found for the given name."
        else:
            details = "Please enter a video number, director's name, or video name."

        if details == "Please enter a valid number.":
            self.set_text(self.status_label, details)
        else:
            self.blank_box.delete(1.0, tk.END)
            self.blank_box.insert(tk.END, details)

    def create_video(self):
        video_number = self.create_video_number_entry.get()
        video_name = self.create_video_name_entry.get()
        video_director = self.create_video_director_entry.get()
        video_rating = self.create_video_rating_entry.get()
        video_play_count = self.create_video_play_count_entry.get()

        try:
            video_number = int(video_number)
            video_rating = int(video_rating)
            video_play_count = int(video_play_count)
            new_video = LibraryItem(video_number, video_name, video_director, video_rating, video_play_count)
            self.manager.add_item(new_video)
            self.set_text(self.status_label, "Video added successfully!")
            self.play_video(new_video)  # Play the video after adding it
        except ValueError:
            self.set_text(self.status_label, "Please enter valid numbers for Video Number, Rating, and Play Count.")

    def play_video(self, video):
        # This is a placeholder for video playing functionality
        self.set_text(self.status_label, f"Playing video: {video.name}")

    def update_video(self):
        video_number = self.update_video_number_entry.get()
        new_rating = self.update_video_rating_entry.get()
        new_play_count = self.update_video_play_count_entry.get()

        try:
            video_number = int(video_number)
            new_rating = int(new_rating)
            new_play_count = int(new_play_count)
            if self.manager.update_item(video_number, new_rating, new_play_count):
                self.set_text(self.status_label, "Video updated successfully!")
            else:
                self.set_text(self.status_label, "Video not found.")
        except ValueError:
            self.set_text(self.status_label, "Please enter valid numbers for Video Number, Rating, and Play Count.")

    def delete_video(self):
        video_number = self.delete_video_number_entry.get()

        try:
            video_number = int(video_number)
            if self.manager.delete_item(video_number):
                self.set_text(self.status_label, "Video deleted successfully!")
            else:
                self.set_text(self.status_label, "Video not found.")
        except ValueError:
            self.set_text(self.status_label, "Please enter a valid number for Video Number.")

    def show_create_video_list_window(self):
        create_video_list_window = Toplevel(self.root)
        create_video_list_window.title("Create Video List")
        create_video_list_window.geometry("750x350")

        Label(create_video_list_window, text="Enter Video Number", font=('Italic', 16)).grid(row=0, column=0, padx=10, pady=10)

        self.input_txt = Entry(create_video_list_window, width=3, font=('Italic', 14))
        self.input_txt.grid(row=0, column=1, padx=10, pady=10)

        Button(create_video_list_window, text="Add Video", font=('Italic', 14), command=self.add_video_clicked).grid(row=0, column=2, padx=10, pady=10)
        Button(create_video_list_window, text="Play Playlist", font=('Italic', 14), command=self.play_playlist_clicked).grid(row=0, column=3, padx=10, pady=10)
        Button(create_video_list_window, text="Reset Playlist", font=('Italic', 14), command=self.reset_playlist_clicked).grid(row=0, column=4, padx=10, pady=10)

        self.playlist_txt = ScrolledText(create_video_list_window, width=48, height=12, wrap="none")
        self.playlist_txt.grid(row=1, column=0, columnspan=5, sticky="W", padx=10, pady=10)

        self.status_lbl = Label(create_video_list_window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=5, sticky="W", padx=10, pady=10)

    def add_video_clicked(self):
        key = self.input_txt.get()
        try:
            key = int(key)
            item = self.manager.get_item(key)  # Assuming get_item returns a LibraryItem or None
            if item:
                self.playlist.append(item.name)
                self.update_playlist_text()
                self.set_text(self.status_lbl, f"Video {item.name} added to playlist!")
            else:
                self.set_text(self.status_lbl, f"Video {key} not found")
        except ValueError:
                self.set_text(self.status_lbl, "Please enter a valid number.")

    def play_playlist_clicked(self):
        if self.playlist:
           video_details = ""
           for video_name in self.playlist:
            # Find the video item by name
                items = self.manager.search_by_name(video_name)
                if items:
                    item = items[0]  # Assuming the first item is the match
                # Increment the play count for each video
                item.play_count += 1
                self.manager.update_item(item.number, item.rating, item.play_count)
                video_details += f"Name: {item.name}\nDirector: {item.director}\nRating: {item.rating}\nPlay Count: {item.play_count}\n\n"
        # Update the playlist display
                self.update_playlist_text()
                self.set_text(self.playlist_txt, video_details.strip())
                self.set_text(self.status_lbl, "Playlist played and play counts updated successfully!")
        else:
            self.playlist_txt.delete(1.0, tk.END)
            self.playlist_txt.insert(tk.END, "Playlist is empty")
            self.set_text(self.status_lbl, "Playlist is empty.")

    def reset_playlist_clicked(self):
        self.playlist = []
        self.update_playlist_text()
        self.set_text(self.status_lbl, "Playlist reset successfully!")

    def update_playlist_text(self):
        self.playlist_txt.delete(1.0, tk.END)
        self.playlist_txt.insert(tk.END, "\n".join(self.playlist))

    def go_back(self, window):
        window.destroy()

    def create_main_window(self):
        self.root.title("Video Player App")
        self.root.geometry("730x600")
        self.root.resizable(False, False)

        Label(self.root, text="Select an option by clicking one of the buttons below", fg='black', font=('Italic', 16), width=60).grid(row=0, column=0, columnspan=4, pady=10)
        peer_1_frame = Frame(self.root)
        peer_2_frame = Frame(self.root)
        peer_3_frame = Frame(self.root)
        peer_4_frame = Frame(self.root)
        peer_5_frame = Frame(self.root)

        Button(peer_1_frame, text='Check Videos', width=11, height=1, font=('Italic', 14), command=self.show_video_check_window).pack(pady=5)
        Button(peer_2_frame, text='Create Video', width=14, height=1, font=('Italic', 14), command=self.show_create_video_window).pack(pady=5)
        Button(peer_3_frame, text='Update Videos', width=12, height=1, font=('Italic', 14), command=self.show_update_video_window).pack(pady=5)
        Button(peer_4_frame, text='Delete Videos', width=12, height=1, font=('Italic', 14), command=self.show_delete_video_window).pack(pady=5)
        Button(peer_5_frame, text='Create Playlist', width=14, height=1, font=('Italic', 14), command=self.show_create_video_list_window).pack(pady=5)

        peer_1_frame.grid(row=1, column=0, padx=(10, 10))
        peer_2_frame.grid(row=1, column=1, padx=(10, 10))
        peer_3_frame.grid(row=1, column=2, padx=(10, 10))
        peer_4_frame.grid(row=1, column=3, padx=(10, 10))
        peer_5_frame.grid(row=2, column=0, columnspan=4, pady=(10, 10))

        self.status_label = Label(self.root, text="", fg='red', font=('Italic', 12), width=60)
        self.status_label.grid(row=3, column=0, columnspan=4, pady=10)

        self.video_list = Listbox(self.root, height=15, width=85)
        self.video_list.grid(row=4, column=0, columnspan=4, pady=10)

        Button(self.root, text="List All Videos", font=('Italic', 14), command=self.list_all_videos).grid(row=5, column=0, columnspan=4, pady=5)

    def show_video_check_window(self):
        check_window = Toplevel(self.root)
        check_window.title("Check Videos")
        check_window.geometry("700x600")

        Label(check_window, text="Enter the video number, director's name, or video name to check details", font=('Italic', 16)).pack(pady=10)

        Label(check_window, text="Video Number:").pack()
        self.video_number_entry = Entry(check_window, font=('Italic', 14), width=20)
        self.video_number_entry.pack(pady=5)

        Label(check_window, text="Or enter Director's Name:").pack()
        self.director_name_entry = Entry(check_window, font=('Italic', 14), width=20)
        self.director_name_entry.pack(pady=5)

        Label(check_window, text="Or enter Video Name:").pack()
        self.video_name_entry = Entry(check_window, font=('Italic', 14), width=20)
        self.video_name_entry.pack(pady=5)

        Button(check_window, text="Check", font=('Italic', 14), command=self.check_video).pack(pady=10)

        self.blank_box = Text(check_window, height=10, width=50)
        self.blank_box.pack(pady=20)

        Button(check_window, text="Back", font=('Italic', 14), command=lambda: self.go_back(check_window)).pack(pady=5)

    def show_create_video_window(self):
        create_window = Toplevel(self.root)
        create_window.title("Create Videos")
        create_window.geometry("700x500")

        Label(create_window, text="Enter the details of the new video", font=('Italic', 16)).pack(pady=10)

        Label(create_window, text="Video Number:").pack()
        self.create_video_number_entry = Entry(create_window, font=('Italic', 14), width=20)
        self.create_video_number_entry.pack(pady=5)

        Label(create_window, text="Video Name:").pack()
        self.create_video_name_entry = Entry(create_window, font=('Italic', 14), width=20)
        self.create_video_name_entry.pack(pady=5)

        Label(create_window, text="Video Director:").pack()
        self.create_video_director_entry = Entry(create_window, font=('Italic', 14), width=20)
        self.create_video_director_entry.pack(pady=5)

        Label(create_window, text="Video Rating:").pack()
        self.create_video_rating_entry = Entry(create_window, font=('Italic', 14), width=20)
        self.create_video_rating_entry.pack(pady=5)

        Label(create_window, text="Play Count:").pack()
        self.create_video_play_count_entry = Entry(create_window, font=('Italic', 14), width=20)
        self.create_video_play_count_entry.pack(pady=5)

        Button(create_window, text="Create", font=('Italic', 14), command=self.create_video).pack(pady=10)
        Button(create_window, text="Back", font=('Italic', 14), command=lambda: self.go_back(create_window)).pack(pady=5)

    def show_update_video_window(self):
        update_window = Toplevel(self.root)
        update_window.title("Update Videos")
        update_window.geometry("700x500")

        Label(update_window, text="Enter the details of the video to update", font=('Italic', 16)).pack(pady=10)

        Label(update_window, text="Video Number:").pack()
        self.update_video_number_entry = Entry(update_window, font=('Italic', 14), width=20)
        self.update_video_number_entry.pack(pady=5)

        Label(update_window, text="New Rating:").pack()
        self.update_video_rating_entry = Entry(update_window, font=('Italic', 14), width=20)
        self.update_video_rating_entry.pack(pady=5)

        Label(update_window, text="New Play Count:").pack()
        self.update_video_play_count_entry = Entry(update_window, font=('Italic', 14), width=20)
        self.update_video_play_count_entry.pack(pady=5)

        Button(update_window, text="Update", font=('Italic', 14), command=self.update_video).pack(pady=10)
        Button(update_window, text="Back", font=('Italic', 14), command=lambda: self.go_back(update_window)).pack(pady=5)

    def show_delete_video_window(self):
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Videos")
        delete_window.geometry("700x500")

        Label(delete_window, text="Enter the video number to delete", font=('Italic', 16)).pack(pady=10)

        Label(delete_window, text="Video Number:").pack()
        self.delete_video_number_entry = Entry(delete_window, font=('Italic', 14), width=20)
        self.delete_video_number_entry.pack(pady=5)

        Button(delete_window, text="Delete", font=('Italic', 14), command=self.delete_video).pack(pady=10)
        Button(delete_window, text="Back", font=('Italic', 14), command=lambda: self.go_back(delete_window)).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    manager = LibraryManager("C:\Coursework\Courswork\musiclist.csv")
    app = VideoPlayerApp(root, manager)
    root.mainloop()