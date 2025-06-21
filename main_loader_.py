import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import webbrowser
import os

class GameLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("500x450")
        self.root.configure(bg="white")
        self.create_widgets()

    
    def create_widgets(self):
        tk.Label(self.root, text="Select a Game", font=("Helvetica", 20), bg="white").pack(pady=20)

        frame = tk.Frame(self.root, bg="white")
        frame.pack()

        self.add_game_button(frame, "Game 1", "assets/game1.png", self.launch_game1)
        self.add_game_button(frame, "Game 2", "assets/game2.png", self.launch_game2)

        video_btn = tk.Button(
            self.root,
            text="🎬 Watch Video",
            font=("Arial", 14),
            bg="#0099ff",
            fg="white",
            command=self.play_video,
            padx=20,
            pady=10
        )
        video_btn.pack(pady=30)



    def add_game_button(self, parent, title, img_path, command):
        try:
            img = Image.open(img_path)
            img = img.resize((120, 120))
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            photo = None
            print(f"Error loading image {img_path}: {e}")

        btn = tk.Button(parent, text=title, image=photo, compound="top",
                        command=command, width=140, height=150)
        btn.image = photo  # Save reference to prevent garbage collection
        btn.pack(side="left", padx=15)

    def launch_game1(self):
        self.run_script("game_no_1.py")
    
    def launch_game2(self):
        self.run_script("game_no_2.py")

    def run_script(self, filename):
        try:
            subprocess.Popen(["python", filename])
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch {filename}\n{e}")


    def play_video(self):
        video_path = os.path.abspath("assets/sample_video.mp4")
        try:
            webbrowser.open(video_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not play video\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncherApp(root)
    root.mainloop()


    