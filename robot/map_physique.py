import pygame

TILE_SIZE = 40

MAP = [
    "111111111111",
    "100000000001",
    "101111011101",
    "100000000001",
    "101011111101",
    "100010000001",
    "111111111111",
]


class MapPhysique:
    def __init__(self):
        self.murs = []
        self.generer_murs()

    def generer_murs(self):
        for row_index, row in enumerate(MAP):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    rect = pygame.Rect(
                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    self.murs.append(rect)

    def draw(self, screen):
        for mur in self.murs:
            pygame.draw.rect(screen, (0, 0, 255), mur)