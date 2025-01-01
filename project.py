import OpenGL.GL as gl
import OpenGL.GLUT as glut

car_x = 0
car_y = -235 

# Road divider (initial y-coordinates of dashed points)
divider_y_positions = [i * 40 for i in range(-500, 500, 1)]

# Window dimensions
width, height = 500, 500

def midpoint_circle(cx, cy, r):
    points = []
    x, y = 0, r
    p = 1 - r
    points.extend([(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y),
                   (cx + y, cy + x), (cx - y, cy + x), (cx + y, cy - x), (cx - y, cy - x)])
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        points.extend([(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y),
                       (cx + y, cy + x), (cx - y, cy + x), (cx + y, cy - x), (cx - y, cy - x)])
    return points

def draw_circle(cx, cy, r):
    points = midpoint_circle(cx, cy, r)
    gl.glBegin(gl.GL_POINTS)
    for point in points:
        gl.glVertex2f(point[0], point[1])
    gl.glEnd()


def draw_line(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    d = 2 * dy - dx
    x, y = x1, y1
    gl.glBegin(gl.GL_POINTS)
    gl.glVertex2f(x, y)
    while x <= x2:
        x += 1
        if d < 0:
            d += 2 * dy
        else:
            y += 1
            d += 2 * (dy - dx)
        gl.glVertex2f(x, y)
    gl.glEnd()


def draw_car():
    # Car body
    draw_line(car_x - 20, car_y, car_x + 20, car_y)  # Bottom line
    draw_line(car_x - 20, car_y, car_x - 20, car_y + 20)  # Left side
    draw_line(car_x + 20, car_y, car_x + 20, car_y + 20)  # Right side
    draw_line(car_x - 20, car_y + 20, car_x + 20, car_y + 20)  # Top line
    # Wheels
    draw_circle(car_x - 15, car_y - 5, 5)
    draw_circle(car_x + 15, car_y - 5, 5)


def draw_road():
    # Left lane boundary
    gl.glBegin(gl.GL_POINTS)
    for y in range(-height // 2, height // 2, 5):
        gl.glVertex2f(-150, y)  # Left boundary
        gl.glVertex2f(150, y)   # Right boundary
    gl.glEnd()

    # Center moving dashed line
    gl.glBegin(gl.GL_POINTS)
    for y in divider_y_positions:
        for x in range(-2, 3):  # Dashed line width
            gl.glVertex2f(x, y)
    gl.glEnd()


def update(value):
    global divider_y_positions
    # Update the divider to simulate downward movement
    divider_y_positions = [(y - 5 if y > -height // 2 else height // 2) for y in divider_y_positions]
    glut.glutPostRedisplay()
    glut.glutTimerFunc(50, update, 0)


def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glLoadIdentity()
    draw_road()
    draw_car()
    glut.glutSwapBuffers()


def keyboard(key, x, y):
    global car_x
    step = 10  # Horizontal movement step
    if key == b'a' and car_x - 50 > -160:  # Move left within left lane
        car_x -= step
    elif key == b'd' and car_x + 50 < 160:  # Move right within right lane
        car_x += step
    glut.glutPostRedisplay()


def reshape(w, h):
    gl.glViewport(0, 0, w, h)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-width // 2, width // 2, -height // 2, height // 2, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)


def main():
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)
    glut.glutInitWindowSize(width, height)
    glut.glutCreateWindow(b"Car Racer Game: Moving Divider")
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    glut.glutDisplayFunc(display)
    glut.glutReshapeFunc(reshape)
    glut.glutKeyboardFunc(keyboard)
    glut.glutTimerFunc(50, update, 0)
    glut.glutMainLoop()


if __name__ == "__main__":
    main()
