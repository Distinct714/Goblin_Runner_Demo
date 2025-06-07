
# PYGAME INTRODUCTION

# Pygame is a free and open-source cross-platform library for the development of multimedia applications like video games using Python. 
# It uses the Simple DirectMedia Layer library and several other popular libraries to abstract the most common functions, 
# making writing these programs a more intuitive task.
# It is a powerful library for game development, offering a wide range of features to simplify your coding journey.


# Graphic
# - With pygame, creating dynamic and engaging graphics has never been easier. 
# - The library provides simple yet effective tools for 2D graphics and animation, including support for images, rectangles, and polygon shapes. 
# - Whether you're a seasoned game developer or just starting out, pygame has you covered.

# Sound
# - Pygame also includes support for playing and manipulating sound and music, making it easy to add sound effects 
#   and background music to your games. 
# - With support for WAV, MP3, and OGG file formats, you have plenty of options to choose from.

# Input 
# - Pygame provides intuitive functions for handling keyboard, mouse, and joystick input, allowing you to quickly and 
#   easily implement player controls in your games. 
# - No more struggling with complex input code, pygame makes it simple.

# Game Development 
# - Lastly, pygame provides a comprehensive suite of tools and features specifically designed for game development. 
# - From collision detection to sprite management, pygame has everything you need to create exciting and engaging games. 
# - Whether you're building a platformer, puzzle game, or anything in between, pygame has you covered.

import pygame

# init() is a function used to initialize pygame to access all code methods and other stuff inside the module.
# Don't forget to add this first whenever creating a game in pygame.
pygame.init()

# display is a module used to control the display window and screen.

# set_mode is a function used to define the dimensions of screen object(width, height). (Double parenthesis is a must)
screen = pygame.display.set_mode((400, 400))

# set_caption is a function used to set the caption or title of the window. (At the window tab)
pygame.display.set_caption('PAIMON IS FLYING!') 


# set_icon is used to change the system image for the display window.
icon = pygame.image.load("C:/Users/Joshua/OneDrive/Documents/Programming Languages/PYTHON/LESSONS/(11) Pygame/cryo.ico")
pygame.display.set_icon(icon)


# flip() is a function used to update the full display surface to the screen. (Like Image Input)
# Without this, the screen will be blank.
pygame.display.flip() 


# Setting up Player Image and its coordinates
player_image = pygame.image.load("C:/Users/Joshua/OneDrive/Documents/Programming Languages/PYTHON/LESSONS/(11) Pygame/paimon.bmp")
x, y = -200, 200


# blit (means draw) is a method which is basically drawing an image of a player to screen. The screen is known as the surface of the game.
# Inside this method, it requires the parameter which is player image and it coordinates.
def player(x, y):
    screen.blit(player_image, (x, y))


# Setting up the variables to keep pygame loop running.
running = True

# Looping through all event
while running:

    # get is a function used to get all the events inside of pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Event is anything that is happening inside the pygame or game window.

    # Quit Event refers to pressing the close button in pygame.
    # QUIT is used to check for quit event.

    # Define the background colour using RGB color coding. Fill the background colour to the screen.
    # Any background color, image, etc. must be inside the loop.
    background_colour = (76, 168, 168) 
    screen.fill(background_colour) 
    

    # This coodinates allow the inserted image to move based on the assigned x and y.
    x += 0.03
    y -= 0.02

    player(x, y)
    pygame.display.update() 

#

# display.flip() will update the contents of the entire display.

# display.update() allows to update a portion of the screen, instead of the entire area of the screen. 
# If no argument is passed, it updates the entire Surface area like pygame.

# To tell PyGame which portions of the screen it should update (i.e. draw on your monitor) 
# you can pass a single pygame.Rect object, or a sequence of them to the display.update() function. 
# A Rect in PyGame stores a width and a height as well as a x- and y-coordinate for the position.

# Due to the fact that display.update() only updates certain portions of the whole screen in comparison to display.flip(), 
# display.update() is faster in most cases.