from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def zoneConversion(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    
def drawLine(x1, y1, x2, y2, color,px):
    # Line drawing algorithm
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy > 0:
            zone = 0
            x_c_0, y_c_0 = x1, y1
            x_c_1, y_c_1 = x2, y2
        elif dx <= 0 and dy > 0:
            zone = 3
            x_c_0, y_c_0 = -x1, y1
            x_c_1, y_c_1 = -x2, y2
        elif dx <= 0 and dy < 0:
            zone = 4
            x_c_0, y_c_0 = -x1, -y1
            x_c_1, y_c_1 = -x2, -y2
        else:
            zone = 7
            x_c_0, y_c_0 = x1,-y1
            x_c_1, y_c_1 = x2,-y2
    else:                  
        if dx >= 0 and dy > 0:
            zone = 1
            x_c_0, y_c_0 = y1, x1
            x_c_1, y_c_1 = y2, x2
        elif dx <= 0 and dy > 0:
            zone = 2
            x_c_0, y_c_0 = y1, -x1
            x_c_1, y_c_1 = y2, -x2
        elif dx <= 0 and dy < 0:
            zone = 5
            x_c_0, y_c_0 = -y1, -x1
            x_c_1, y_c_1 = -y2, -x2
        else:
            zone = 6
            x_c_0, y_c_0 = -y1, x1
            x_c_1, y_c_1 = -y2, x2   
    dx = x_c_1 - x_c_0
    dy = y_c_1 - y_c_0
    d = 2*dy - dx
    dE = 2*dy
    dNE = 2*(dy-dx)
    x, y = x_c_0, y_c_0
    glColor3f(color[0], color[1], color[2])
    glPointSize(px) 
    glBegin(GL_POINTS)
    for i in range (int(x), int(x_c_1)):
        temp = zoneConversion(i, y, zone)
        glVertex2f(temp[0], temp[1])
        if d < 0:
            d += dE
        else:
            d += dNE
            y += 1
    glEnd()

if __name__ == "__main__":
    pass