from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from button import Button, Text
from midpointLine import drawLine
from midpointCircle import drawCircle
import random

# Global Variables
homepage = True
levelpage = False
gamepage = False
pausepage = False
gameoverpage = False
delay = [False, 0]
animation_loop = 0

# Car properties
car_x = 400
car_y = 100
car_width = 50
car_height = 100
obstacles = []
obstacle_speed = 5
score = 0

# Button Instances
play_button = Button([324, 400], [0.58, 0.749, 0.56], 4, 3, ['PLAY'], [20, 20])
quitButton = Button([324, 300], [0.788, 0.392, 0.501], 4, 3, ['EXIT'], [20, 20])

def HOMEPAGE():
    Text.draw("AFTERBURN", [178, 650], [0.858, 0.505, 0.482], 7)
    Text.draw("ASSAULT", [228, 580], [0.858, 0.505, 0.482], 7)
    play_button.draw(True)
    quitButton.draw(True)

def keyboard(key, x, y):
    global car_x, pausepage, gamepage, homepage
    if key == b'\x1b':  # Escape key to pause
        if gamepage:
            pausepage = True
            gamepage = False
    if gamepage:
        if key == b'a' and car_x - car_width / 2 > 150:
            car_x -= 20
        elif key == b'd' and car_x + car_width / 2 < 650:
            car_x += 20

def mouse(button, state, x, y):
    global homepage, gamepage, delay, animation_loop
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 800 - y  # Convert GLUT's y-coordinate
        if homepage and not delay[0]:
            if play_button.pressed(x, y):
                homepage = False
                gamepage = True
                delay = [True, (animation_loop - 90) % 100]
            elif quitButton.pressed(x, y):
                glutLeaveMainLoop()

def showScreen():
    global homepage, gamepage
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.074, 0.0627, 0.16, 1.0)
    glLoadIdentity()
    iterate()
    if homepage:
        HOMEPAGE()
    elif gamepage:
        GAMEPAGE()
    glutSwapBuffers()

def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def generate_obstacle():
    x_pos = random.randint(200, 600)
    obstacles.append([x_pos, 800, 50, 50])  # [x, y, width, height]

def draw_car():
    car_color = [1.0, 0.0, 0.0]  # Red car
    wheel_color = [0.0, 0.0, 0.0]  # Black wheels
    line_thickness = 2  # Pixel size for the car lines
    
    # Car body
    drawLine(car_x - car_width // 2, car_y, car_x + car_width // 2, car_y, car_color, line_thickness)  # Bottom
    drawLine(car_x - car_width // 2, car_y, car_x - car_width // 2, car_y + car_height, car_color, line_thickness)  # Left
    drawLine(car_x + car_width // 2, car_y, car_x + car_width // 2, car_y + car_height, car_color, line_thickness)  # Right
    drawLine(car_x - car_width // 2, car_y + car_height, car_x + car_width // 2, car_y + car_height, car_color, line_thickness)  # Top
    
    # Wheels
    drawCircle([car_x - 15, car_y - 10], 10, wheel_color, line_thickness)  # Left wheel
    drawCircle([car_x + 15, car_y - 10], 10, wheel_color, line_thickness)  # Right wheel

def draw_obstacles():
    obstacle_color = [0.0, 0.0, 1.0]  # Blue obstacles
    line_thickness = 2  # Pixel size for the obstacle lines
    
    for obs in obstacles:
        drawLine(obs[0] - obs[2] // 2, obs[1], obs[0] + obs[2] // 2, obs[1], obstacle_color, line_thickness)  # Top
        drawLine(obs[0] - obs[2] // 2, obs[1], obs[0] - obs[2] // 2, obs[1] + obs[3], obstacle_color, line_thickness)  # Left
        drawLine(obs[0] + obs[2] // 2, obs[1], obs[0] + obs[2] // 2, obs[1] + obs[3], obstacle_color, line_thickness)  # Right
        drawLine(obs[0] - obs[2] // 2, obs[1] + obs[3], obs[0] + obs[2] // 2, obs[1] + obs[3], obstacle_color, line_thickness)  # Bottom

def draw_road():
    road_color = [0.5, 0.5, 0.5]  # Grey road
    line_thickness = 2  # Pixel size for road lines
    drawLine(150, 0, 150, 800, road_color, line_thickness)  # Left boundary
    drawLine(650, 0, 650, 800, road_color, line_thickness)  # Right boundary
    
    dashed_line_color = [1.0, 1.0, 1.0]  # White dashed line
    for i in range(0, 800, 40):
        drawLine(400, i, 400, i + 20, dashed_line_color, line_thickness)  # Center dashed line

def draw_environment():
    grass_color = [0.0, 0.5, 0.0]  # Green grass
    line_thickness = 2  # Pixel size for environment lines
    drawLine(0, 0, 150, 0, grass_color, line_thickness)  # Bottom left
    drawLine(150, 0, 150, 800, grass_color, line_thickness)  # Left boundary
    drawLine(0, 800, 150, 800, grass_color, line_thickness)  # Top left
    drawLine(0, 800, 0, 0, grass_color, line_thickness)  # Left vertical

    drawLine(650, 0, 800, 0, grass_color, line_thickness)  # Bottom right
    drawLine(650, 0, 650, 800, grass_color, line_thickness)  # Right boundary
    drawLine(800, 800, 650, 800, grass_color, line_thickness)  # Top right
    drawLine(800, 800, 800, 0, grass_color, line_thickness)  # Right vertical

def GAMEPAGE():
    global score, obstacles
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_environment()
    draw_road()
    draw_car()
    draw_obstacles()
    move_obstacles()
    check_collision()
    display_score()
    glutSwapBuffers()

def move_obstacles():
    global score, obstacles
    for obs in obstacles:
        obs[1] -= obstacle_speed
        if obs[1] + obs[3] < 0:
            obstacles.remove(obs)
            score += 1
    if len(obstacles) < 5 and random.randint(1, 50) == 1:
        generate_obstacle()

def check_collision():
    global gamepage, gameoverpage
    for obs in obstacles:
        if (car_x - car_width // 2 < obs[0] + obs[2] // 2 and
            car_x + car_width // 2 > obs[0] - obs[2] // 2 and
            car_y < obs[1] + obs[3] and
            car_y + car_height > obs[1]):
            gamepage = False
            gameoverpage = True

def display_score():
    Text.draw(f"SCORE: {score}", [10, 750], [1.0, 1.0, 1.0], 3)

def animate(value):
    global animation_loop
    animation_loop = (animation_loop + 1) % 100
    if not delay[0] or (delay[1] == animation_loop):
        delay[0] = False
    glutPostRedisplay()
    glutTimerFunc(30, animate, 0)

# Initialize GLUT and start the main loop
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Afterburn Assault")
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
animate(0)
glutMainLoop()
