#!/usr/bin/env python3

import curses
from curses import textpad
import random

def create_food(snake, box):
    """ Function to generate food inside the play arena """
    food = None
    while food == None:
        food = [random.randint(box[0][0]+1, box[1][0]-1),
        random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food = None
    return food

def print_score(stdscr, score):
    """ Function to print the score on top """
    h, w = stdscr.getmaxyx()
    score_text = "Score: {}".format(score)
    stdscr.addstr(1, w//2 - len(score_text)//2, score_text)


def main(stdscr):
    curses.curs_set(0) # Disable blinking cursor
    stdscr.nodelay(1) # Disable delay for getch()
    stdscr.timeout(100) # Set delay timeout

    sh, sw = stdscr.getmaxyx() # Get maximum height and width of window

    # Drawing box for the game area
    box = [[3, 3], [sh-3, sw-3]] # Setting border of 3 units
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    # Defining inital position and direction of the snake
    snake = [[sh//2, sw//2 + 1],[sh//2, sw//2],[sh//2, sw//2 - 1]]
    direction = curses.KEY_RIGHT

    # Drawing the snake
    for y, x in snake:
        stdscr.addstr(y, x, '#')

    # Drawing food
    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], '*')

    # Drawing scoreboard
    score = 0
    print_score(stdscr, score)

    # Game loop
    while 1:
        # Get direction input
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            direction = key

        # Change direction of snake movement    
        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]

        snake.insert(0, new_head)
        stdscr.addstr(new_head[0], new_head[1], "#")
        # If snake eats food, increase length and increment score
        if snake[0] == food:
            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], '*')
            score += 1
            print_score(stdscr, score)
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], " ")
            snake.pop()

        # Game over condition
        if (snake[0][0] in [box[0][0], box[1][0]] or
            snake[0][1] in [box[0][1], box[1][1]] or # Snake hits borders
            snake[0] in snake[1:]): # Snake hits itself
            msg = "GAME OVER!"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            break

        stdscr.refresh()

curses.wrapper(main)
