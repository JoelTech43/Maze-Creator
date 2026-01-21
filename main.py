import pygame
import pygame_gui

pygame.init()

maze_size = 100
pygame.display.set_caption("Maze Creator")
window = pygame.display.set_mode((5*maze_size, 5*maze_size))

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

maze = [[(False, False, False, False) for i in range(maze_size)] for j in range(maze_size)]

class Cursor:
    def __init__(self, start_pos, colour):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.col = colour

    def move(self, move):
        if move == (-1, 0) and self.x != 0:
            self.x -= 1
        elif move == (1, 0) and self.x != maze_size-1:
            self.x += 1
        elif move == (0, -1) and self.y != 0:
            self.y -= 1
        elif move == (0, 1) and self.y != maze_size-1:
            self.y += 1
        
    def draw(self, canvas):
        pygame.draw.rect(canvas, self.col, (self.x*(maze_size//2), self.y*(maze_size//2), maze_size//2, maze_size//2), width=2,)

exit = False
cursor = Cursor((0,0), GREEN)

while not exit:
    window.fill(WHITE)
    cursor.draw(window)
    pygame.display.update()