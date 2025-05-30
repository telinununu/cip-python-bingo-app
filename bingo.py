import customtkinter as ctk
import random
from tkinter import messagebox

# Constants for layout and phrases
ROWS = 5
COLS = 5
CELL_WIDTH = 255
CELL_HEIGHT = 155
WINDOW_WIDTH = CELL_WIDTH * COLS + 60
WINDOW_HEIGHT = CELL_HEIGHT * ROWS + 180

# List of fun bingo phrases about learning Python
PHRASES = [
    "Attended a makeup section", "Asked ChatGPT for help", "Commented out half the code", "Program works by accident", "Typed ‘list’ as a variable name",
    "Used list instead of str", "IndentationError... again", "Used = instead of ==", "Infinite loop panic", "Missed a colon",
    "Karel won’t turn left", "Watched lecture at 1.5x speed", "Did the assignment 1 hour before section", "Added a print just to see what happens", "Stuck on making quilt in graphics",
    "Put beeper… in the wrong spot", "Mixed up keys and values", "Debugged for 30 mins… typo", "Didn’t test edge cases", "Printed ‘Hello World’ like a boss",
    "Wrote a function, forgot to call it", "Didn’t write comments, got lost in own code", "Wrote the solution… outside of main()", "Index out of range", "Googled the error message"
]

# Each row has a different pastel color
ROW_COLORS = ["#E0E3FF", "#CACFFF", "#B6BDFF", "#A1AAFF", "#959FFD"]

class BingoApp(ctk.CTk):
    """
    Main application class for the Python-themed Bingo game.
    This class sets up the window, creates a grid of bingo tiles,
    handles user interaction, checks for wins, and manages the game state.
    """
    def __init__(self):
        super().__init__()
        self.title("CIP - Learning Python Bingo")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.update_idletasks()
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.resizable(False, False)
        self.configure(fg_color="white")

        # Add fullscreen toggle button
        self.fullscreen = False
        self.toggle_btn = ctk.CTkButton(
            master=self,
            text=" Fullscreen Mode",
            command=self.toggle_fullscreen,
            width=150
        )
        self.toggle_btn.pack(pady=(10, 0))

        # Internal state trackers
        self.grid_buttons = []
        self.marked = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.frozen = False

        # Instruction label above the board
        self.info_label = ctk.CTkLabel(
            master=self,
            text="Click the tiles that apply to your Python journey.\nGet five in a row to win Bingo.",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        self.info_label.pack(pady=(20, 10))

        # Control panel for reset button
        self.control_frame = ctk.CTkFrame(self, fg_color="white")
        self.control_frame.pack(pady=10)

        self.reset_btn = ctk.CTkButton(
            master=self.control_frame,
            text="Reset Board",
            command=self.reset_board,
            width=120
        )
        self.reset_btn.pack(side="left", padx=10)

        # Grid where bingo tiles live
        self.grid_frame = ctk.CTkFrame(self, fg_color="white")
        self.grid_frame.pack()

        self.build_board()

    def toggle_fullscreen(self):
        """
        Toggle the fullscreen mode for the application window.
        Useful for maximizing screen space and improving visibility during gameplay.
        """
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def build_board(self):
        self.clear_grid()
        self.grid_buttons = []
        self.marked = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.frozen = False

        phrases = random.sample(PHRASES, ROWS * COLS - 1)

        for i in range(ROWS):
            row_buttons = []
            for j in range(COLS):
                if i == ROWS // 2 and j == COLS // 2:
                    phrase = " ☆ ☆ ☆ ☆ Free Space ☆ ☆ ☆ ☆ "
                    is_free = True
                else:
                    phrase = phrases.pop(0)
                    is_free = False

                base_color = ROW_COLORS[i % len(ROW_COLORS)]

                btn = ctk.CTkButton(
                    master=self.grid_frame,
                    text=phrase,
                    width=CELL_WIDTH,
                    height=CELL_HEIGHT,
                    corner_radius=10,
                    font=ctk.CTkFont(size=15),
                    fg_color="#FFBC6A" if is_free else base_color,
                    hover_color="#FFD262",
                    text_color="#000745",
                    anchor="center",
                    command=lambda x=i, y=j: self.toggle_cell(x, y)
                )
                btn.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
                btn._text_label.configure(wraplength=CELL_WIDTH - 20, justify="center")
                row_buttons.append((btn, base_color))
                self.marked[i][j] = is_free
            self.grid_buttons.append(row_buttons)

    def toggle_cell(self, row, col):
        if self.frozen or (row == ROWS // 2 and col == COLS // 2):
            return
        self.marked[row][col] = not self.marked[row][col]
        btn, base_color = self.grid_buttons[row][col]
        new_color = "#FFBC6A" if self.marked[row][col] else base_color
        btn.configure(fg_color=new_color, text_color="#000745")
        self.check_win()

    def check_win(self):
        """
        Check if the user has completed a row, column, or diagonal.
        If a winning pattern is found, trigger the celebration animation.
        """
        winning_cells = []

        for i in range(ROWS):
            if all(self.marked[i]):
                winning_cells = [(i, j) for j in range(COLS)]
                break

        if not winning_cells:
            for j in range(COLS):
                if all(self.marked[i][j] for i in range(ROWS)):
                    winning_cells = [(i, j) for i in range(ROWS)]
                    break

        if not winning_cells and all(self.marked[i][i] for i in range(ROWS)):
            winning_cells = [(i, i) for i in range(ROWS)]

        if not winning_cells and all(self.marked[i][COLS - 1 - i] for i in range(ROWS)):
            winning_cells = [(i, COLS - 1 - i) for i in range(ROWS)]

        if winning_cells:
            self.flash_celebration(winning_cells)

    def flash_celebration(self, cells):
        """
        Visually celebrate a win by flashing the entire board in soft colors
        a few times. Then restore all tiles and show a popup message.
        This helps highlight the moment of winning before locking the board.
        """
        def flash_all(times):
            color = "#ABECB1" if times % 2 == 0 else "#7CD384"
            for row_buttons in self.grid_buttons:
                for btn, _ in row_buttons:
                    btn.configure(fg_color=color)
            if times < 4:
                self.after(180, lambda: flash_all(times + 1))
            else:
                for i in range(ROWS):
                    for j in range(COLS):
                        btn, base_color = self.grid_buttons[i][j]
                        if self.marked[i][j]:
                            btn.configure(fg_color="#FFBC6A")
                        else:
                            btn.configure(fg_color=base_color)
                self.frozen = True
                messagebox.showinfo("Bingo!", "You got 5 in a row! 🥳")

        flash_all(0)

    def reset_board(self):
        self.build_board()

    def clear_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = BingoApp()
    app.mainloop()
