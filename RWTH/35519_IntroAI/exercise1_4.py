# RWTH - Introduction to AI
# Assignment 1
# Exercise 1.4
# Author: Elouan COLYBES
# Date: 08/11/2023
# Creative Commons BY-NC-SA

# Please make sure you installed Python and all librairies on your computer.
# The program is ready to run. Enjoy clicking on the buttons! But not too fast please, you'd risk to break everything :(

import turtle
import tkinter as tk
from tkinter import messagebox
from random import random


##### Model variables setting #####

CELL_WIDTH = 40     # px cell width
N_COLUMNS = 8       # row length
N_ROWS = 6          # columns length
SPEED = 6           # turtle speed


##### Problem representation #####

GRID=[]
for i in range(N_COLUMNS):
    GRID.append([])
    for j in range(N_ROWS):
        GRID[i].append(0)
POS = [0,0]      # live position of the cleaner
DIREC = [1]      # can be 0, 1, 2, 3 for right, up, left, down


##### Create objects #####

root = tk.Tk()
canvas = tk.Canvas(master = root, width = 2*CELL_WIDTH*N_COLUMNS+20, height = 2*CELL_WIDTH*N_ROWS+20)
canvas.pack()

turtle_screen = turtle.TurtleScreen(canvas)
turtle_screen.setworldcoordinates(-20,-20,CELL_WIDTH*N_COLUMNS+20,CELL_WIDTH*N_ROWS+20)
tur = turtle.RawTurtle(turtle_screen)

##### Define useful functions #####

def teleport(i,j):
    tur.up()
    tur.setpos(i,j)
    tur.down()

def rand_pos(n=N_COLUMNS, m=N_ROWS, pos=POS, cell_width=CELL_WIDTH):
    i = int(random()*n)
    j = int(random()*m)
    teleport((i+0.5)*cell_width,(j+0.5)*cell_width)
    pos[0] = i
    pos[1] = j
    k = int(random()*4)
    for _ in range(k):
        turnLeft()

def draw_grid(n=N_COLUMNS, m=N_ROWS, cell_width=CELL_WIDTH):
    grid_width = cell_width*n
    grid_height = cell_width*m
    
    tur.width(2)
    teleport(0,0)

    for i in range(m+1):
        tur.forward(grid_width)
        teleport(0,(i+1)*cell_width)

    tur.left(90)
    teleport(0,0)

    for i in range(n+1):
        tur.forward(grid_height)
        teleport((i+1)*cell_width,0)
    
    tur.width(1)
    teleport(0,0)


def set_dust(n=N_COLUMNS, m=N_ROWS, cell_width=CELL_WIDTH, grid=GRID):
    for i in range(n):
        for j in range(m):
            if random()<=0.2:
                grid[i][j]=1
                teleport(int((i+0.75)*cell_width), int((j+0.5)*cell_width))
                tur.circle(cell_width/4)
                teleport(int((i+0.6)*cell_width), int((j+0.5)*cell_width))
                tur.circle(cell_width/10)
    teleport(0,0)

def clear_dust(n=N_COLUMNS, m=N_ROWS, cell_width=CELL_WIDTH, grid=GRID):
    messagebox.showinfo("Information", "Clearing grid will begin, please do not press any button until operation complete (wait for next message).")
    tur.speed(0)
    reset_turtle()
    tur.color("white")
    for i in range(n):
        for j in range(m):
            teleport(int((i+0.05)*cell_width), int((j+0.05)*cell_width))
            grid[i][j]=0
            tur.begin_fill()
            for _ in range(4):
                tur.forward(int(0.9*cell_width))
                tur.right(90)
            tur.end_fill()
    tur.color("black")
    tur.speed(1000)
    teleport(0,0)
    root.update_idletasks()
    messagebox._show("Information", "Cleaning done")

def one_dust(n=N_COLUMNS, m=N_ROWS, cell_width=CELL_WIDTH, grid=GRID):
    reset_turtle()
    i = int(random()*n)
    j = int(random()*m)
    grid[i][j]=1
    teleport(int((i+0.75)*cell_width), int((j+0.5)*cell_width))
    tur.circle(cell_width/4)
    teleport(int((i+0.6)*cell_width), int((j+0.5)*cell_width))
    tur.circle(cell_width/10)
    teleport(0,0)

def reset_turtle(pos=POS, direc=DIREC):
    tur.up()
    teleport(0,0)
    tur.down()
    while direc[0]!=1:
        turnLeft()
    pos[0]=0
    pos[1]=0


##### Exercise functions we are allowed to call #####

def turnLeft(direc=DIREC):
    direc[0] = (direc[0]+1)%4
    tur.left(90)

def turnRight(direc=DIREC):
    direc[0] = (direc[0]-1)%4
    tur.right(90)

def forward(cell_width=CELL_WIDTH, direc=DIREC, pos=POS):
    tur.forward(cell_width)
    if direc[0]==0:   pos[0]+=1
    elif direc[0]==1: pos[1]+=1
    elif direc[0]==2: pos[0]-=1
    elif direc[0]==3: pos[1]-=1

def sensingDirt(pos=POS, grid=GRID):
    return grid[pos[0]][pos[1]]==1

def sensingWall(pos=POS, direc=DIREC):
    i=pos[0]
    j=pos[1]
    print("(",i,",",j,") & direction",direc[0],"(0:right, 1:up, 2:left, 3:down)")
    return (i==0 and direc[0]==2) or (i==N_COLUMNS-1 and direc[0]==0) or (j==0 and direc[0]==3) or (j==N_ROWS-1 and direc[0]==1)

def suck(pos=POS, cell_width=CELL_WIDTH, grid=GRID):
    grid[pos[0]][pos[1]] = 0
    tur.color("white")
    tur.speed(0)
    tur.begin_fill()
    tur.forward(int(0.4*cell_width))
    tur.left(90)
    tur.forward(int(0.4*cell_width))
    tur.left(90)
    for _ in range(3):
        tur.forward(int(0.8*cell_width))
        tur.left(90)
    tur.forward(int(0.4*cell_width))
    tur.left(90)
    tur.forward(int(0.4*cell_width))
    tur.left(90)
    tur.left(90)
    tur.end_fill()
    tur.speed(SPEED)
    tur.color("black")

##### Now the problem algorithms #####

def algo1(cell_width=CELL_WIDTH, speed=SPEED, pos=POS):
    # Initialise the model
    if pos[0]==0 and pos[1]==0:
        teleport(int(cell_width/2),int(cell_width/2))
        turnRight()
    tur.speed(speed)
    
    # Logic implementation
    if sensingDirt():
        suck()
    for _ in range(4):
        while not(sensingWall()):
            forward()
            if sensingDirt():
                suck()
        turnLeft()
    tur.speed(0)
    reset_turtle()


def algo1bis(cell_width=CELL_WIDTH, direc=DIREC, speed=SPEED, pos=POS):
    # Initialise the model
    if pos[0]==0 and pos[1]==0:
        teleport(int(cell_width/2),int(cell_width/2))
        turnRight()
    tur.speed(speed)

    # Logic implementation
    if sensingDirt():
        suck()
    for _ in range(100):
        if not(sensingWall()):
            forward()
            if sensingDirt():
                suck()

        d = int(4*random()-0.01)   # Choose an alea direction
        while direc[0]!=d:         # And align on it
            turnLeft()
    tur.speed(0)
    reset_turtle()
        
def state_init():
    while not(sensingWall()): forward()
    turnLeft()
    while not(sensingWall()): forward()
    turnLeft()

def state_left():
    if sensingDirt():
        suck()
    while not(sensingWall()):
        forward()
        if sensingDirt():
            suck()
    turnLeft()
    if sensingWall():
        return False
    else:
        forward()
        turnLeft()
    return True

def state_right():
    if sensingDirt():
        suck()
    while not(sensingWall()):
        forward()
        if sensingDirt():
            suck()
    turnRight()
    if sensingWall():
        return False
    else:
        forward()
        if sensingDirt():
            suck()
        turnRight()
    return True

def algo2(speed=SPEED, pos=POS, cell_width=CELL_WIDTH):
    # Initialise the model
    if pos[0]==0 and pos[1]==0:
        teleport(int(cell_width/2),int(cell_width/2))
    tur.speed(speed)

    # Logic implementation
    state_init()
    t=True
    while t:
        if state_left():
            t = state_right()
        else:
            t = False
    tur.speed(0)
    reset_turtle()


##### Graphic initialisation ####

tur.speed(0)
draw_grid()
set_dust()

##### Button functionalities #####

clear_dust = tk.Button(root, text="Clear grid", command=clear_dust)
clear_dust.pack()

new_dust = tk.Button(root, text="One more dust", command=one_dust)
new_dust.pack()

algo1 = tk.Button(root, text="Use the first algorithm (border)", command=algo1)
algo1.pack()

algo1bis = tk.Button(root, text="Use the first algorithm (alea)", command=algo1bis)
algo1bis.pack()

algo2 = tk.Button(root, text="Use the second algorithm (states)", command=algo2)
algo2.pack()

alea_pos = tk.Button(root, text="Move the cleaner randomly on the grid", command=rand_pos)
alea_pos.pack()

reset = tk.Button(root, text="Reset the cleaner position", command=rand_pos)
reset.pack()

root.mainloop()
