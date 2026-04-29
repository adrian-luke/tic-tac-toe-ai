import random
import os

board = [[" " for _ in range(3)] for _ in range(3)]

human = "X"
ai = "O"

human_score = 0
ai_score = 0
draw_score = 0


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def reset_board():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]


def print_board():
    print()
    num = 1

    for r in range(3):
        row = []
        for c in range(3):
            if board[r][c] == " ":
                row.append(str(num))
            else:
                row.append(board[r][c])
            num += 1

        print(" " + " | ".join(row))

        if r < 2:
            print("---+---+---")
    print()


def print_score():
    print(f"Score: You {human_score} | Computer {ai_score} | Draws {draw_score}")


def choose_symbol():
    global human, ai

    while True:
        choice = input("Do you want to be X or O? ").upper()

        if choice == "X":
            human = "X"
            ai = "O"
            break
        elif choice == "O":
            human = "O"
            ai = "X"
            break
        else:
            print("Pick X or O.")


def choose_difficulty():
    while True:
        print("\nChoose difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        choice = input("Enter 1, 2, or 3: ")

        if choice == "1":
            return "Easy"
        elif choice == "2":
            return "Medium"
        elif choice == "3":
            return "Hard"
        else:
            print("Invalid choice.")


def get_winner():
    for r in range(3):
        if board[r][0] != " " and board[r][0] == board[r][1] == board[r][2]:
            return board[r][0]

    for c in range(3):
        if board[0][c] != " " and board[0][c] == board[1][c] == board[2][c]:
            return board[0][c]

    if board[0][0] != " " and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] != " " and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def is_draw():
    return get_winner() is None and all(cell != " " for row in board for cell in row)


def get_available_moves():
    moves = []

    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                moves.append((r, c))

    return moves


def human_move():
    while True:
        try:
            move = int(input("Enter your move: "))

            if move < 1 or move > 9:
                print("Pick a number from 1 to 9.")
                continue

            row = (move - 1) // 3
            col = (move - 1) % 3

            if board[row][col] != " ":
                print("That spot is already taken.")
                continue

            board[row][col] = human
            break

        except ValueError:
            print("Enter a valid number.")


def random_ai_move():
    moves = get_available_moves()
    if moves:
        row, col = random.choice(moves)
        board[row][col] = ai


def find_winning_move(symbol):
    for row, col in get_available_moves():
        board[row][col] = symbol

        if get_winner() == symbol:
            board[row][col] = " "
            return row, col

        board[row][col] = " "

    return None


def smart_ai_move():
    # First, try to win.
    move = find_winning_move(ai)
    if move:
        row, col = move
        board[row][col] = ai
        return

    # Second, block the human from winning.
    move = find_winning_move(human)
    if move:
        row, col = move
        board[row][col] = ai
        return

    # Third, take center if open.
    if board[1][1] == " ":
        board[1][1] = ai
        return

    # Otherwise, random move.
    random_ai_move()


def ai_move(difficulty):
    if difficulty == "Easy":
        random_ai_move()

    elif difficulty == "Medium":
        if random.random() < 0.6:
            smart_ai_move()
        else:
            random_ai_move()

    else:
        smart_ai_move()


def play_game(difficulty):
    global human_score, ai_score, draw_score

    reset_board()

    current_turn = "X"

    while True:
        clear_screen()
        print("=== TIC-TAC-TOE ===")
        print_score()
        print(f"You are {human}. Computer is {ai}.")
        print_board()

        winner = get_winner()

        if winner == human:
            print("You win!")
            human_score += 1
            break

        elif winner == ai:
            print("Computer wins!")
            ai_score += 1
            break

        elif is_draw():
            print("It's a draw!")
            draw_score += 1
            break

        if current_turn == human:
            human_move()
        else:
            ai_move(difficulty)

        current_turn = "O" if current_turn == "X" else "X"


def main():
    clear_screen()
    print("=== TIC-TAC-TOE ===")

    choose_symbol()
    difficulty = choose_difficulty()

    while True:
        play_game(difficulty)

        while True:
            again = input("\nPlay again? (y/n): ").lower()

            if again == "y":
                break
            elif again == "n":
                print("Thanks for playing.")
                return
            else:
                print("Please enter y or n.")

main()
