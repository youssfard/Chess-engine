import copy
from move_manager import move_manager


class gamecontroller:
    def __init__(self):
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["pw", "pw", "pw", "pw", "pw", "pw", "pw", "pw"],
            ["rw", "nw", "bw", "qw", "kw", "bw", "nw", "rw"]
        ]

        self.black_pieces = ["p", "r", "n", "b", "q", "k"]
        self.white_pieces = ["pw", "rw", "nw", "bw", "qw", "kw"]

        self.turn = "w"
        self.move_manager = move_manager()

        self.active_piece = None
        self.active_pos = None
        self.selected_moves = []

        self.in_check = False
        self.in_checkmate = False

    def get_turn(self):
        return self.turn

    def next_turn(self):
        self.turn = "b" if self.turn == "w" else "w"

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_piece_color(self, piece):
        return "b" if piece in self.black_pieces else "w"

    def same_color(self, p1, p2):
        return self.get_piece_color(p1) == self.get_piece_color(p2)

    def get_board(self):
        return self.board

    def get_selected_moves(self):
        return self.selected_moves

    def select_piece(self, row, col):
        piece = self.get_piece(row, col)

        if piece == ".":
            return
        if self.get_piece_color(piece) != self.turn:
            return

        self.active_piece = piece
        self.active_pos = (row, col)
        self.selected_moves = self.get_possible_moves(row, col)

    def clear_selection(self):
        self.active_piece = None
        self.active_pos = None
        self.selected_moves = []

    def is_valid_move(self, row, col):
        return (col, row) in self.selected_moves

    def play_move(self, row, col):
        old_row, old_col = self.active_pos
        piece = self.active_piece

        self.board[old_row][old_col] = "."
        self.board[row][col] = piece

        self.clear_selection()

        self.next_turn()
        self.update_game_state()

    def get_possible_moves(self, row, col):
        piece = self.get_piece(row, col)

        if piece in ["pw", "p"]:
            moves = self.move_manager.pawn_moves(col, row, piece, self.board, self)

        elif piece in ["r", "rw"]:
            moves = self.move_manager.rook_moves(col, row, self.board, self, piece)

        elif piece in ["b", "bw"]:
            moves = self.move_manager.bishop_moves(col, row, piece, self.board, self)

        elif piece in ["q", "qw"]:
            moves = (
                self.move_manager.rook_moves(col, row, self.board, self, piece) +
                self.move_manager.bishop_moves(col, row, piece, self.board, self)
            )

        elif piece in ["n", "nw"]:
            moves = self.move_manager.knight_moves(col, row, piece, self.board, self)

        elif piece in ["k", "kw"]:
            moves = self.move_manager.king_moves(col, row, piece, self.board, self)

        else:
            return []

        legal_moves = []
        for (c, r) in moves:
            test_board = self.simulate_move(self.board, (row, col), (r, c), piece)
            if self.is_king_safe(test_board, self.get_piece_color(piece)):
                legal_moves.append((c, r))

        return legal_moves

    def simulate_move(self, board, from_pos, to_pos, piece):
        new_board = copy.deepcopy(board)
        fr, fc = from_pos
        tr, tc = to_pos
        new_board[fr][fc] = "."
        new_board[tr][tc] = piece
        return new_board

    def is_king_safe(self, board, color):
        king_pos = self.find_king(color, board)
        enemy = "b" if color == "w" else "w"
        return not self.detect_check(board, king_pos, enemy)

    def is_in_check(self, color):
        king_pos = self.find_king(color, self.board)
        enemy = "b" if color == "w" else "w"
        return self.detect_check(self.board, king_pos, enemy)

    def find_king(self, color, board):
        target = "kw" if color == "w" else "k"

        for row in range(8):
            for col in range(8):
                if board[row][col] == target:
                    return (col, row)

    def handle_click(self, row, col):
        if self.active_piece is None:
            self.select_piece(row, col)
            return

        if self.is_valid_move(row, col):
            self.play_move(row, col)

        else:
            self.clear_selection()
            self.select_piece(row, col)

    def detect_check(self, board, king_pos, enemy_color):
        for row in range(8):
            for col in range(8):
                piece = board[row][col]

                if piece == ".":
                    continue
                if self.get_piece_color(piece) != enemy_color:
                    continue

                attacks = self.move_manager.get_attacks(col, row, piece, board, self)

                if king_pos in attacks:
                    return True

        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece == ".":
                    continue
                if self.get_piece_color(piece) != color:
                    continue

                moves = self.get_possible_moves(row, col)
                if len(moves) > 0:
                    return False

        return True

    def update_game_state(self):
        color = self.turn

        self.in_check = self.is_in_check(color)

        if self.is_checkmate(color):
            self.in_checkmate = True
            print("CHECKMATE")