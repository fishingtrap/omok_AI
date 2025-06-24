import time
import math
import random

BOARD_SIZE = 19
DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선, 역대각

class OmokAI:
    def __init__(self, player, time_limit):
        self.player = player  # 'B' or 'W'
        self.opponent = 'W' if player == 'B' else 'B'
        self.time_limit = time_limit
        self.start_time = None

    # ✅ 최상위 search 함수
    def search(self, board):
        self.start_time = time.time()

        # 1. 내가 지금 이길 수 있는 수가 있다면 그것부터 둔다
        win_move = self.find_immediate_win(board, self.player)
        if win_move:
            return win_move

        # 2. 그 외는 Alpha-Beta + Iterative Deepening
        best_move = None
        depth = 1
        while time.time() - self.start_time < self.time_limit:
            score, move = self.alphabeta(board, depth, -math.inf, math.inf, True)
            if time.time() - self.start_time >= self.time_limit:
                break
            if move:
                best_move = move
            depth += 1
        return best_move

    # ✅ Alpha-Beta 탐색 함수
    def alphabeta(self, board, depth, alpha, beta, maximizing):
        if time.time() - self.start_time >= self.time_limit or depth == 0:
            return self.heuristic(board), None

        best_move = None
        moves = self.get_candidate_moves(board)

        # Move Ordering: 더 좋은 수부터 탐색
        if maximizing:
            moves.sort(key=lambda move: self.score_move(board, move[0], move[1], self.player), reverse=True)
        else:
            moves.sort(key=lambda move: self.score_move(board, move[0], move[1], self.opponent), reverse=True)

        if maximizing:
            value = -math.inf
            for x, y in moves:
                board.make_move(x, y, self.player)
                score, _ = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.board[x][y] = '.'
                if score > value:
                    value = score
                    best_move = (x, y)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value, best_move
        else:
            value = math.inf
            for x, y in moves:
                board.make_move(x, y, self.opponent)
                score, _ = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.board[x][y] = '.'
                if score < value:
                    value = score
                    best_move = (x, y)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, best_move

    # ✅ 즉시 이기는 수 감지
    def find_immediate_win(self, board, player):
        moves = self.get_candidate_moves(board)
        for x, y in moves:
            board.make_move(x, y, player)
            if board.check_win(x, y, player):
                board.board[x][y] = '.'
                return (x, y)
            board.board[x][y] = '.'
        return None

    # ✅ 가능한 후보 수 위치만 추출 (탐색 공간 축소)
    def get_candidate_moves(self, board):
        candidates = set()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board.board[i][j] != '.':
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            ni, nj = i + dx, j + dy
                            if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and board.board[ni][nj] == '.':
                                candidates.add((ni, nj))
        if not candidates:
            # fallback: 중앙을 기본 시작점으로
            center = BOARD_SIZE // 2
            candidates.add((center, center))
        return list(candidates)

    # ✅ Move Ordering용 점수 평가
    def score_move(self, board, x, y, player):
        board.make_move(x, y, player)
        score = self.heuristic(board)  # 대략적인 평가
        board.board[x][y] = '.'
        return score

    # ✅ 휴리스틱 평가 함수 (중복 제거 포함)
    def heuristic(self, board):
        total_score = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board.board[x][y] != '.':
                    player = board.board[x][y]
                    for dx, dy in DIRECTIONS:
                        prev_x, prev_y = x - dx, y - dy
                        if 0 <= prev_x < BOARD_SIZE and 0 <= prev_y < BOARD_SIZE:
                            if board.board[prev_x][prev_y] == player:
                                continue
                        score = self.evaluate_pattern(board, x, y, dx, dy, player)
                        if player == self.player:
                            total_score += score
                        else:
                            total_score -= score
        return total_score

    # ✅ 한 방향에서 연속 돌 패턴 분석
    def evaluate_pattern(self, board, x, y, dx, dy, player):
        length = 1
        block = 0
        i, j = x + dx, y + dy

        # forward direction
        while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board.board[i][j] == player:
            length += 1
            i += dx
            j += dy
        if not (0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE) or board.board[i][j] != '.':
            block += 1

        # backward direction
        i, j = x - dx, y - dy
        while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board.board[i][j] == player:
            length += 1
            i -= dx
            j -= dy
        if not (0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE) or board.board[i][j] != '.':
            block += 1

        return self.get_score(length, block)

    # ✅ 점수표
    def get_score(self, length, block):
        if length >= 5:
            return 100000
        if length == 4:
            if block == 0:
                return 10000
            elif block == 1:
                return 2000
        elif length == 3:
            if block == 0:
                return 500
            elif block == 1:
                return 100
        elif length == 2:
            if block == 0:
                return 50
            elif block == 1:
                return 10
        elif length == 1:
            return 1
        return 0