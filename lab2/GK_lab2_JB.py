import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

RAND_SEED = 0

def startup():
    global RAND_SEED
    RAND_SEED = random.randint(0, 10000)
    print("random seed:", RAND_SEED)
    update_viewport(None, 800, 800)
    glClearColor(0.1, 0.1, 0.3, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

    glFlush()

def render1():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    
    glColor3f(1, 0, 0)
    glVertex2f(-50, -50)
    
    glColor3f(0, 1, 0)
    glVertex2f(50, -50)
    
    glColor3f(0, 0, 1)
    glVertex2f(0, 50)

    glEnd()

    glFlush()

def render2():
    glClear(GL_COLOR_BUFFER_BIT)

    rect(0, 0, 100, 100, mode='CENTER', color_mode='FLAT')

    glFlush()

def render3():
    random.seed(RAND_SEED)
    glClear(GL_COLOR_BUFFER_BIT)

    rect(0, 0, 100, 100, mode='CENTER', color_mode='FLAT')
    rect(0, 0, 100, 100, mode='CENTER', color_mode='COLORFUL', d=4.0)

    glFlush()

def render4():
    random.seed(RAND_SEED)
    glClear(GL_COLOR_BUFFER_BIT)
    
    sierpinski_rect(-90, -90, 180, 180, color_mode='COLORFUL', levels=4)

    glFlush()

def render5():
    glClear(GL_COLOR_BUFFER_BIT)
    
    sierpinski_triangle((-90, -90), (90, -90), (0, 90), levels=6)

    glFlush()

def render6():
    glClear(GL_COLOR_BUFFER_BIT)
    
    
    random.seed(RAND_SEED)
    iterated_function_system((-50, -50))

    glFlush()

def rect(x, y, w, h, mode='CORNER', color_mode='COLORFUL', color = (0.0, 0.3, 0.7), d=0.0):
    if mode == 'CENTER':
        return rect(x-w/2, y-h/2, w, h, color_mode=color_mode, color=color, d=d)

    colors = tuple([tuple([random.random() for _ in range(3)]) for _ in range(4)]) #dl, dr, ur, ul

    dl, dr, ur, ul = colors
    if color_mode == 'FLAT':
        dl, dr, ur, ul = color, color, color, color

    displacements = [[random.random()*2-1 for _ in range(2)] for _ in range(4)]

    ps = [[x,   y],
          [x+w,   y],
          [x,   y+h],
          [x+w,   y+h]]
    
    for j in range(4):
        for i in range(2):
            ps[j][i] += d * displacements[j][i]

    

    glBegin(GL_TRIANGLE_STRIP)

    #Lower-Left    
    glColor3f(*dl)
    glVertex2f(*ps[0])
    
    #Lower-Right
    glColor3f(*dr)
    glVertex2f(*ps[1])
    
    #Upper-Left
    glColor3f(*ul)
    glVertex2f(*ps[2])

    #Upper-Right
    glColor3f(*ur)
    glVertex2f(*ps[3])
        
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

def plasma_fractal(resolution):
    random.seed(RAND_SEED)
    arr = [[-1 for _ in range(resolution)] for _ in range(resolution)]
    
    #INIT
    arr[0][0] = random.random()
    arr[0][-1] = random.random()
    arr[-1][0] = random.random()
    arr[-1][-1] = random.random()

    for line in arr:
        print(line)

def fi(p, params):
    nx = params[0]*p[0] + params[1]*p[1] + params[2]
    ny = params[3]*p[0] + params[4]*p[1] + params[5]
    return nx, ny

def iterated_function_system(start):
    fis = [ [-0.67, -0.02, 0, -0.18, 0.81, 10],
            [0.4, 0.4, 0, -0.1, 0.4, 0],
            [-0.4, -0.4, 0, -0.1, 0.4, 0],
            [-0.1, 0, 0, 0.44, 0.44, -2]]
    
    glBegin(GL_POINTS)
    glColor3f(0, 1, 0)
    for i in range(50000):
        glVertex2fv(start)

        fi_params = random.choice(fis)
        start = fi(start, fi_params)
    glEnd()


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

    window = glfwCreateWindow(800, 800, "lab2", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        # render(glfwGetTime()) #example
        # render1() #triangle
        # render2() #rect
        # render3() #random
        render4() #sierpinski rect
        # render5() #sierpinski triangle
        # render6() #iterated function system
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()
