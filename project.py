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
road_offset = 0
paused = False

# Car properties
car_x = 400
car_y = 100
car_width = 50
car_height = 100
obstacles = []
obstacle_speed = 15
score = 0
level = 1
min_score = 20

# Button Instances
play_button = Button([324, 400], [0.58, 0.749, 0.56], 4, 3, ['PLAY'], [20, 20])
quitButton = Button([324, 300], [0.788, 0.392, 0.501], 4, 3, ['EXIT'], [20, 20])
restart_button = Button([324, 300], [0.78, 0.392, 0.5], 4, 3, ['RESTART'], [20, 20])

def HOMEPAGE():
    Text.draw("PIXEL", [178, 650], [0.858, 0.505, 0.482], 7)
    Text.draw("VELOCITY", [228, 580], [0.858, 0.505, 0.482], 7)
    play_button.draw(True)
    quitButton.draw(True)

def keyboard(key, x, y):
    global car_x, pausepage, gamepage, homepage, paused
    if key == b'\x1b':  # Escape key to pause
        if gamepage:
            pausepage = True
            gamepage = False
    elif key == b'p':  # 'p' key to toggle pause/play
        if gamepage:
            paused = not paused
    if gamepage:
        if key == b'a' and car_x - car_width / 2 > 150:
            car_x -= 20
        elif key == b'd' and car_x + car_width / 2 < 650:
            car_x += 20

def mouse(button, state, x, y):
    global homepage, gamepage, delay, animation_loop, car_x, car_y, gameoverpage, score, obstacles
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 800 - y  # Convert GLUT's y-coordinate
        if homepage and not delay[0]:
            if play_button.pressed(x, y):
                homepage = False
                gamepage = True
                delay = [True, (animation_loop - 90) % 100]
            elif quitButton.pressed(x, y):
                glutLeaveMainLoop()
        elif gameoverpage:
            if restart_button.pressed(x, y):
                restart_game()
                gameoverpage = False
                gamepage = True  

def restart_game():
    global car_x, car_y, score, level, obstacles, obstacle_speed, min_score
    car_x = 400
    car_y = 100
    score = 0
    level = 1
    obstacles = []
    obstacle_speed = 5
    min_score = 20

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
    elif gameoverpage:
        GAMEOVERPAGE()
    glutSwapBuffers()

def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()




def draw_filled_rectangle(x1, y1, x2, y2, color, px):
    for y in range(y1, y2 + 1):
        drawLine(x1, y, x2, y, color, px)
def draw_car():
    car_color = [1.0, 0.0, 0.0]  # Red car body
    wheel_color = [0.0, 0.0, 0.0]  # Black wheels
    rim_color = [0.7, 0.7, 0.7]  # Gray rims
    window_color = [0.5, 0.5, 0.5]  # Grey windows
    line_thickness = 2  # Pixel size for lines
    wheel_radius = 12  # Wheel size

    # Car body
    draw_filled_rectangle(
        car_x - car_width // 2, car_y, car_x + car_width // 2, int(car_y + car_height * 0.6),
        car_color, line_thickness
    )

    # Car roof (slightly curved appearance)
    draw_filled_rectangle(
        car_x - car_width // 4, int(car_y + car_height * 0.6), car_x + car_width // 4, int(car_y + car_height),
        car_color, line_thickness
    )

    # Window section
    draw_filled_rectangle(
        car_x - car_width // 4, int(car_y + car_height * 0.6), car_x + car_width // 4, int(car_y + car_height * 0.7),
        window_color, line_thickness
    )

    # Rear wheels
    rear_wheel_offset = 10
    drawCircle([car_x - car_width // 2 - rear_wheel_offset, car_y + car_height * 0.2], wheel_radius, wheel_color, line_thickness)
    drawCircle([car_x + car_width // 2 + rear_wheel_offset, car_y + car_height * 0.2], wheel_radius, wheel_color, line_thickness)

    # Front wheels
    front_wheel_offset = 10
    drawCircle([car_x - car_width // 3 - front_wheel_offset, car_y + car_height - 10], wheel_radius, wheel_color, line_thickness)
    drawCircle([car_x + car_width // 3 + front_wheel_offset, car_y + car_height - 10], wheel_radius, wheel_color, line_thickness)

    # Optional: Adding filled rims for the wheels
    for wheel_x, wheel_y in [
        [car_x - car_width // 2 - rear_wheel_offset, car_y + car_height * 0.2],
        [car_x + car_width // 2 + rear_wheel_offset, car_y + car_height * 0.2],
        [car_x - car_width // 3 - front_wheel_offset, car_y + car_height - 10],
        [car_x + car_width // 3 + front_wheel_offset, car_y + car_height - 10],
    ]:
        drawCircle([wheel_x, wheel_y], wheel_radius * 0.8, rim_color, line_thickness)  # Rim
        drawCircle([wheel_x, wheel_y], wheel_radius * 0.6, [0.2, 0.2, 0.2], line_thickness)  # Tread texture

def generate_obstacle():
    x_pos = random.randint(200, 600)
    width = random.randint(30, 80)
    height = 60
    # Generate random color
    obstacles.append([x_pos, 800, width, height])  # Add color to obstacle data


def draw_obstacles():
    line_thickness = 2  # Pixel size for the obstacle lines
    color = [random.random(), random.random(), random.random()]

    for obs in obstacles:
        x1 = obs[0] - obs[2] // 2  # Left x-coordinate
        y1 = obs[1]                # Bottom y-coordinate
        x2 = obs[0] + obs[2] // 2  # Right x-coordinate
        y2 = obs[1] + obs[3]       # Top y-coordinate
                  # Fixed color for the obstacle

        # Draw filled rectangle for the obstacle
        draw_filled_rectangle(x1, y1, x2, y2, color, line_thickness)



def draw_road():
    global road_offset
    road_color = [0.3, 0.3, 0.3]  # Dark grey road
    line_thickness = 2  # Pixel size for lines

    

    # Left and right boundaries using lines
    drawLine(150, 0, 150, 800, road_color, line_thickness)
    drawLine(650, 0, 650, 800, road_color, line_thickness)

    # Side stripes (white)
    side_stripe_color = [1.0, 1.0, 1.0]
    drawLine(160, 0, 160, 800, side_stripe_color, line_thickness)  # Left side stripe
    drawLine(640, 0, 640, 800, side_stripe_color, line_thickness)  # Right side stripe

     # Center dashed line (moving effect)
    dashed_line_color = [1.0, 1.0, 1.0]  # White dashed line
    for i in range(-40, 800, 40):
        y_start = (i + road_offset) % 800
        y_end = (i + road_offset + 20) % 800
        if y_start < y_end:
            drawLine(400, y_start, 400, y_end, dashed_line_color, line_thickness)
        else:
            # Handle wrapping case
            drawLine(400, y_start, 400, 800, dashed_line_color, line_thickness)
            drawLine(400, 0, 400, y_end, dashed_line_color, line_thickness)

    # Update the road offset to simulate movement
    road_offset = (road_offset + 5) % 800


def draw_filled_circle(center, radius, color, px):
    # Draw a filled circle using multiple concentric circles
    for r in range(radius, 0, -1):
        drawCircle(center, r, color, px)

def draw_environment():
    grass_color = [0.0, 0.5, 0.0]  # Green grass
    tree_trunk_color = [0.55, 0.27, 0.07]  # Brown for tree trunks
    tree_leaves_color = [0.0, 0.8, 0.0]  # Bright green for tree leaves
    bush_color = [0.0, 0.6, 0.0]  # Dark green for bushes
    rock_color = [0.5, 0.5, 0.5]  # Grey for rocks
    flower_color = [1.0, 0.0, 0.0]  # Red for flowers
    line_thickness = 2  # Pixel size for environment lines

    # Grass areas on the left and right of the road
    drawLine(0, 0, 150, 0, grass_color, line_thickness)  # Bottom left
    drawLine(150, 0, 150, 800, grass_color, line_thickness)  # Left boundary
    drawLine(0, 800, 150, 800, grass_color, line_thickness)  # Top left
    drawLine(0, 800, 0, 0, grass_color, line_thickness)  # Left vertical

    drawLine(650, 0, 800, 0, grass_color, line_thickness)  # Bottom right
    drawLine(650, 0, 650, 800, grass_color, line_thickness)  # Right boundary
    drawLine(800, 800, 650, 800, grass_color, line_thickness)  # Top right
    drawLine(800, 800, 800, 0, grass_color, line_thickness)  # Right vertical

    # Adding filled trees along the left and right sides
    for x, y in [(40, 200), (100, 300), (80, 500)]:  # Left side trees
        draw_filled_circle([x, y - 10], 6, tree_trunk_color, line_thickness)  # Tree trunk
        draw_filled_circle([x, y + 10], 15, tree_leaves_color, line_thickness)  # Tree leaves

    for x, y in [(680, 250), (740, 400), (710, 600)]:  # Right side trees
        draw_filled_circle([x, y - 10], 6, tree_trunk_color, line_thickness)  # Tree trunk
        draw_filled_circle([x, y + 10], 15, tree_leaves_color, line_thickness)  # Tree leaves

    # Adding filled bushes along the sides
    for x, y in [(60, 100), (120, 150), (90, 600)]:  # Left side bushes
        draw_filled_circle([x, y], 10, bush_color, line_thickness)
        draw_filled_circle([x + 10, y + 5], 8, bush_color, line_thickness)

    for x, y in [(690, 120), (750, 180), (720, 650)]:  # Right side bushes
        draw_filled_circle([x, y], 10, bush_color, line_thickness)
        draw_filled_circle([x - 10, y - 5], 8, bush_color, line_thickness)

    # Adding filled rocks for variation
    for x, y in [(50, 250), (110, 450), (700, 350), (760, 500)]:
        draw_filled_circle([x, y], 5, rock_color, line_thickness)

    # Adding filled flowers for color and variety
    for x, y in [(60, 220), (140, 500), (720, 150), (770, 450)]:
        draw_filled_circle([x, y], 3, flower_color, line_thickness)
        draw_filled_circle([x + 2, y + 2], 2, flower_color, line_thickness)



def GAMEPAGE():
    global score, obstacles
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_environment()
    draw_road()
    draw_car()
    draw_obstacles()
    move_obstacles()
    check_collision()
    update_level()
    display_score()
    glutSwapBuffers()

def move_obstacles():
    global score, obstacles
    for obs in obstacles:
        obs[1] -= obstacle_speed
        if obs[1] + obs[3] < 0:
            obstacles.remove(obs)
            score += 1
    if len(obstacles) < 20 and random.randint(1, 30) == 1:
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

def GAMEOVERPAGE():
    global score
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    center_x = 400  
    center_y = 400  

    gameover_y = center_y + 150  # Positioned higher up from the center to allow space for other elements
    score_y = center_y + 50      # Positioned below the "GAME OVER" text
    level_y = score_y - 50       # Positioned below score
    button_y = center_y - 250    # Further down to avoid overlap with texts

    Text.draw("GAME OVER", [center_x - 200, gameover_y], [1.0, 0.0, 0.0], 7)  
    score_text = f"FINAL SCORE: {score}"
    level_text = f"LEVEL REACHED: {level}"
    Text.draw(score_text, [center_x - 220, score_y], [1.0, 1.0, 1.0], 5) 
    Text.draw(level_text, [center_x - 220, level_y], [1.0, 1.0, 1.0], 5)
    restart_button.position = [center_x - 93, button_y]  
    restart_button.draw(True)  
    glutSwapBuffers()


def update_level():
    global level, obstacle_speed, min_score
    if score >= min_score:
        level += 1
        obstacle_speed += 2 
        min_score += 20 


def display_score():
    Text.draw(f"SCORE: {score}", [10, 750], [1.0, 1.0, 1.0], 3)
    Text.draw(f"LEVEL: {level}", [600, 750], [1.0, 1.0, 1.0], 3)

def animate(value):
    global animation_loop
    # animation_loop = (animation_loop + 1) % 100
    # if not delay[0] or (delay[1] == animation_loop):
    #     delay[0] = False
    glutPostRedisplay()
    glutTimerFunc(30, animate, 0)

# Initialize GLUT and start the main loop
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Pixel Velocity")
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
animate(0)
glutMainLoop()
