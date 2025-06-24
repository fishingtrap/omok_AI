BOARD_SIZE = 19

class OmokBoard:
    def __init__(self):
        self.board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def display(self):
        print("  " + " ".join(chr(c + ord('A')) for c in range(BOARD_SIZE)))
        for i in range(BOARD_SIZE):
            row = [self.board[i][j] for j in range(BOARD_SIZE)]
            print(f"{i+1:2} " + " ".join(row))

    def make_move(self, x, y, player):
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == '.':
            self.board[x][y] = player
            return True
        return False

    def check_win(self, x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for d in [1, -1]:
                nx, ny = x + d*dx, y + d*dy
                while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == player:
                    count += 1
                    nx += d*dx
                    ny += d*dy
            if count >= 5:
                return True
        return False