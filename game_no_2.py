import pygame
import random
import math

class Game2048:
    def __init__(self):
        pygame.init()

        self.FPS = 60
        self.WIDTH, self.HEIGHT = 800, 800
        self.ROWS, self.COLS = 4, 4
        self.RECT_HEIGHT = self.HEIGHT // self.ROWS
        self.RECT_WIDTH = self.WIDTH // self.COLS

        self.OUTLINE_COLOR = (187, 173, 160)
        self.OUTLINE_THICKNESS = 10
        self.BACKGROUND_COLOR = (205, 192, 180)
        self.FONT_COLOR = (119, 110, 101)

        self.FONT = pygame.font.SysFont("comicsans", 60, bold=True)
        self.MOVE_VEL = 20

        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("2048 Game")

    class Tile:
        COLORS = [
            (237, 229, 218),
            (238, 225, 201),
            (243, 178, 122),
            (246, 150, 101),
            (247, 124, 95),
            (247, 95, 59),
            (237, 208, 115),
            (237, 204, 99),
            (236, 202, 80),
        ]

        def __init__(self, value, row, col, width, height, font, font_color):
            self.value = value
            self.row = row
            self.col = col
            self.x = col * width
            self.y = row * height
            self.width = width
            self.height = height
            self.font = font
            self.font_color = font_color

        def get_color(self):
            color_index = int(math.log2(self.value)) - 1
            return self.COLORS[min(color_index, len(self.COLORS)-1)]

        def draw(self, window):
            pygame.draw.rect(window, self.get_color(), (self.x, self.y, self.width, self.height))
            text = self.font.render(str(self.value), 1, self.font_color)
            window.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2),
                ),
            )

        def set_pos(self, ceil=False):
            if ceil:
                self.row = math.ceil(self.y / self.height)
                self.col = math.ceil(self.x / self.width)
            else:
                self.row = math.floor(self.y / self.height)
                self.col = math.floor(self.x / self.width)

        def move(self, delta):
            self.x += delta[0]
            self.y += delta[1]

    def draw_grid(self):
        for row in range(1, self.ROWS):
            y = row * self.RECT_HEIGHT
            pygame.draw.line(self.WINDOW, self.OUTLINE_COLOR, (0, y), (self.WIDTH, y), self.OUTLINE_THICKNESS)

        for col in range(1, self.COLS):
            x = col * self.RECT_WIDTH
            pygame.draw.line(self.WINDOW, self.OUTLINE_COLOR, (x, 0), (x, self.HEIGHT), self.OUTLINE_THICKNESS)

        pygame.draw.rect(self.WINDOW, self.OUTLINE_COLOR, (0, 0, self.WIDTH, self.HEIGHT), self.OUTLINE_THICKNESS)

    def draw(self, tiles):
        self.WINDOW.fill(self.BACKGROUND_COLOR)
        for tile in tiles.values():
            tile.draw(self.WINDOW)
        self.draw_grid()
        pygame.display.update()

    def get_random_pos(self, tiles):
        while True:
            row = random.randrange(0, self.ROWS)
            col = random.randrange(0, self.COLS)
            if f"{row}{col}" not in tiles:
                return row, col

    def move_tiles(self, tiles, clock, direction):
        updated = True
        blocks = set()

        def setup_direction(direction):
            if direction == "left":
                return lambda x: x.col, False, (-self.MOVE_VEL, 0), \
                       lambda t: t.col == 0, \
                       lambda t: tiles.get(f"{t.row}{t.col - 1}"), \
                       lambda t, n: t.x > n.x + self.MOVE_VEL, \
                       lambda t, n: t.x > n.x + self.RECT_WIDTH + self.MOVE_VEL, True
            elif direction == "right":
                return lambda x: x.col, True, (self.MOVE_VEL, 0), \
                       lambda t: t.col == self.COLS - 1, \
                       lambda t: tiles.get(f"{t.row}{t.col + 1}"), \
                       lambda t, n: t.x < n.x - self.MOVE_VEL, \
                       lambda t, n: t.x + self.RECT_WIDTH + self.MOVE_VEL < n.x, False
            elif direction == "up":
                return lambda x: x.row, False, (0, -self.MOVE_VEL), \
                       lambda t: t.row == 0, \
                       lambda t: tiles.get(f"{t.row - 1}{t.col}"), \
                       lambda t, n: t.y > n.y + self.MOVE_VEL, \
                       lambda t, n: t.y > n.y + self.RECT_HEIGHT + self.MOVE_VEL, True
            elif direction == "down":
                return lambda x: x.row, True, (0, self.MOVE_VEL), \
                       lambda t: t.row == self.ROWS - 1, \
                       lambda t: tiles.get(f"{t.row + 1}{t.col}"), \
                       lambda t, n: t.y < n.y - self.MOVE_VEL, \
                       lambda t, n: t.y + self.RECT_HEIGHT + self.MOVE_VEL < n.y, False

        sort_func, reverse, delta, boundary_check, get_next_tile, merge_check, move_check, ceil = setup_direction(direction)

        while updated:
            clock.tick(self.FPS)
            updated = False
            sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

            for i, tile in enumerate(sorted_tiles):
                if boundary_check(tile):
                    continue

                next_tile = get_next_tile(tile)
                if not next_tile:
                    tile.move(delta)
                elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                    if merge_check(tile, next_tile):
                        tile.move(delta)
                    else:
                        next_tile.value *= 2
                        sorted_tiles.pop(i)
                        blocks.add(next_tile)
                elif move_check(tile, next_tile):
                    tile.move(delta)

                tile.set_pos(ceil)
                updated = True

            self.update_tiles(tiles, sorted_tiles)

        return self.end_move(tiles)

    def end_move(self, tiles):
        if len(tiles) == 16:
            return "lost"

        row, col = self.get_random_pos(tiles)
        tiles[f"{row}{col}"] = self.Tile(random.choice([2, 4]), row, col, self.RECT_WIDTH, self.RECT_HEIGHT, self.FONT, self.FONT_COLOR)
        return "continue"

    def update_tiles(self, tiles, sorted_tiles):
        tiles.clear()
        for tile in sorted_tiles:
            tiles[f"{tile.row}{tile.col}"] = tile
        self.draw(tiles)

    def generate_tiles(self):
        tiles = {}
        for _ in range(2):
            row, col = self.get_random_pos(tiles)
            tiles[f"{row}{col}"] = self.Tile(2, row, col, self.RECT_WIDTH, self.RECT_HEIGHT, self.FONT, self.FONT_COLOR)
        return tiles

    def run(self):
        clock = pygame.time.Clock()
        tiles = self.generate_tiles()
        run = True

        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_tiles(tiles, clock, "left")
                    elif event.key == pygame.K_RIGHT:
                        self.move_tiles(tiles, clock, "right")
                    elif event.key == pygame.K_UP:
                        self.move_tiles(tiles, clock, "up")
                    elif event.key == pygame.K_DOWN:
                        self.move_tiles(tiles, clock, "down")

            self.draw(tiles)

        pygame.quit()


if __name__ == "__main__":
    game = Game2048()
    game.run()
