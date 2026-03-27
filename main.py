import pygame
import os
import json

pygame.init()

maze_size = 100 #maximum maze size. All 100 cells displayed but don't all have to be used.
cell_width = 8
pygame.display.set_caption("Maze Creator")
window = pygame.display.set_mode((cell_width*maze_size, cell_width*maze_size))

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255,0,0)
ORANGE = (255, 204, 0)
YELLOW = (255,255,0)
BLUE = (51, 102, 255)

maze = [[[False, False, False, False] for i in range(maze_size)] for j in range(maze_size)] #maze initialised as 2D array of cell lists with no walls.
enemies = []
collectibles = []
player = (0,0)
finish = (99,99)

class Cursor: #user moves cursor to edit cells.
    def __init__(self, start_pos, colour):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.col = colour

    def move(self, move): #move cursor in the given direction
        if move == (-1, 0) and self.x != 0:
            self.x -= 1
        elif move == (1, 0) and self.x != maze_size-1:
            self.x += 1
        elif move == (0, -1) and self.y != 0:
            self.y -= 1
        elif move == (0, 1) and self.y != maze_size-1:
            self.y += 1
        
    def draw(self, canvas): #draw the cursor.
        pygame.draw.rect(canvas, self.col, (self.x*(cell_width), self.y*(cell_width), cell_width, cell_width))

def draw_maze(canvas, maze): #draw all of the walls for the maze.
    for rowInd in range(len(maze)):
        for colInd in range(len(maze[rowInd])): #iterate through all Cells.
            if maze[rowInd][colInd][0]: #if left wall is True, draw it.
                pygame.draw.rect(canvas, BLACK, (colInd*cell_width, rowInd*cell_width, 1, cell_width))
            if maze[rowInd][colInd][1]: #if top wall is True, draw it.
                pygame.draw.rect(canvas, BLACK, (colInd*cell_width, rowInd*cell_width, cell_width, 1))
            if maze[rowInd][colInd][2]: #if right wall is True, draw it.
                pygame.draw.rect(canvas, BLACK, (colInd*cell_width+cell_width-1, rowInd*cell_width, 1, cell_width))
            if maze[rowInd][colInd][3]: #if bottom wall is True, draw it.
                pygame.draw.rect(canvas, BLACK, (colInd*cell_width, rowInd*cell_width+cell_width-1, cell_width, 1))

def toggle_wall(dir): #if there is a wall in the direction given, get rid of it. Otherwise, place one.
    row, col = cursor.y, cursor.x
    match dir:
        case (-1,0):
            maze[row][col][0] = not maze[row][col][0] #toggle this cell's left wall.
            if col != 0:
                maze[row][col-1][2] = not maze[row][col-1][2] #if not the leftmost cell, toggle left neighbour's right wall.
        case (1,0):
            maze[row][col][2] = not maze[row][col][2] #toggle this cell's right wall.
            if col != maze_size-1:
                maze[row][col+1][0] = not maze[row][col+1][0] #if not the rightmost cell, toggle right neighbour's left wall.
        case (0,-1):
            maze[row][col][1] = not maze[row][col][1] #toggle this cell's top wall.
            if row != 0:
                maze[row-1][col][3] = not maze[row-1][col][3] #if not the topmost cell, toggle above neighbour's bottom wall.
        case (0,1):
            maze[row][col][3] = not maze[row][col][3] #toggle this cell's bottom wall.
            if row != maze_size-1:
                maze[row+1][col][1] = not maze[row+1][col][1] #if not the bottommost cell, toggle lower neighbour's top wall.

def toggle_enemy(): #place/remove an enemy in the current cell.
    coord = (cursor.x, cursor.y)
    if coord in enemies:
        enemies.remove(coord)
    else:
        enemies.append(coord)

def toggle_collectible(): #place/remove a collectible in the current cell.
    coord = (cursor.x, cursor.y)
    if coord in collectibles:
        collectibles.remove(coord)
    else:
        collectibles.append(coord)

def move_player(): #move player's start position to the cursor's position.
    coord = (cursor.x, cursor.y)
    player = coord
    return player

def move_finish(player, current): #if the cursor's position isn't the same as the player's, move the finish cell to the cursor's position.
    coord = (cursor.x, cursor.y)
    if coord != player:
        finish = coord
    else:
        finish = current
    return finish

def draw_player(canvas, coord): #draw player
    pygame.draw.rect(canvas, GREEN, (coord[0]*(cell_width), coord[1]*(cell_width), cell_width, cell_width))

def draw_finish(canvas, coord): #draw finish cell
    pygame.draw.rect(canvas, BLUE, (coord[0]*(cell_width), coord[1]*(cell_width), cell_width, cell_width))

def draw_enemies(canvas, coords): #iterate through all enemies and draw them.
    for coord in coords:
        pygame.draw.rect(canvas, RED, (coord[0]*cell_width, coord[1]*cell_width, cell_width, cell_width))

def draw_collectibles(canvas, coords): #iterate through all collectibles and draw them.
    for coord in coords:
        pygame.draw.rect(canvas, YELLOW, (coord[0]*cell_width, coord[1]*cell_width, cell_width, cell_width))

def save_maze(player, maze, finish, enemies):
    name = input("Enter Maze Name:") #get info about the created maze.
    height = int(input("Enter Maze Height: "))
    width = int(input("Enter Maze Width: "))
    
    cwd = os.getcwd()
    filename = os.path.join(cwd, f"{name}.json")
    conf = "y"
    if os.path.isfile(filename): #if file already exists, check they want to overwrite it.
        conf = input("This file already exists! Overwrite? (y/n) ").lower()[0]

    if conf == "y":
        outputMaze = []
        for rowInd in range(height): #compile all necessary cells (within the height and width given) into the maze 2D list.
            row = maze[rowInd][:width]
            outputMaze.append(row)
        
        maze_data = { #create the maze_data dictionary
            "height": height,
            "width": width,
            "player": player,
            "finish": finish,
            "enemies": enemies,
            "collectibles": collectibles,
            "maze": outputMaze
        }

        with open(filename, "w") as maze_file:
            json.dump(maze_data,maze_file) #dump the dictionary to a JSON file, ready for importing into the game.
        
        print("Successfully Saved!")
    else:
        print("Saving Aborted!")

exit = False
cursor = Cursor((0,0), ORANGE) #instantiate a cursor

while not exit:
    window.fill(WHITE) #clear screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #move cursor left
                cursor.move((-1,0))
            elif event.key == pygame.K_RIGHT: #move cursor right
                cursor.move((1,0))
            elif event.key == pygame.K_UP: #move cursor up.
                cursor.move((0,-1))
            elif event.key == pygame.K_DOWN: #move cursor down.
                cursor.move((0,1))
            elif event.key == pygame.K_a: #toggle left wall.
                toggle_wall((-1,0))
            elif event.key == pygame.K_d: #toggle right wall.
                toggle_wall((1,0))
            elif event.key == pygame.K_w: #toggle top wall.
                toggle_wall((0,-1))
            elif event.key == pygame.K_s: #toggle bottom wall.
                toggle_wall((0,1))
            elif event.key == pygame.K_e: #toggle enemy.
                toggle_enemy()
            elif event.key == pygame.K_c: #toggle collectible.
                toggle_collectible()
            elif event.key == pygame.K_f: #move finish.
                finish = move_finish(player, finish)
            elif event.key == pygame.K_p: #move player.
                player = move_player()
            elif event.key == pygame.K_ESCAPE: #exit tool by saving maze.
                save_maze(player, maze, finish, enemies)
    
    draw_collectibles(window, collectibles) #draw everything
    draw_enemies(window, enemies)
    draw_finish(window, finish)
    draw_player(window, player)
    cursor.draw(window) #cursor drawn last out of all entities so that displays above others like Player and Enemy.
    draw_maze(window, maze)
    pygame.display.update() #update the Pygame window.