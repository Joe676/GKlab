import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, comb
from random import random

N = 6
control_points = []
max_h = 10
bezier_start_point = (-10, -10)
bezier_extents = (20, 20)

curr = [0, 0]

bezier = []
bN = 30

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
R = 10
scale = 1

pix2angle = 1.0
pix2scale = 0.002
deg2rad = 3.141592/180

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

MODE = 0 #0 - camera, 1 - node modification
show_control_points = True
show_bezier_surface = True

def calculate_bezier():
    global bezier
    global bN

    for i in range(bN):
        for j in range(bN):
            bezier[i][j] = bezier_point(i, j)

def B(a, b, c):
    return comb(b, a) * c**a * (1-c)**(b-a)

def bezier_point(i, j):
    u = i/(bN-1)
    v = j/(bN-1)
    P = [0, 0, 0]
    for k in range(N):
        for l in range(N):
            for h in range(3):
                P[h] += control_points[k][l][h] * B(k, N-1, u) * B(l, N-1, v)
    return P

def randomize_control_points():
    for i in range(N):
        for j in range(N):
            control_points[i][j] = [bezier_start_point[0] + i*(bezier_extents[0]/(N-1)),
                                    random()*max_h*2 - max_h,
                                    bezier_start_point[1] + j*(bezier_extents[1]/(N-1))]


def startup():
    global control_points
    global bezier
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    control_points = [[[0, 0, 0] for _ in range(N)] for _ in range(N)]
    bezier = [[[0, 0, 0] for _ in range(bN)] for _ in range(bN)]
    randomize_control_points()
    calculate_bezier()


def shutdown():
    pass


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

def draw_control_points():
    global control_points

    glColor3d(255, 0, 102)

    quadric = gluNewQuadric()

    for i in range(N):
        for j in range(N):
            glTranslatef(*control_points[i][j])
            if MODE == 1 and i == curr[0] and j == curr[1]:
                glColor3f(1, 1, 0)
                gluSphere(quadric, 0.5, 5, 5)
                glColor3d(255, 0, 102)
            else:
                gluSphere(quadric, 0.2, 4, 4)

            glTranslatef(-control_points[i][j][0], -control_points[i][j][1], -control_points[i][j][2])

    gluDeleteQuadric(quadric)

    glColor3f(255/255, 153/255, 221/255)
    for i in range(N-1):
        for j in range(N-1):
            glBegin(GL_LINE_LOOP)

            glVertex3fv(control_points[i][j])
            glVertex3fv(control_points[i+1][j])
            glVertex3fv(control_points[i][j+1])

            glEnd()
        glBegin(GL_LINES)
        glVertex3fv(control_points[i][N-1])
        glVertex3fv(control_points[i+1][N-1])
        glEnd()
    glBegin(GL_LINE_STRIP)
    for j in range(N):
        glVertex3fv(control_points[N-1][j])
    glEnd()

def draw_bezier_surface():
    glColor3f(0.0, 1.0, 0.0)

    quadric = gluNewQuadric()

    for i in range(bN):
        for j in range(bN):
            glTranslatef(*bezier[i][j])
            gluSphere(quadric, 0.1, 4, 4)
            glTranslatef(-bezier[i][j][0], -bezier[i][j][1], -bezier[i][j][2])

    gluDeleteQuadric(quadric)
    glBegin(GL_LINES)
    for i in range(bN-1):
        for j in range(bN-1):
            glVertex3fv(bezier[i][j])
            glVertex3fv(bezier[i+1][j])
            glVertex3fv(bezier[i][j])
            glVertex3fv(bezier[i][j+1])
        glVertex3fv(bezier[i][bN-1])
        glVertex3fv(bezier[i+1][bN-1])
    for j in range(bN-1):
        glVertex3fv(bezier[bN-1][j])
        glVertex3fv(bezier[bN-1][j+1])
    glEnd()

def render(time):
    global theta
    global phi
    global R
    global control_points

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
        if phi > 180:
            phi -= 360
        if phi < -180:
            phi += 360
    

    if MODE == 0:
        if right_mouse_button_pressed:
            R += delta_y * 0.1
            if R < 0.2:
                R = 0.2
            if R > 30:
                R = 30
    else:
        if right_mouse_button_pressed:
            control_points[curr[0]][curr[1]][1] += delta_y * 0.1
            calculate_bezier()

    x_eye = R*cos(theta*deg2rad)*cos(phi*deg2rad)
    y_eye = R*sin(phi*deg2rad)
    z_eye = R*sin(theta*deg2rad)*cos(phi*deg2rad)
    if phi <= 90 and phi >= -90:
        gluLookAt(x_eye, y_eye, z_eye,
            0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    else:
        gluLookAt(x_eye, y_eye, z_eye,
            0.0, 0.0, 0.0, 0.0, -1.0, 0.0)
    axes()
    if show_control_points:
        draw_control_points()
    if show_bezier_surface:
        draw_bezier_surface()

    glFlush()



def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global MODE
    global show_control_points
    global show_bezier_surface
    global curr

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        MODE = (MODE+1)%2
    if key == GLFW_KEY_C and action == GLFW_PRESS:
        show_control_points = not show_control_points
    if key == GLFW_KEY_B and action == GLFW_PRESS:
        show_bezier_surface = not show_bezier_surface
    if key == GLFW_KEY_R and action == GLFW_PRESS:
        randomize_control_points()
        calculate_bezier()
    
    
    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        curr[1] = (curr[1]+1)%N
    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        curr[1] = (curr[1]-1)%N
    if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
        curr[0] = (curr[0]+1)%N
    if key == GLFW_KEY_LEFT and action == GLFW_PRESS:
        curr[0] = (curr[0]-1)%N



def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0
        
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime()) #5.0

        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
