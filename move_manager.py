class move_manager:
    def __init__(self):
        pass

    def get_attacks(self, col, row, piece, board, gc):

        if piece == "r" or piece == "rw":
            return self.rook_moves(col, row, board, gc, piece)

        elif piece == "b" or piece == "bw":
            return self.bishop_moves(col, row, piece, board, gc)

        elif piece == "q" or piece == "qw":
            return (
                    self.rook_moves(col, row, board, gc, piece) +
                    self.bishop_moves(col, row, piece, board, gc)
            )

        elif piece == "n" or piece == "nw":
            return self.knight_moves(col, row, piece, board, gc)

        elif piece == "k" or piece == "kw":
            return self.king_moves(col, row, piece, board, gc)

        return []

    def king_moves(self, col,row,piece,board,gc):
        available = []

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            r = row + dr
            c = col + dc

            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]

                if target == ".":
                    available.append((c, r))
                elif not gc.same_color(target, piece):
                    available.append((c, r))

        return available

    def knight_moves(self, col, row, piece, board, gc):
        available = []

        directions = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        for dr, dc in directions:
            r = row + dr
            c = col + dc

            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]

                if target == ".":
                    available.append((c, r))
                elif not gc.same_color(target, piece):
                    available.append((c, r))

        return available

    def bishop_moves(self, col,row,piece,board,gc):
        available = []
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        for dr, dc in directions:
            r = row + dr
            c = col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == ".":
                    available.append((c, r))
                elif gc.same_color(board[r][c], piece):
                    break
                else:
                    available.append((c, r))
                    break
                r += dr
                c += dc
        return available

    def rook_moves(self, col, row, board,gc,piece):
        available = []
        directions = [(-1, 0),(1, 0),(0, -1),(0, 1)]

        for dr, dc in directions:
            r = row + dr
            c = col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == ".":
                    available.append((c, r))
                elif gc.same_color(board[r][c],piece):
                    break
                else:
                    available.append((c, r))
                    break
                r += dr
                c += dc
        return available


    def pawn_moves(self, col, row, piece, board,gc):
        modifier = 1 if gc.get_piece_color(piece) == "w" else -1
        available = []
        available += self.get_pawn_captures(modifier, col, row, board,gc,piece)

        for i in range(1, 3):
            if i == 2:
                if gc.get_piece_color(piece) == "w" and row != 6:
                    break
                if gc.get_piece_color(piece) == "b" and row != 1:
                    break

            if board[row - modifier * i][col] == ".":
                available.append((col, row - modifier * i))
            else:
                break

        return available

    def get_pawn_captures(self, modifier, c, r, board, gc, piece):
        captures = []
        nr = r - modifier

        if 0 <= nr < 8 and 0 <= c + 1 < 8:
            target1 = board[nr][c + 1]

            if target1 != "." and not gc.same_color(target1, piece):
                captures.append((c + 1, nr))

        if 0 <= nr < 8 and 0 <= c - 1 < 8:
            target2 = board[nr][c - 1]

            if target2 != "." and not gc.same_color(target2, piece):
                captures.append((c - 1, nr))

        return captures