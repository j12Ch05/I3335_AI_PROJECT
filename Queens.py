n = 0
fundamental = set()

def is_safe(row, col, board):
    for i in range(row):
        if board[i][col] == 2:
            return False

    i, j = row - 1, col - 1     # upper-left diagonal
    while i >= 0 and j >= 0:
        if board[i][j] == 2:
            return False
        i -= 1
        j -= 1

    i, j = row - 1, col + 1     # upper-right diagonal
    while i >= 0 and j < n:
        if board[i][j] == 2:
            return False
        i -= 1
        j += 1
        
    # after changing the algo, row checking is not necessary

    return True

def rotate90(b):
    r = [0] * n
    for i in range(n):
        r[b[i]] = n - 1 - i     # new row = old col || new col = n - 1 - old row
    return r

def reflect(b):
    r = [0] * n
    for i in range(n):
        r[i] = n - 1 - b[i]     # new col = 3 - old col
    return r

def canonical(b):
    forms = [b]

    r1 = rotate90(b)
    r2 = rotate90(r1)
    r3 = rotate90(r2)

    forms.append(r1)
    forms.append(r2)
    forms.append(r3)

    forms.append(reflect(b))
    forms.append(reflect(r1))
    forms.append(reflect(r2))
    forms.append(reflect(r3))

    return min(forms)

def solve(row, board, config):
    if row == n:
        fundamental.add(tuple(canonical(config)))
        return

    for col in range(n):
        if is_safe(row, col, board):
            board[row][col] = 2
            config[row] = col

            solve(row + 1, board, config)

            board[row][col] = 0     # backtracking :P
            config[row] = 0

def print_board(config):
    for i in range(n):
        for j in range(n):
            if config[i] == j:
                print("Q", end=" ")
            else:
                print("-", end=" ")
        print()
    print("======================================================")

def main():
    global n
    #n = int(input("Enter board size: "))

    board = [[0 for a in range(n)] for b in range(n)]   # creates a nxn boadr
    config = [0] * n        # List of n length filled with 0

    solve(0, board, config)

    print(f"\nSolutions: {len(fundamental)}\n")

    for sol in fundamental:
        print_board(sol)



if __name__ == "__main__":
    main()