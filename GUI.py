import tkinter as tk
from functools import partial

# Create the main chess game window
window = tk.Tk()
window.title("Chess Game")

# Create the chessboard GUI
chessboard_frame = tk.Frame(window)
chessboard_frame.pack()

chessboard_buttons = []
for row in range(8):
    row_buttons = []
    for col in range(8):
        button = tk.Button(chessboard_frame, width=4, height=2)
        button.grid(row=row, column=col)
        row_buttons.append(button)
    chessboard_buttons.append(row_buttons)

# Example function to update the chessboard GUI based on the game state
def update_chessboard(game_state):
    for row in range(8):
        for col in range(8):
            piece = game_state[row][col]
            button = chessboard_buttons[row][col]
            # Set the button's text and color based on the piece
            button.configure(text=piece, bg="white" if (row + col) % 2 == 0 else "gray")

# Example function to handle a human player's move
def handle_human_move(row, col):
    # Get the selected row and column and make the move
    make_move(row, col)
    # Update the chessboard GUI
    update_chessboard(game_state)

    # AI's turn
    ai_move = get_best_move(game_state)
    make_move(ai_move[0], ai_move[1])
    # Update the chessboard GUI
    update_chessboard(game_state)

# Bind the buttons to the human move handler
for row in range(8):
    for col in range(8):
        chessboard_buttons[row][col].configure(command=partial(handle_human_move, row, col))

# Start the game
update_chessboard(game_state)  # Update the chessboard GUI based on the initial game state

# Run the GUI main loop
window.mainloop()
