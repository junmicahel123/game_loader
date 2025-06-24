import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import webbrowser
import os

class GameLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Game Launcher")
        self.root.geometry("600x500")
        self.root.configure(bg="#ffe6f0") 
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="🎮 Choose Your Game",
            font=("Segoe UI", 24, "bold"),
            bg="#ffe6f0",
            fg="#333"
        )
        title.pack(pady=25)

        frame = tk.Frame(self.root, bg="#ffe6f0")
        frame.pack(pady=10)

        self.add_game_button(frame, "Game 1", "game1.png", self.launch_game1)
        self.add_game_button(frame, "Game 2", "game2.png", self.launch_game2)

        video_btn = tk.Button(
            self.root,
            text="🎬 Watch Video",
            font=("Segoe UI", 14, "bold"),
            bg="#ff4da6",
            fg="white",
            activebackground="#e60073",
            activeforeground="white",
            command=self.play_video,
            padx=20,
            pady=12,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        video_btn.pack(pady=40)

    def add_game_button(self, parent, title, img_path, command):
        try:
            img = Image.open(img_path)
            img = img.resize((120, 120))
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            photo = None
            print(f"Error loading image {img_path}: {e}")

        container = tk.Frame(parent, bg="#ffe6f0")
        container.pack(side="left", padx=25)

        btn = tk.Button(
            container,
            text=title,
            image=photo,
            compound="top",
            font=("Segoe UI", 12),
            command=command,
            width=140,
            height=160,
            bg="white",
            fg="#333",
            relief="raised",
            bd=2,
            cursor="hand2",
            activebackground="#ffb3d9"
        )
        btn.image = photo
        btn.pack()

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
        video_path = os.path.abspath("sample_video.mp4")
        try:
            webbrowser.open(video_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not play video\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncherApp(root)
    root.mainloop()
