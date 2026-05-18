import pygame


class GUI:

    def __init__(self):

        pygame.init()

        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

        pygame.display.set_caption("Chess")

        self.running = True

    def draw_board(self):

        tile_size = self.screen_width // 8

        for row in range(8):
            for col in range(8):

                color = (255, 255, 255) if (row + col) % 2 == 0 else (85, 106, 47)

                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * tile_size, row * tile_size, tile_size, tile_size)
                )

    def draw_pieces(self, gc):

        tile_size = self.screen_width // 8
        board = gc.get_board()

        for row in range(8):
            for col in range(8):

                piece = board[row][col]

                if piece != ".":

                    img = pygame.image.load(
                        "pieces/" + piece + ".png"
                    ).convert_alpha()

                    self.screen.blit(
                        img,
                        (10 + col * tile_size, 10 + row * tile_size)
                    )

    def highlight_sq(self, gc):

        tile_size = self.screen_width // 8
        moves = gc.get_selected_moves()

        for move in moves:

            highlight = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)

            pygame.draw.rect(
                highlight,
                (255, 0, 0, 50),
                (0, 0, tile_size, tile_size)
            )

            self.screen.blit(
                highlight,
                (move[0] * tile_size, move[1] * tile_size)
            )

    def start(self, gc):

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    x, y = pygame.mouse.get_pos()
                    tile_size = self.screen_width // 8

                    col = x // tile_size
                    row = y // tile_size

                    gc.handle_click(row, col)

            self.screen.fill((255, 255, 255))

            self.draw_board()
            self.highlight_sq(gc)
            self.draw_pieces(gc)

            pygame.display.flip()

        pygame.quit()