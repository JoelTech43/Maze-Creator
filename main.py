import pygame
import os
import json

pygame.init()

maze_size = 100
cell_width = 8
pygame.display.set_caption("Maze Creator")
window = pygame.display.set_mode((cell_width*maze_size, cell_width*maze_size))

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255,0,0)
ORANGE = (255, 204, 0)
BLUE = (51, 102, 255)

maze = [[[False, False, False, False] for i in range(maze_size)] for j in range(maze_size)]
enemies = []
player = (0,0)
finish = (99,99)

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
        pygame.draw.rect(canvas, self.col, (self.x*(cell_width), self.y*(cell_width), cell_width, cell_width))

def draw_maze(canvas, maze):
    for rowInd in range(len(maze)):
        for colInd in range(len(maze[rowInd])):
            if maze[rowInd][colInd][0]:
                pygame.draw.rect(canvas, BLACK, (colInd*cell_width, rowInd*cell_width, 1, cell_width))
            if maze[rowInd][colInd][1]:
                pygame.draw.rect(canvas, BLACK, (colInd*cell_width, rowInd*cell_width, cell_width, 1))
            if maze[rowInd][colInd][2]:
                pygame.draw.rect(canvas, BLACK, (colInd*cell_width+cell_width-1, rowInd*cell_width, 1, cell_width))
            if maze[rowInd][colInd][3]:
                pygame.draw.rect(canvas, BLACK, (colInd*cell_width, rowInd*cell_width+cell_width-1, cell_width, 1))

def toggle_wall(dir):
    row, col = cursor.y, cursor.x
    match dir:
        case (-1,0):
            maze[row][col][0] = not maze[row][col][0]
            if col != 0:
                maze[row][col-1][2] = not maze[row][col-1][2]
        case (1,0):
            maze[row][col][2] = not maze[row][col][2]
            if col != maze_size-1:
                maze[row][col+1][0] = not maze[row][col+1][0]
        case (0,-1):
            maze[row][col][1] = not maze[row][col][1]
            if row != 0:
                maze[row-1][col][3] = not maze[row-1][col][3]
        case (0,1):
            maze[row][col][3] = not maze[row][col][3]
            if row != maze_size-1:
                maze[row+1][col][1] = not maze[row+1][col][1]

def toggle_enemy():
    coord = (cursor.x, cursor.y)
    if coord in enemies:
        enemies.remove(coord)
    else:
        enemies.append(coord)

def move_player():
    coord = (cursor.x, cursor.y)
    player = coord
    return player

def move_finish(player, current):
    coord = (cursor.x, cursor.y)
    if coord != player:
        finish = coord
    else:
        finish = current
    return finish

def draw_player(canvas, coord):
    pygame.draw.rect(canvas, GREEN, (coord[0]*(cell_width), coord[1]*(cell_width), cell_width, cell_width))

def draw_finish(canvas, coord):
    pygame.draw.rect(canvas, BLUE, (coord[0]*(cell_width), coord[1]*(cell_width), cell_width, cell_width))

def draw_enemies(canvas, coords):
    for coord in coords:
        pygame.draw.rect(canvas, RED, (coord[0]*cell_width, coord[1]*cell_width, cell_width, cell_width))

def save_maze(player, maze, finish, enemies):
    name = input("Enter Maze Name:")
    height = int(input("Enter Maze Height: "))
    width = int(input("Enter Maze Width: "))
    
    cwd = os.getcwd()
    filename = os.path.join(cwd, f"{name}.json")
    conf = "y"
    if os.path.isfile(filename):
        conf = input("This file already exists! Overwrite? (y/n) ").lower()[0]

    if conf == "y":
        outputMaze = []
        for rowInd in range(height):
            row = maze[rowInd][:width]
            outputMaze.append(row)
        
        maze_data = {
            "height": height,
            "width": width,
            "player": player,
            "finish": finish,
            "enemies": enemies,
            "maze": outputMaze
        }

        with open(filename, "w") as maze_file:
            json.dump(maze_data,maze_file)
        
        print("Successfully Saved!")
    else:
        print("Saving Aborted!")

exit = False
cursor = Cursor((0,0), ORANGE)

while not exit:
    window.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cursor.move((-1,0))
            elif event.key == pygame.K_RIGHT:
                cursor.move((1,0))
            elif event.key == pygame.K_UP:
                cursor.move((0,-1))
            elif event.key == pygame.K_DOWN:
                cursor.move((0,1))
            elif event.key == pygame.K_a:
                toggle_wall((-1,0))
            elif event.key == pygame.K_d:
                toggle_wall((1,0))
            elif event.key == pygame.K_w:
                toggle_wall((0,-1))
            elif event.key == pygame.K_s:
                toggle_wall((0,1))
            elif event.key == pygame.K_e:
                toggle_enemy()
            elif event.key == pygame.K_f:
                finish = move_finish(player, finish)
            elif event.key == pygame.K_p:
                player = move_player()
            elif event.key == pygame.K_ESCAPE:
                save_maze(player, maze, finish, enemies)
    
    draw_enemies(window, enemies)
    draw_finish(window, finish)
    draw_player(window, player)
    cursor.draw(window)
    draw_maze(window, maze)
    pygame.display.update()