from omok_ai import OmokAI  # OmokAI 클래스
from omok_board import OmokBoard  # 보드 클래스

import sys

def main():
    # 사용자 인자 받기: 플레이어 색(B/W), 시간제한(초)
    player = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ['B', 'W'] else 'B'
    time_limit = 10

    board = OmokBoard()
    ai = OmokAI(player, time_limit)

    current_turn = 'B'

    while True:
        board.display()

        if current_turn == player:
            print(f"AI({player}) is thinking...")
            x, y = ai.search(board)
            print(f"AI chooses: {chr(y + ord('A'))},{x + 1}")
        else:
            move = input("Enter move (e.g., J,10): ")
            try:
                col, row = move.strip().split(',')
                y = ord(col.upper()) - ord('A')
                x = int(row) - 1
            except:
                print("Invalid input. Try again.")
                continue

        success = board.make_move(x, y, current_turn)
        if not success:
            print("Invalid move. Try again.")
            continue

        if board.check_win(x, y, current_turn):
            board.display()
            print(f"{current_turn} wins!")
            break

        current_turn = 'W' if current_turn == 'B' else 'B'

if __name__ == "__main__":
    main()