board = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
]


def print_board():
    for row in board:
        print(row[0], "|", row[1], "|", row[2])
        print("---------")


def get_position(choice):
    match choice:
        case "1":
            return 0, 0
        case "2":
            return 0, 1
        case "3":
            return 0, 2
        case "4":
            return 1, 0
        case "5":
            return 1, 1
        case "6":
            return 1, 2
        case "7":
            return 2, 0
        case "8":
            return 2, 1
        case "9":
            return 2, 2
        case _:
            return -1, -1


def check_winner(player):
    if board[0][0] == player and board[0][1] == player and board[0][2] == player:
        return True

    if board[1][0] == player and board[1][1] == player and board[1][2] == player:
        return True

    if board[2][0] == player and board[2][1] == player and board[2][2] == player:
        return True

    if board[0][0] == player and board[1][0] == player and board[2][0] == player:
        return True

    if board[0][1] == player and board[1][1] == player and board[2][1] == player:
        return True

    if board[0][2] == player and board[1][2] == player and board[2][2] == player:
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False


def main():
    player = "X"

    while True:
        print_board()

        choice = input("Player " + player + ", enter position: ")

        row, col = get_position(choice)

        if row == -1:
            print("Invalid position!")
            continue

        if board[row][col] == "X" or board[row][col] == "O":
            print("Already taken!")
            continue

        board[row][col] = player

        if check_winner(player):
            print_board()
            print(player, "wins!")
            break

        if player == "X":
            player = "O"
        else:
            player = "X"

if __name__ == "__main__":
    main()
