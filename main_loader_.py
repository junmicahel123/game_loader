import tkinter as tk
from tkinter import messagebox


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



    def add_game_button(self, parent, title, img_path, command):
        pass

    def launch_game1(self):
        pass
    
    def launch_game2(self):
        pass

    def run_script(self, filename):
        pass

    def play_video(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncherApp(root)
    root.mainloop()


    