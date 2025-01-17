from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from midpointLine import drawLine
from midpointCircle import drawCircle
from character import CHARACTERS

class Button:
    def __init__(self, pos, color, px, arr, padding = [0,0]):
        self.x = pos[0]
        self.y = pos[1]
        self.size = [0,0]
        self.px = px
        self.color = color 
        self.arr = arr
        self.padding = padding
        self.size = [(len(arr[0])*7*px)+(2*padding[0]), (8*px)+(2*padding[1])]
        
      
    
    def draw(self, boundary = False):
        
        self.textDraw() 
        if boundary:
            self.drawBoundaryBox()

            
        
    def drawBoundaryBox(self):
        x1 = self.x
        y1 = self.y
        x2 = x1 + self.size[0]
        y2 = y1 + self.size[1]
        drawLine(x1,y1, x2,y1, self.color, 1)
        drawLine(x1,y1, x1,y2, self.color, 1)
        drawLine(x2,y1, x2,y2, self.color, 1)
        drawLine(x1,y2, x2,y2, self.color, 1)
        
   
    def textDraw(self):
        glColor3f(self.color[0], self.color[1], self.color[2])
        glPointSize(self.px) 
        glBegin(GL_POINTS)
        string = self.arr[0]
        x = self.x + self.padding[0]
        y = self.y + self.padding[1]
        
        for i in string:
            matrix  = CHARACTERS[i]
            
            for j in range(7):
                y_ = (7-j)*self.px + y
                for k in range(6):
                    if matrix[j][k] == 1:
                        x_ = (k+1)*self.px + x
                        glVertex2f(x_,y_)
            x += 7*self.px
        glEnd()
        
    def pressed(self, x, y):
        if self.x < x < self.x + self.size[0] and self.y < y < self.y + self.size[1]:
            return True
        return False


class Text:
    def draw(string, pos, color, px):
        glColor3f(color[0], color[1], color[2])
        glPointSize(px) 
        glBegin(GL_POINTS)
        x = pos[0]
        y = pos[1]
        for i in string:
            matrix  = CHARACTERS[i]
            
            for j in range(7):
                y_ = (7-j)*px + y
                for k in range(6):
                    if matrix[j][k] == 1:
                        x_ = (k+1)*px + x
                        glVertex2f(x_,y_)
            x += 7*px
        glEnd()
        
