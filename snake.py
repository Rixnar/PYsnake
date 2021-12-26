# -------------------------------
# |                             |
# |         Assignement         |
# |            Snake            |
# |           Jan Maat          |
# |       stud.no. 2714600      |
# |          8-12-2021          |
# |     Programming in PYTHON   |
# |                             |
# -------------------------------

import snakelib

width = 0  # initialized in play_snake
height = 0  # initialized in play_snake
ui = None  # initialized in play_snake
SPEED = 1
keep_running = True
xcoord = 0
ycoord = 0
dir = "east"  # default direction
snakeposition = [[1, 0], [0, 0]]
appleposition = [0, 0]  # default position apple
apple_spot = 0 #default


def xposition(num):  # get the x position based on the number in the grid
    x = num % width
    return x


def yposition(num):  # get y position based on the number in the grid
    y = int(num / width)
    return y


def numbergrid(x, y):  # convert a pair of coordinates into a gridnumber
    num = y * width + x
    return num

def init(): #initialze the game, the start position should be gridnumbers 0 and 1 and place the apple in a free position
    global snakeposition, apple_spot
    #Place the apple on the first free position
    apple_spot = 2
    #Place a snake with length 2 on the first 2 positions
    snakeposition[0][0] = xposition(1)
    snakeposition[0][1] = yposition(1)
    snakeposition[1][0] = xposition(0)
    snakeposition[1][0] = yposition(0)
    draw()

def update_coords():
    global dir, xcoord, ycoord
    for i in range(0, len(snakeposition) - 1):
        snakeposition[i][0] = snakeposition[i + 1][0]
        snakeposition[i][1] = snakeposition[i + 1][1]
    if dir == "east":
        if xcoord >= width - 1:
            xcoord = 0
        else:
            xcoord += 1
    elif dir == "west":
        if xcoord <= 0:
            xcoord = width - 1
        else:
            xcoord -= 1
    elif dir == "north":
        if ycoord <= 0:
            ycoord = height - 1
        else:
            ycoord -= 1
    elif dir == "south":
        if ycoord >= height - 1:
            ycoord = 0
        else:
            ycoord += 1
    snakeposition[len(snakeposition) - 1][0] = xcoord
    snakeposition[len(snakeposition) - 1][1] = ycoord

def grow():
    global snakeposition, SPEED
    headposition = len(snakeposition) - 1
    if dir == "east":
        addCoord = [snakeposition[headposition][0] + 1, snakeposition[headposition][1]]
    elif dir == "west":
        addCoord = [snakeposition[headposition][0] - 1, snakeposition[headposition][1]]
    elif dir == "north":
        addCoord = [snakeposition[headposition][0], snakeposition[headposition][1] + 1]
    elif dir == "south":
        addCoord = [snakeposition[headposition][0], snakeposition[headposition][1] - 1]
    if addCoord[0] < 0:
        addCoord[0] = width - 1
    elif addCoord[0] > width - 1:
        addCoord[0] = 0
    elif addCoord[1] < 0:
        addCoord[1] = height - 1
    elif addCoord[1] > height - 1:
        addCoord[1] = 0
    snakeposition.append(addCoord)
    ui.clear_text()
    ui.print_("Level " + str(len(snakeposition) - 1) + "\n" + "Current Speed: " + str(SPEED) + "\n")
    if len(snakeposition) % 5 == 0:
        ui.print_("Well done, lets speed it up!")
        SPEED += 2

def placeApple():
    global appleposition, apple_spot
    x_available = [False for i in range(len(snakeposition))]
    y_available = [False for i in range(len(snakeposition))]
    while not any(x_available) and not any(y_available):
        x = ui.random(width)
        y = ui.random(height)
        for i in range(0, len(snakeposition) - 1):
            if snakeposition[i][0] != x:
                x_available[i] = True
            if snakeposition[i][1] != y:
                y_available[i] = True
    appleposition[0] = x
    appleposition[1] = y
    apple_spot = numbergrid(x,y)


def eat():
    global appleposition, snakeposition
    xhead = snakeposition[len(snakeposition) - 1][0]
    yhead = snakeposition[len(snakeposition) - 1][1]
    if xhead == appleposition[0] and yhead == appleposition[1]:
        placeApple()
        grow()

def collide():
    x_collide = [False for i in range(len(snakeposition) - 1)]  # snake without head
    y_collide = [False for i in range(len(snakeposition) - 1)]  # snake without head
    while not any(x_collide) and not any(y_collide):
        for i in range(0, len(snakeposition) - 1):
            if xcoord == snakeposition[i][0]:
                x_collide[i] = True
            if ycoord == snakeposition[i][1]:
                y_collide[i] = True
            if not any(x_collide) and not any(y_collide):
                pass

def draw():
    global xcoord, ycoord
    ui.clear()
    print(xposition(apple_spot), yposition(apple_spot), apple_spot)
    ui.place(xposition(apple_spot), yposition(apple_spot), ui.FOOD)
    for x in snakeposition:
        ui.place(x[0], x[1], ui.SNAKE)


def play_snake(init_ui):
    global width, height, ui, keep_running, xcoord, ycoord, dir, apple_spot
    ui = init_ui
    width, height = ui.board_size()
    init()
    ui.show()
    ui.print_("Level 1")

    while keep_running:
        event = ui.get_event()
        if event.name == "alarm":
            ui.show()
            update_coords()
            eat()
            collide()
            draw()
        elif event.name == "arrow" and event.data == "r" and dir != "east" and dir != "west":
            dir = "east"
        elif event.name == "arrow" and event.data == "l" and dir != "east" and dir != "west":
            dir = "west"
        elif event.name == "arrow" and event.data == "u" and dir != "north" and dir != "south":
            dir = "north"
        elif event.name == "arrow" and event.data == "d" and dir != "north" and dir != "south":
            dir = "south"
        # make sure you handle the quit event like below,
        # or the test might get stuck in an infinite loop
        if event.name == "quit":
            keep_running = False

if __name__ == "__main__":
    # do this if running this module directly
    # (not when importing it for the tests)
    ui = snakelib.SnakeUserInterface(10, 10)
    ui.set_animation_speed(SPEED)
    play_snake(ui)
