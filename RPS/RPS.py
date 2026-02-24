"""
Rock-Paper-Scissors (CLI)

A simple command-line implementation of the classic game.

Features:
(i) Score tracking;
(ii) Input validation;
(iii) Clear game loop structure.
"""

import random

OPTIONS = ("rock", "paper", "scissors")

def get_user_choice() -> str | None:
    """
    Prompt user for input.

    Returns:
        Valid choice ("rock", "paper", "scissors")
        or None if user wants to quit.
    """
    user_input = input("Type Rock/Paper/Scissors (Q to quit): ").strip().lower()

    if user_input == "q":
        return None

    if user_input not in OPTIONS:
        print("Invalid choice. Try again.")
        return get_user_choice()

    return user_input

def get_computer_choice() -> str:
    """
    Randomly select computer move.
    """
    return random.choice(OPTIONS)

def determine_winner(user: str, computer: str) -> int:
    """
    Determine game outcome.

    Returns:
        1  -> user wins
        -1 -> computer wins
        0  -> tie
    """
    if user == computer:
        return 0

    wins = {
        ("rock", "scissors"),
        ("paper", "rock"),
        ("scissors", "paper"),
    }

    return 1 if (user, computer) in wins else -1

def main() -> None:
    """
    Run the main game loop.
    """
    user_score = 0
    computer_score = 0

    while True:
        user_choice = get_user_choice()

        if user_choice is None:
            break

        computer_choice = get_computer_choice()
        print(f"Computer picked: {computer_choice}")

        result = determine_winner(user_choice, computer_choice)

        if result == 1:
            print("You won!")
            user_score += 1
        elif result == -1:
            print("You lost!")
            computer_score += 1
        else:
            print("It's a tie!")

        print(f"Score: You {user_score} - Computer {computer_score}\n")

    print("Final score:")
    print(f"You won {user_score} times.")
    print(f"Computer won {computer_score} times.")

if __name__ == "__main__":
    main()
