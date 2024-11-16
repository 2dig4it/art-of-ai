#final code (created via ChatGPT)
import flet as ft
from flet import ElevatedButton, Page, Row, Text, Column, Audio

DBG_OUT = True #printf output, manually added

board = [["" for _ in range(3)] for _ in range(3)]
winner_text = Text(size=30)

# Function to determine if there's a winner
def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            if DBG_OUT: print(f"Winner found at row {i}")
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            if DBG_OUT: print(f"Winner found at column {i}")
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        if DBG_OUT: print("Winner found on main diagonal")
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        if DBG_OUT: print("Winner found on anti-diagonal")
        return board[0][2]
    return None

# Main function to build the Tic-Tac-Toe UI
def main(page: Page):
    page.title = "Tic-Tac-Toe with Flet"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Initialize board and game state
    current_player = ["Player 1"]
    current_player_text = Text(value="Current Player: Player 1 (Red X)", size=20)
    audio = Audio(src="https://www.example.com/im_in_the_thick_of_it.mp3", autoplay=False)

    # Function to handle button click
    def button_click(row, col):
        global board
        global winner_text
        if DBG_OUT: 
            print(f"Button clicked at row {row}, column {col}", type(winner_text.value) )
            print(board[0])
            print(board[1])
            print(board[2])
        if board[row][col] == '' and (winner_text.value == None or winner_text.value == ""): 
            # Change background color on click
            page.bgcolor = "#f0f0f0" if current_player[0] == "Player 1" else "#e0e0e0"
            page.update()
            
            symbol = "X" if current_player[0] == "Player 1" else "O"
            color = "red" if current_player[0] == "Player 1" else "blue"
            print(f"Placing {symbol} at row {row}, column {col}")
            board[row][col] = symbol
            buttons[row][col].text = symbol
            buttons[row][col].color = color
            buttons[row][col].update()
            winner = check_winner(board)
            if winner:
                print(f"Player {winner} wins!")
                winner_text.value = f"Player {'1' if winner == 'X' else '2'} wins!"
                winner_text.update()
                # Play audio when a player wins
                audio.autoplay = True
                audio.update()
                reset_button.visible = True
                reset_button.update()
            else:
                current_player[0] = "Player 2" if current_player[0] == "Player 1" else "Player 1"
                current_player_text.value = f"Current Player: {current_player[0]} ({'Red X' if current_player[0] == 'Player 1' else 'Blue O'})"
                current_player_text.update()
                print(f"Next player: {current_player[0]}")

    # Function to reset the game
    def reset_game(e):
        global board
        global winner_text
        
        board = [["" for _ in range(3)] for _ in range(3)]
        winner_text.value = None
        current_player[0] = "Player 1"
        current_player_text.value = None
        page.bgcolor = "white"
        current_player_text.update()
        winner_text.update()
        reset_button.visible = True
        reset_button.update()
        for i in range(3):
            for j in range(3):
                buttons[i][j].text = ""
                buttons[i][j].color = None
                buttons[i][j].update()

    # Create a 3x3 grid of buttons
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            btn = ElevatedButton(
                text="",
                width=100,
                height=100,
                on_click=lambda e, r=i, c=j: button_click(r, c),
            )
            row.append(btn)
        buttons.append(row)

    # Create reset button
    reset_button = ElevatedButton(
        text="Reset Game",
        visible=True,
        on_click=reset_game
    )

    # Add rows of buttons to the page
    for row in buttons:
        page.add(Row(controls=row))

    # Add current player text, winner text, audio, and reset button to the page
    page.add(Column(controls=[current_player_text, winner_text, reset_button, audio]))

# Run the Flet app
ft.app(target=main)
