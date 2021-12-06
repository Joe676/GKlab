import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, pi
from random import random

N = 20
vertices = [[[0, 0, 0] for _ in range(N)] for _ in range(N)]
colors = [[[random(), random(), random()] for _ in range(N)] for _ in range(N)]


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    global vertices
    u_arr = [i/(N-1) for i in range(N)]
    v_arr = [i/(N-1) for i in range(N)]
    for i, u in enumerate(u_arr): #u
        for j, v in enumerate(v_arr): #v
            vertices[i][j] = [x(u, v), y(u, v), z(u, v)]
    #Fixing coloring artifact
    #Indexes of adjacent vertices on the seam are "flipped"
    #That's why the colors can't be simply copied from one side to the other
    #but also flipped i -> N-i-1
    for i in range(N):
        colors[i][0] = colors[N-i-1][N-1] 


def shutdown():
    pass

def spin(angle):
    glRotatef(angle, 1, 0, 0)
    glRotatef(angle, 0, 1, 0)
    glRotatef(angle, 0, 0, 1)

def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def x(u, v):
    return (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u) * cos(pi*v)

def y(u, v):
    return 160*u**4 - 320*u**3 + 160*u**2 -5 #-5 to center the egg

def z(u, v):
    return (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u) * sin(pi*v)

def egg():
    glColor3f(0.5, 0.5, 0.9)
    glBegin(GL_POINTS)

    for i in range(N):
        for j in range(N):
            glVertex3fv(vertices[i][j])

    glEnd()

def egg_lines():
    glColor3f(0.5, 0.5, 0.9)
    glBegin(GL_LINES)

    for i in range(N-1):
        for j in range(N-1):
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[(i+1)%N][j])

            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i][(j+1)%N])

    glEnd()

def egg_triangles():
    glBegin(GL_TRIANGLES)

    for i in range(N-1):
        for j in range(N-1):
            glColor3fv(colors[i][j])
            glVertex3fv(vertices[i][j])
            glColor3fv(colors[i+1][j])
            glVertex3fv(vertices[i+1][j])
            glColor3fv(colors[i][j+1])
            glVertex3fv(vertices[i][j+1])

            glColor3fv(colors[i+1][j])    
            glVertex3fv(vertices[i+1][j])
            glColor3fv(colors[i+1][j+1])
            glVertex3fv(vertices[i+1][j+1])
            glColor3fv(colors[i][j+1])
            glVertex3fv(vertices[i][j+1])

    glEnd()

def egg_strips():
    for i in range(N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N-1):
            glColor3fv(colors[i][j])
            glVertex3fv(vertices[i][j])
            glColor3fv(colors[i+1][j])
            glVertex3fv(vertices[i+1][j])
        glColor3fv(colors[i][N-1])
        glVertex3fv(vertices[i][N-1])
        glColor3fv(colors[i+1][N-1])
        glVertex3fv(vertices[i+1][N-1])
        glEnd()

def mid_point(a, b):
    return [(i+j)/2 for i, j in zip(a, b)]

def sierpinski_pyramid(p0, p1, p2, p3, lvl = 0):
    if lvl == 0:
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex3fv(p0)
        glVertex3fv(p1)
        glVertex3fv(p2)

        glColor3f(0, 1, 0)
        glVertex3fv(p0)
        glVertex3fv(p2)
        glVertex3fv(p3)

        glColor3f(0, 0, 1)
        glVertex3fv(p0)
        glVertex3fv(p3)
        glVertex3fv(p1)

        glColor3f(1, 0, 1)
        glVertex3fv(p1)
        glVertex3fv(p2)
        glVertex3fv(p3)
        
        glEnd()
        return
    m01 = mid_point(p0, p1)
    m02 = mid_point(p0, p2)
    m03 = mid_point(p0, p3)
    m12 = mid_point(p1, p2)
    m13 = mid_point(p1, p3)
    m23 = mid_point(p2, p3)

    sierpinski_pyramid(p0, m01, m02, m03, lvl=lvl-1)
    sierpinski_pyramid(m01, p1, m12, m13, lvl=lvl-1)
    sierpinski_pyramid(m02, m12, p2, m23, lvl=lvl-1)           
    sierpinski_pyramid(m03, m13, m23, p3, lvl=lvl-1)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    egg()
    axes()

    glFlush()

def render1(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time*180/3.1415)
    
    egg_lines()
    axes()

    glFlush()

def render2(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time*180/3.1415)
    
    egg_triangles()
    axes()

    glFlush()

def render3(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time*180/3.1415)
    
    egg_strips()
    axes()

    glFlush()

def render4(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time*180/3.1415/2)
    
    sierpinski_pyramid([0, 5, 0], 
                        [-4, -2, 4], 
                        [4, -2, 4], 
                        [0, -2, -4], lvl=4)
    axes()

    glFlush()


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
        # render(glfwGetTime()) #drawing egg
        # render1(glfwGetTime()) #drawing spinning egg /w lines
        # render2(glfwGetTime()) #drawing spinning egg /w triangles & random colors
        # render3(glfwGetTime()) #drawing spinning egg /w triangle strips
        render4(glfwGetTime()) #drawing spinning sierpinski pyramid

        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
