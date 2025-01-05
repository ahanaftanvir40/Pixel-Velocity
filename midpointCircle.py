from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def drawCirclePoint(center, x, y):
    glVertex2f(center[0] + x, center[1] + y)
    glVertex2f(center[0] - x, center[1] + y)
    glVertex2f(center[0] + x, center[1] - y)
    glVertex2f(center[0] - x, center[1] - y)
    glVertex2f(center[0] + y, center[1] + x)
    glVertex2f(center[0] - y, center[1] + x)
    glVertex2f(center[0] + y, center[1] - x)
    glVertex2f(center[0] - y, center[1] - x)
    
def drawCircle(center, radius, color, px):
    if len(color) == 3:
        glColor3f(color[0], color[1], color[2])
    if len(color) == 4:
        glColor4f(color[0], color[1], color[2], color[3])
    glPointSize(px)
    glBegin(GL_POINTS)
    # Midpoint Circle Drawing Algorithm
    x, y = 0, radius
    d = 1 - radius
    drawCirclePoint(center, x, y)
    while y > x:
        if d < 0:
            d += 2*x + 3
            x += 1
        else:
            d += 2*(x-y) + 5
            x += 1
            y -= 1
        drawCirclePoint(center, x, y)
    glEnd()

if __name__ == "__main__":
    pass