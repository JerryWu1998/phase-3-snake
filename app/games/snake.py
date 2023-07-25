from pytimedinput import timedInput
from random import randint
from colorama import Fore, init
import pygame
import os

score = 0

def print_field():
    for cell in CELLS:
        if cell in snake_body:
            print(Fore.GREEN + "X", end="")
        elif cell == apple_pos:
            print(Fore.RED + "a", end="")
        elif cell[1] in (0, FIELD_HEIGHT - 1) or cell[0] in (0, FIELD_WIDTH - 1):
            print("#", end="")
        else:
            print(" ", end="")

        if cell[0] == FIELD_WIDTH - 1:
            print("")


def update_snake():
    global eaten
    new_head = snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]
    snake_body.insert(0, new_head)
    if not eaten:
        snake_body.pop(-1)
    eaten = False


def apple_collision():
    global apple_pos, eaten, score

    if snake_body[0] == apple_pos:
        apple_pos = place_apple()
        eaten = True
        score += 1
        pygame.mixer.Sound('app/mp3/coin-collect-retro-8-bit-sound-effect-145251.mp3').play()


def place_apple():
    col = randint(1, FIELD_WIDTH - 2)
    row = randint(1, FIELD_HEIGHT - 2)
    while (col, row) in snake_body:
        col = randint(1, FIELD_WIDTH - 2)
        row = randint(1, FIELD_HEIGHT - 2)
    return (col, row)

def print_title():
    print('''
  ██████  ███▄    █  ▄▄▄       ██ ▄█▀▓█████ 
▒██    ▒  ██ ▀█   █ ▒████▄     ██▄█▒ ▓█   ▀ 
░ ▓██▄   ▓██  ▀█ ██▒▒██  ▀█▄  ▓███▄░ ▒███   
  ▒   ██▒▓██▒  ▐▌██▒░██▄▄▄▄██ ▓██ █▄ ▒▓█  ▄ 
▒██████▒▒▒██░   ▓██░ ▓█   ▓██▒▒██▒ █▄░▒████▒
▒ ▒▓▒ ▒ ░░ ▒░   ▒ ▒  ▒▒   ▓▒█░▒ ▒▒ ▓▒░░ ▒░ ░
░ ░▒  ░ ░░ ░░   ░ ▒░  ▒   ▒▒ ░░ ░▒ ▒░ ░ ░  ░
░  ░  ░     ░   ░ ░   ░   ▒   ░ ░░ ░    ░   
      ░           ░       ░  ░░  ░      ░  ░
    ''')

def play():
    init(autoreset=True)
    pygame.mixer.init()

    # settings
    global FIELD_WIDTH, FIELD_HEIGHT, CELLS, snake_body, DIRECTIONS, direction, eaten, apple_pos, score
    FIELD_WIDTH = 32
    FIELD_HEIGHT = 16
    CELLS = [(col, row) for row in range(FIELD_HEIGHT) for col in range(FIELD_WIDTH)]

    # snake
    snake_body = [
        (5, FIELD_HEIGHT // 2),
        (4, FIELD_HEIGHT // 2),
        (3, FIELD_HEIGHT // 2),
    ]
    DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}
    OPPOSITE_DIRECTIONS = {"left": "right", "right": "left", "up": "down", "down": "up"}
    direction = DIRECTIONS["right"]
    eaten = False
    apple_pos = place_apple()
    # initialize score
    score = 0

    while True:
        # clear field
        os.system("clear")

        # print title
        print_title()

        # draw field
        print_field()

        # get input
        txt, _ = timedInput("", timeout=0.2)
        if txt == "w" and direction != DIRECTIONS[OPPOSITE_DIRECTIONS["up"]]:
            direction = DIRECTIONS["up"]
        elif txt == "a" and direction != DIRECTIONS[OPPOSITE_DIRECTIONS["left"]]:
            direction = DIRECTIONS["left"]
        elif txt == "s" and direction != DIRECTIONS[OPPOSITE_DIRECTIONS["down"]]:
            direction = DIRECTIONS["down"]
        elif txt == "d" and direction != DIRECTIONS[OPPOSITE_DIRECTIONS["right"]]:
            direction = DIRECTIONS["right"]
        elif txt == "q":
            return False

        # update game
        update_snake()
        apple_collision()

        # check death
        if (
            snake_body[0][1] in (0, FIELD_HEIGHT - 1)
            or snake_body[0][0] in (0, FIELD_WIDTH - 1)
            or snake_body[0] in snake_body[1:]
        ):
            while True:
                pygame.mixer.Sound('app/mp3/8-bit-video-game-fail-version-2-145478.mp3').play()
                print("Game Over. Your score was: ", score)
                choice = input("Do you want to play again? (y/n): ")
                if choice.lower() == 'y':
                    return score, True
                elif choice.lower() == 'n':
                    return score, False
                else:
                    print("Invalid choice. Please enter y/n.")