import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

# RAND_SEED = 0

def startup():
    # global RAND_SEED
    # RAND_SEED = random.randint(0, 10000)
    update_viewport(None, 800, 800)
    glClearColor(0.1, 0.1, 0.3, 1.0)


def shutdown():
    pass


def render(time):
    random.seed(0)
    glClear(GL_COLOR_BUFFER_BIT)

    # glBegin(GL_TRIANGLES)
    # glColor3f(1.0, 0.0, 0.0)
    # glVertex2f(-50.0, -50.0)
    # glColor3f(0.0, 1.0, 0.0)
    # glVertex2f(50.0, -50.0)
    # glColor3f(0.0, 0.0, 1.0)
    # glVertex2f(0.0, 50.0)
    # glEnd()

    # rect(0, 0, 60, 70, 'CENTER')
    sierpinski_rect(-90, -90, 80, 180, color_mode='COLORFUL', levels = 4)

    glColor3f(0.9, 0.5, 0.8)
    # triangle((0,0), (50, 50), (-50, 50))
    sierpinski_triangle((0, -90), (90, -90), (45, 90))


    glFlush()

def rect(x, y, w, h, mode='CORNER', color_mode='COLORFUL', color = (0.0, 0.3, 0.7)):
    if mode == 'CENTER':
        return rect(x-w/2, y-h/2, w, h, color_mode=color_mode, color=color)

    colors = tuple([tuple([random.random() for _ in range(3)]) for _ in range(4)]) #dl, dr, ur, ul

    dl, dr, ur, ul = colors
    if color_mode == 'FLAT':
        dl, dr, ur, ul = color, color, color, color

    glBegin(GL_TRIANGLES)
        
    glColor3f(*dl)
    glVertex2f(x,   y)
    glColor3f(*dr)
    glVertex2f(x+w, y)
    glColor3f(*ul)
    glVertex2f(x,   y+h)

    glColor3f(*dr)
    glVertex2f(x+w, y)
    glColor3f(*ul)
    glVertex2f(x,   y+h)
    glColor3f(*ur)
    glVertex2f(x+w, y+h)
        
    glEnd()

def triangle(p1, p2, p3):
    glBegin(GL_TRIANGLES)    
    glVertex2f(*p1)
    glVertex2f(*p2)
    glVertex2f(*p3)
    glEnd()

def sierpinski_rect(x, y, w, h, levels = 3, color_mode='FLAT'):
    if levels == 0:
        rect(x, y, w, h, color_mode=color_mode)
        return
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            sierpinski_rect(x + w*i/3, y + h*j/3, w/3, h/3, levels=levels-1, color_mode=color_mode)

def mid_point(a, b):
    return tuple([(i+j)/2 for i, j in zip(a, b)])

def sierpinski_triangle(p1, p2, p3, levels=3):
    if levels == 0:
        triangle(p1, p2, p3)
        return
    
    np1 = mid_point(p2, p3)
    np2 = mid_point(p1, p3)
    np3 = mid_point(p1, p2)

    sierpinski_triangle(p1, np3, np2, levels=levels-1)
    sierpinski_triangle(p2, np1, np3, levels=levels-1)
    sierpinski_triangle(p3, np2, np1, levels=levels-1)

def koch_flake(center, side_len, levels=3):
    
    pass

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()
