import random

HUMAN = "X"
AI = "O"

board = [" " for _ in range(10)]

def insert_letter(letter: str, pos: int) -> None:
    """
    Place a letter on the board at the given position.

    Args:
        letter: "X" or "O".
        pos: Board position (1–9).
    """
    board[pos] = letter

def free_space(pos: int) -> bool:
    """
    Check whether a board position is empty.

    Args:
        pos: Board position (1–9).

    Returns:
        True if the position is empty, otherwise False.
    """
    return board[pos] == " "

def print_board(bo: list[str]) -> None:
    """
    Print the current state of the board in a formatted layout.
    """
    print("   |   |")
    print(f" {bo[1]} | {bo[2]} | {bo[3]}")
    print("   |   |")
    print("-----------")
    print("   |   |")
    print(f" {bo[4]} | {bo[5]} | {bo[6]}")
    print("   |   |")
    print("-----------")
    print("   |   |")
    print(f" {bo[7]} | {bo[8]} | {bo[9]}")
    print("   |   |")


def is_winner(bo: list[str], le: str) -> bool:
    """
    Determine whether a player has won.

    Args:
        bo: Current board.
        le: Player symbol ("X" or "O").

    Returns:
        True if the player has a winning combination.
    """
    wins = [
        (7, 8, 9),
        (4, 5, 6),
        (1, 2, 3),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7),
    ]
    return any(bo[a] == bo[b] == bo[c] == le for a, b, c in wins)

def available_moves(bo: list[str]) -> list[int]:
    """
    Get a list of available (empty) board positions.

    Args:
        bo: Current board.

    Returns:
        List of free positions (1–9).
    """
    return [i for i in range(1, 10) if bo[i] == " "]

def player_move() -> None:
    """
    Handle user input and place the HUMAN symbol on the board.

    Ensures:
        - Input is numeric
        - Position is within range
        - Position is not already occupied
    """
    while True:
        move_str = input(f"Select a position to place '{HUMAN}' (1-9): ").strip()
        try:
            move = int(move_str)
        except ValueError:
            print("Type a number.")
            continue

        if move not in range(1, 10):
            print("Select a number within the range 1-9.")
            continue

        if not free_space(move):
            print("This space is already taken.")
            continue

        insert_letter(HUMAN, move)
        return

def select_random(moves: list[int]) -> int:
    """
    Select a random move from a list of possible moves.

    Args:
        moves: List of valid board positions.

    Returns:
        Randomly selected position.
    """
    return random.choice(moves)

def computer_move() -> int:
    """
    Determine the AI move using a rule-based strategy.

    Strategy:
        1. Win if possible.
        2. Block opponent win.
        3. Take a corner.
        4. Take center.
        5. Take an edge.

    Returns:
        Selected board position (1–9).
        Returns 0 if no moves are available.
    """
    possible = available_moves(board)

    for let in (AI, HUMAN):
        for i in possible:
            copy_board = board[:]
            copy_board[i] = let
            if is_winner(copy_board, let):
                return i

    corners = [i for i in (1, 3, 7, 9) if i in possible]
    if corners:
        return select_random(corners)

    if 5 in possible:
        return 5

    edges = [i for i in (2, 4, 6, 8) if i in possible]
    if edges:
        return select_random(edges)

    return 0

def full_board(bo: list[str]) -> bool:
    """
    Check whether the board is full.

    Args:
        bo: Current board.

    Returns:
        True if no empty spaces remain.
    """
    return " " not in bo[1:]

def main() -> None:
    """
    Run the Tic-Tac-Toe game loop.

    The human player always starts first.
    """
    print_board(board)

    while True:
        if is_winner(board, AI):
            print("Sorry to tell you, but you lost to PC.")
            break
        if is_winner(board, HUMAN):
            print("Yay, you won! Well played.")
            break
        if full_board(board):
            print("Well, it is a Tie Game.")
            break

        player_move()
        print_board(board)

        if is_winner(board, HUMAN) or full_board(board):
            continue

        move = computer_move()
        if move == 0:
            print("Well, it is a Tie Game.")
            break

        insert_letter(AI, move)
        print(f"Computer made a play in position {move}")
        print_board(board)

if __name__ == "__main__":
    main()
