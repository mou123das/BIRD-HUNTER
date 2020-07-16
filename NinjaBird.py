import pygame
from pygame import mixer
import math
import random
import sys
import time

# initialize all imported pygame modules
pygame.init()

# List of Directions
a = ["1. To control the Ninja use the arrow keys (left and right).",
     "2. To throw stones at the birds use the spacebar.",
     "3. To pause the game enter P.",
     "4. You will lose the game if atleast one of the birds crosses,",
     "    the red line."
    ]


# create the screen
screen = pygame.display.set_mode((800, 600))

# Defining the pygame clock
clock = pygame.time.Clock()

# Background Images
main_background = pygame.image.load('BACKGROUND.jpg').convert()
help_background = pygame.image.load('HELP BACK.jpg').convert()


# SoundS
mixer.music.load("BACKGROUND MUSIC.mp3")
mixer.music.play(-1)
pop = mixer.Sound("POP.wav")  # Playing a sound


# Setting the Caption and Icon
pygame.display.set_caption("Bird Hunter")
Ninja_icon = pygame.image.load('NINJA ICON.png')
pygame.display.set_icon(Ninja_icon)

RockImg = pygame.image.load('ROCK.png')  # Loading the image of the Rock

score_count = 0  # initial score count

Rock_visibility = False  # to use this variable as global one

#List of colors
black = (0, 0, 0)
white = (255, 255, 255)

dark_red = (255, 0, 0)
light_red = (255,51,51)

dark_green = (0, 255, 0)
light_green = (75,206,42)

dark_violet=(153,0,153)
light_violet=(255,51,255)

dark_brown=(204,102,0)
light_brown=(255,153,51)

grey=(139,126,126)

name=""  # To store name of the user

f=0  # acting as a check variable, to check certain conditions



def show_button(text, inside_box_color, outside_box_color, x, y, w, h):

    mouse = pygame.mouse.get_pos()  # to get the x,y position of the mouse
    click = pygame.mouse.get_pressed()  # gets the state of the three buttons of the mouse

    boundary = pygame.draw.rect(screen, outside_box_color, (x, y, w, h))

    if boundary.collidepoint(mouse):  # if the mouse pointer is within the specified box

        pygame.draw.rect(screen, inside_box_color, (x, y, w, h))  # drawing the box with inside_box_color

        if click[0] == 1:  # if the left button is pressed

            if (text == "BACK"):
                intro_menu()

            elif (text == "PLAY" or text == "PLAY AGAIN"):
                gameloop()

            elif (text == "RESUME"):
                pygame.mixer.music.unpause()  # resuming the music
                return -1

            elif (text == "QUIT"):
                sys.exit(0)

            elif (text == "HELP?"):
                Help()

    else:   # if the mouse pointer is not within the specified box

        pygame.draw.rect(screen, outside_box_color, (x, y, w, h))  # drawing the box with outside_box_color

    # displaying the text inside the box

    show_button_font = pygame.font.Font('SNAP.ttf', 20)
    show_button_text_surface = show_button_font.render(text, True, (0, 0, 0))
    textRect = show_button_text_surface.get_rect()
    textRect.center = ((x + w / 2), (y + h / 2))
    screen.blit(show_button_text_surface, (textRect[0], textRect[1]))



def display_score(x,y,font_size,color):

    score_font = pygame.font.Font('SNAP.TTF', font_size)  # Setting Properties of Score font
    score = score_font.render("SCORE: " + str(score_count), True, color)
    screen.blit(score, (x,y))  # Displaying the score



def game_over():

    if name!="":
      t=name+", thanks for playing!"
    else:
      t = "Thanks for playing!"

    sm_font = pygame.font.Font('GOUDOSB.TTF', 40)
    sm_text = sm_font.render(t, True, dark_red)

    game_over_font = pygame.font.Font('SNAP.TTF', 80)  # Setting Properties of Game over font
    over_score = game_over_font.render("GAME OVER", True, black)

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # If user wants to end the game
                sys.exit(0)

        # Background Image
        screen.blit(main_background, (0, 0))

        screen.blit(over_score, (100, 150))  # Displaying the Game Over text
        screen.blit(sm_text, (140, 280))  # Displaying the message
        display_score(270,350,45,black)  # Displaying the final score

        # Displaying the required buttons
        show_button("PLAY AGAIN", light_violet,dark_violet, 200, 450, 175, 50)
        show_button("QUIT", light_red,dark_red, 475, 450, 100, 50, )

        pygame.display.update()
        clock.tick(15)



def throw_Rock(x, y):

    global Rock_visibility  # Defining the variable as Global so that it can be modified inside a function and not be treated as a local variable
    Rock_visibility = True  # Now the Rock can be seen on the screen
    screen.blit(RockImg, (x + 25, y + 6))  # Displaying the Rock



def has_Collision_Ocurred(BirdX, BirdY, RockX, RockY):

    distance = math.sqrt(math.pow(BirdX - RockX, 2) + (math.pow(BirdY - RockY, 2)))  # calculating the distance between specific bird and the rock

    if distance < 34:  # if distance is less than 34 return True else False
        return True
    else:
        return False



def pause():

    pygame.mixer.music.pause()  # Pauisng the music

    Pause_font = pygame.font.Font('SNAP.TTF', 140)
    Pause_text = Pause_font.render("Paused", True, (0, 0, 0))

    while True:

        for event in pygame.event.get():  # If user wants to end the game

            if event.type == pygame.QUIT:
                sys.exit(0)

        # Background Image
        screen.blit(main_background, (0, 0))

        screen.blit(Pause_text, (120, 150))

        # Displaying the required button
        r = show_button("RESUME", light_violet, dark_violet, 150, 400, 120, 50)

        if (r == -1):  # if user wants to resume
            break # break the current loop and return to the game

        # Displaying the required button
        show_button("QUIT", light_red,dark_red, 550, 400, 100, 50)

        pygame.display.update()
        clock.tick(15)



def Help():

    help_font = pygame.font.Font('GOUDOSB.TTF', 25)
    t="All the best "+name+"!!"

    dir_font = pygame.font.Font('algerian.TTF', 78)
    dir_text = dir_font.render("DIRECTIONS", True, (0, 0, 0))
    d=dir_text.get_rect()

    while True:

        posY = 150 # each time setting the initial height

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # If user wants to end the game
                sys.exit(0)

        # Background Image
        screen.blit(help_background, (0, 0))

        screen.blit(dir_text, (200,30))
        pygame.draw.line(screen, black, (200,120), ((200+d.w),120), 5)

        for x in a:  # looping through the directions list
            text = help_font.render(x, True, (0, 0, 0))
            screen.blit(text, (100, posY))
            posY = posY + 50

        text = help_font.render(t, True, (255, 0, 0))
        screen.blit(text, (180, posY+20))

        # Displaying the required button
        show_button("BACK", light_brown, dark_brown,340, 520, 100, 50)

        pygame.display.update()
        clock.tick(15)



def intro_menu():

    playX = -100
    helpX = 810
    quitX = -100

    global name
    global f

    title_font = pygame.font.Font('algerian.TTF', 115)
    title_text = title_font.render("Bird Hunter", True, black)

    enter_font = pygame.font.Font('GOUDOSB.TTF', 35)
    enter_text = enter_font.render("ENTER YOUR NAME", True, black)

    sm_font = pygame.font.Font('GOUDOSB.TTF', 20)
    sm_text = sm_font.render("Limit of length of the name exceeded!", True, dark_red)

    name_font = pygame.font.Font('GOUDOSB.TTF', 30)
    k=0
    m=0

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # If user wants to end the game
                sys.exit(0)

            if event.type==pygame.KEYDOWN and f==0:  # continue to accept the keydown events untill a name has been entered

                if event.key==13:  # if enter is pressed
                    f=1  # setting the counter as one denoting the name has been entered

                if m==1 and event.key!=pygame.K_BACKSPACE and f==0:  # if limit of the name exceeds
                    pop.play()  # play a pop sound

                if event.key==pygame.K_BACKSPACE and len(name)!=0 and f==0:  # when backspace is entered
                    name=name[0:(len(name)-1)]
                    m=0

                if event.key!=pygame.K_BACKSPACE and f==0:

                    if rect.w < 390:  # if entered name is within the box
                      name+=event.unicode
                      m=0

                    else:
                      m=1


        k=k+1 # recording each frame


        # Background Image
        screen.blit(main_background, (0, 0))
        screen.blit(title_text, (50, 100))  # Displaying the Game Over text

        name_text = name_font.render(name, True, (0, 0, 0))
        rect=name_text.get_rect()

        if f==0:  # if the name has not been completely entered

            pygame.draw.rect(screen, black, (102, 360, 460, 50), 3)  # drawing the outer box
            screen.blit(enter_text, (100, 300))


            screen.blit(name_text, (110, 369)) # and the name

            if m==1:  # warning text
              screen.blit(sm_text, (102, 420))

            if k%2!=0: # alternate times blinking the cursor

                if len(name) == 0:
                   pygame.draw.line(screen, grey, (109,365), (109,405), 3)
                else:
                   pygame.draw.line(screen, grey, (110+rect.w + 2, 365), (110+rect.w + 2, 405), 3)

            clock.tick(6)
            

        if f==1:  # if the name has been completely entered

            # animating the buttons
            if playX < 348 and helpX > 348 and quitX < 348:
        
                playX += 8
                helpX -= 8
                quitX += 8

                show_button("PLAY", light_green, dark_green, playX, 300, 100, 50)
                show_button("HELP?", light_violet, dark_violet, helpX, 380, 100, 50)
                show_button("QUIT", light_red, dark_red, quitX, 460, 100, 50)
        
        
            else:
                show_button("PLAY", light_green, dark_green, 348, 300, 100, 50)
                show_button("HELP?", light_violet, dark_violet, 348, 380, 100, 50)
                show_button("QUIT", light_red, dark_red, 348, 460, 100, 50)
                clock.tick(15)

        pygame.display.update()



def loading():

    load_font = pygame.font.Font('algerian.TTF', 60)

    l="Loading"  # Initial "Loading" text

    width=0  # Initial width of loading bar

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # If user wants to end the game
                sys.exit(0)

        screen.fill(black)

        pygame.draw.rect(screen, white, (160, 280, 463, 50), 3)  # outer rectangle

        if width<468:
          pygame.draw.rect(screen, dark_red, (162, 282, width, 46))  # loading bar

        else:
            time.sleep(1.2)
            intro_menu()

        width+=20  # increasing the loading bar width

        if len(l)==12:
            l="Loading"

        load_text = load_font.render(l, True, white)
        screen.blit(load_text, (260,200))

        l += "."

        pygame.display.update()
        clock.tick(6)



def gameloop():

    global score_count
    score_count = 0  # Initialising the initial score count as zero

    # Setting the Ninja/Player properties

    NinjaImg = pygame.image.load('NINJA.png')  # Loading the image of Ninja
    NinjaX = 370  # X coordinate of the Image
    NinjaY = 480  # Y coordinate of the Image
    NinjaX_speed = 0  # Declaring the rate at which the Ninja will move


    # Setting the Bird properties
    # Here we are working with 7 Birds and so the properties are defined using lists

    BirdImg1 = pygame.image.load('BIRD.png')
    BirdImg = []  # List containing each bird's image
    BirdX = []  # List containing the X coordinates of the Images of the birds
    BirdY = []  # List containing the X coordinates of the Images of the birds
    BirdX_speed = []  # List containing the rates at which birds would move in +X or -X direction
    BirdY_speed = []  # List containing the rates at which birds would move in +Y direction
    num_of_birds = 7  # The number of birds


    # Initial initialisation of the properties of the birds

    for i in range(num_of_birds):
        BirdImg.append(BirdImg1)
        BirdX.append(random.randint(0, 736))  # Randomly generating the X coordinates of each bird
        BirdY.append(random.randint(10, 100))  # Randomly generating the Y coordinates of each bird
        BirdX_speed.append(1)
        BirdY_speed.append(60)


    # Setting the Rock Properties

    # RockImg = pygame.image.load('ROCK.png')  # Loading the image of the Rock
    RockX = 0  # X coordinate of the Rock
    RockY = 480  # Y coordinate of the Rock
    RockY_speed = 5  # # Declaring the rate at which the Ninja will move
    global Rock_visibility
    Rock_visibility = False
    # False - You can't see the Rock on the screen
    # True - The Rock is currently moving
    # The Rock_visibility variable's value will help us to contol the state of the Rock


    while True:

        # Background Image
        screen.blit(main_background, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # If user wants to end the game
                sys.exit(0)

            if event.type == pygame.KEYDOWN:  # If any Key is pressed

                if event.key == pygame.K_p: # If the pressed key is p
                    pause()  # calling the pause function

                if event.key == pygame.K_RIGHT:  # If the pressed key is Right
                    NinjaX_speed = 3  # the ninja would be move in the right direction

                if event.key == pygame.K_LEFT:  # If the pressed key is Left
                    NinjaX_speed = -3  # the ninja would be move in the left direction

                if event.key == pygame.K_SPACE:  # If the pressed key is Space bar

                    if Rock_visibility == False:  # If the rock is not previously thrown
                        RockX = NinjaX  # Get the current X coordinate of the Ninja
                        # Only when the space bar is pressed we will hold that initial X coordinate of the Ninja
                        # So that when the game continues and the key is released the rock doesn't follow the direction of the Ninja
                        throw_Rock(RockX, RockY)  # Throwing the Rock

            if event.type == pygame.KEYUP:  # If any key is released
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # If right or left key
                    NinjaX_speed = 0  # The Ninja speed is made  zero so that the ninja will only move when the key is pressed

        NinjaX += NinjaX_speed  # Moving the Ninja

        pygame.draw.line(screen, dark_violet, (0, 440), (800, 440), 3)

        #  If the Ninja reaches either the left or right boundary keep it there
        if NinjaX <= 0:
            NinjaX = 0
        elif NinjaX >= 705:
            NinjaX = 705


        screen.blit(NinjaImg, (NinjaX, NinjaY))  # Displaying the Ninja

        # Bird Movement
        # Iterating through all the birds
        for i in range(num_of_birds):

            # Game Over
            if BirdY[i] > 390:  # If any of the birds crosses the violet line
                game_over()  # Call game_over() menu

            BirdX[i] += BirdX_speed[i]  # Moving the Birds

            if BirdX[i] <= 0:  # if any of the birds reach the left boundary
                BirdX_speed[i] = 1  # now we will move it towards right
                BirdY[i] += BirdY_speed[i]  # and lower it down by BirdY_speed value

            elif BirdX[i] >= 736:  # if any of the birds reach the right boundary
                BirdX_speed[i] = -1  # now we will move it towards left
                BirdY[i] += BirdY_speed[i]  # and lower it down by BirdY_speed value

            # Checking if any of the birds collided with the rock or not
            collision = has_Collision_Ocurred(BirdX[i], BirdY[i], RockX, RockY)

            if collision == True:  # If a collision has occured

                pop.play()  # Playing pop sound
                RockY = 480  # again bring it back to its original height
                Rock_visibility = False  # make its visibility false
                BirdX[i] = random.randint(0, 736)  # Randomly generating the X coordinates of that particular bird
                BirdY[i] = random.randint(10, 100)  # Randomly generating the Y coordinates of that  particular bird
                score_count += 1  # Increment the score by 1

            screen.blit(BirdImg[i], (BirdX[i], BirdY[i]))  # Displaying the birds

        # Rock Movement

        if RockY <= 0:  # if the rock has been thrown away from the screen
            RockY = 480  # bring back to its original height
            Rock_visibility = False  # make its visibility false


        if Rock_visibility == True:  # if the visibility is true
            throw_Rock(RockX, RockY)  # throw the rock
            RockY -= RockY_speed  # continue to move it upwards

        display_score(10,10,20,black)  # keep displaying the score

        pygame.display.update()  # Update portions of the screen for software displays



loading()  # Calling the initial function to run the game

