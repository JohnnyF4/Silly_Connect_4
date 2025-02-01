# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Libby Signor
#               Samuel Caridad Romero
#               Johnny Figueroa
#               Brooke Noble
# Section:      522
# Assignment:   Fun Game
# Date:         December 7 2022
import turtle
import numpy as np
import time as te
import pygame
import sys
import math


# functions that help setup the game
def board():
    """returns the game board as an array"""
    setup = np.zeros((6, 7))
    return setup


def return_board(start):
    """Flips the board around so that the pieces place correctly"""
    setup_flip = np.flip(start, 0)
    return setup_flip


def move_piece(start, row, Move, piece):
    """Replaces an empty slot with a piece"""
    start[row][Move] = piece


def location(start, Move):
    """Checks to see if a row is filled after a piece is placed"""
    return start[5][Move] == 0


def next_row(start, Move):
    """"Function that places the next piece in the next available row"""
    for i in range(6):
        if start[i][Move] == 0:
            return i


def win_condition(start, row, Move):
    """After piece is placed checks to see if there are four consecutive pieces(vertical,horizontal, diagonal)"""
    item = start[row][Move]
    rows = len(start)
    column = len(start[0])
    if item == 0:
        return False
    for other_r, other_c in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        consecutive_item = 1
        for i in (1, -1):
            other_r *= i
            other_c *= i
            next_row = row + other_r
            next_col = Move + other_c
            while rows > next_row >= 0 and column > next_col >= 0:
                if start[next_row][next_col] == item:
                    consecutive_item += 1
                else:
                    break
                if consecutive_item == 4:
                    return True
                next_row += other_r
                next_col += other_c
    return False

def draw(start):
    """Draws the board using pygame package and the pieces for both players"""
    for i in range(7):
        for j in range(6):
            pygame.draw.rect(screen, (40,69,167), (i*squares, j*squares+squares, squares, squares))
            pygame.draw.circle(screen,(255,255,255),(int(i*squares+squares/2), int(j*squares+squares+squares/2)), int(squares/2-5))
    for i in range(7):
        for j in range(6):
            if start[j][i] == 1:
                pygame.draw.circle(screen,(255,0,0),(int(i*squares+squares/2), height-int(j*squares+squares/2)), int(squares/2-5))
            elif start[j][i] == 2:
                pygame.draw.circle(screen,(255,255,0),(int(i*squares+squares/2), height-int(j*squares+squares/2)), int(squares/2-5))
    pygame.display.update()

###Code the actual game
start = board()
return_board(start)
turn_player = 0

pygame.init()
squares = 100 #varible meant to help adjust the different size of the board
width = 7 * squares #width of board
height = 7 * squares #height of board
size = (width, height)
screen = pygame.display.set_mode(size) #variable for pygame board

font = pygame.font.SysFont("arial", 65)

#reads a file called connect4
file = open('connect4.txt', 'r')
line = file.readline()
line1 = file.readline()
line2 = file.readline()
file.close()

print("Welcome to connect 4")

while True:
    try:
        options = input("What would you like to do?(instructions, play, exit): ")
        break
    except:
        print("Sorry can't do that")
        options = input("What would you like to do?(instructions, play, exit): ")

while True:
    if options == "play":
        print("The game has opened, use the pygame window to play.Enjoy!")
        play = True
        break
    elif options == "exit":
        play = False
        break
    elif options == "instructions":
        inst = open("instructions.txt", "r")
        for l in inst:
            print(l)
        inst.close()
        options = input("What would you like to do? (play, exit): ")
    else:
        print("Sorry can't do that")
        options = input("What would you like to do?(instructions, play, exit): ")


while play == True:
    draw(start)
    pygame.display.update()
    #closes the game if you close the window
    for stuff in pygame.event.get():
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, width, squares))
        if stuff.type == pygame.QUIT:
            sys.exit()

    #draw the piece moving as you move around the board
        if stuff.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,(255,255,255),(0,0,width,squares))
            xpos = stuff.pos[0]
            if turn_player == 0:
                pygame.draw.circle(screen,(255,0,0),(xpos, int(squares/2)),int(squares/2-5))
            else:
                pygame.draw.circle(screen,(255,255,0),(xpos, int(squares/2)),int(squares/2-5))

        pygame.display.update()


    #Let the player palce their piece on the proper column / row
        if stuff.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,(255,255,255),(0,0,width,squares))
            #player 1 stuff
            if turn_player == 0:
                xpos = stuff.pos[0]
                Move = int(math.floor(xpos/squares))
                if location(start, Move):
                    row = next_row(start, Move)
                    piece = move_piece(start, row, Move, 1)
                #end the game when player 1  wins
                if win_condition(start, row, Move):
                    vic_display = font.render(line1[0:-1], 1, (255, 0, 0))
                    screen.blit(vic_display, (105, 10))
                    play = False
            #player 2 stuff
            else:
                xpos = stuff.pos[0]
                Move = int(math.floor(xpos / squares))
                if location(start, Move):
                    row = next_row(start, Move)
                    piece = move_piece(start, row, Move, 2)
                #end the game when player 2 wins
                if win_condition(start, row, Move):
                    vic_display = font.render(line2 ,1,(255,255,0))
                    screen.blit(vic_display,(105,10))
                    play = False

            return_board(start)
            draw(start)
            turn_player += 1
            turn_player = turn_player % 2
            #delay before the game closes
            if play == False:
                # turtle graphics to print final message
                te.sleep(2)
                t = turtle.Turtle()
                t.hideturtle()
                turtle.Screen().bgpic("anya.gif")
                t.write("Thanks for playing!", align="center", font=("cooper black", 25, "normal"))


                pygame.time.wait(2000)



