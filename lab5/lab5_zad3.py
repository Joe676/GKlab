import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, pi, sqrt
from random import random


N = 20
vertices = [[[0, 0, 0] for _ in range(N)] for _ in range(N)]
colors = [[[random(), random(), random()] for _ in range(N)] for _ in range(N)]
normals =  [[[0, 0, 0] for _ in range(N)] for _ in range(N)]

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
R = 10

pix2angle = 1.0
deg2rad = 3.141592/180

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    global vertices
    global normals
    u_arr = [i/(N-1) for i in range(N)]
    v_arr = [i/(N-1) for i in range(N)]
    for i, u in enumerate(u_arr): #u
        for j, v in enumerate(v_arr): #v
            vertices[i][j] = [x(u, v), y(u, v), z(u, v)]
            if i == 0 or i == N-1:
                normals[i][j] = [0, -1, 0]
                continue
            if i < N/2:
                normals[i][j] = neg(norm(u, v))
            else:
                normals[i][j] = norm(u, v)
    
    #Fixing coloring artifact
    #Indexes of adjacent vertices on the seam are "flipped"
    #That's why the colors can't be simply copied from one side to the other
    #but also flipped i -> N-i-1
    for i in range(N):
        colors[i][0] = colors[N-i-1][N-1] 


def shutdown():
    pass


def x(u, v):
    return (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u) * cos(pi*v)

def y(u, v):
    return 160*u**4 - 320*u**3 + 160*u**2 -5 #-5 to center the egg

def z(u, v):
    return (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u) * sin(pi*v)

#DERIVATIVES FOR NORMALS
def xu(u, v):
    return (-450*u**4 + 900*u**3 - 810*u**2 + 360*u - 45) * cos(pi*v)

def xv(u, v):
    return pi*(90*u**5 - 225*u**4 + 270*u**3 - 180*u**2 + 45*u) * sin(pi*v)

def yu(u, v):
    return 640*u**3 - 960*u**2 + 320*u

def yv(u, v):
    return 0

def zu(u, v):
    return (-450*u**4 + 900*u**3 - 810*u**2 + 360*u - 45) * sin(pi*v)

def zv(u, v):
    return -pi*(90*u**5 - 225*u**4 + 270*u**3 - 180*u**2 + 45*u) * cos(pi*v)

def norm(u, v):
    vec = [yu(u, v)*zv(u, v) - zu(u, v)*yv(u, v), zu(u, v)*xv(u, v) - xu(u, v)*zv(u, v), xu(u, v)*yv(u, v) - yu(u, v)*xv(u, v)]
    return normalized(neg(vec))

def neg(vec):
    return [-x for x in vec]

def length(vec):
    return sqrt(sum([x*x for x in vec]))

def normalized(vec):
    l = length(vec)
    if l==0:
        return vec
    return [x/l for x in vec]

def egg_strips():
    glColor3f(0.5, 0.5, 0.5)
    for i in range(N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N-1):
            # glColor3fv(colors[i][j])
            glNormal(*normals[i][j])
            glVertex3fv(vertices[i][j])
            # glColor3fv(colors[i+1][j])
            glNormal(*normals[i+1][j])
            glVertex3fv(vertices[i+1][j])
        # glColor3fv(colors[i][N-1])
        glNormal(*normals[i][N-1])
        glVertex3fv(vertices[i][N-1])
        # glColor3fv(colors[i+1][N-1])
        glNormal(*normals[i+1][N-1])
        glVertex3fv(vertices[i+1][N-1])
        glEnd()

def egg_normals():
    glColor3f(1.0, 0.0, 0.0)
    for i in range(N-1):
        glBegin(GL_LINES)
        for j in range(N-1):
            glVertex3fv(vertices[i][j])
            glVertex3fv([v+n for v, n in zip(vertices[i][j], normals[i][j])])
        glEnd()


def render(time):
    global theta
    global phi
    global R

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
        if phi > 180:
            phi -= 360
        if phi < -180:
            phi += 360
    
    light_position[0] = R*cos(theta*deg2rad)*cos(phi*deg2rad)
    light_position[1] = R*sin(phi*deg2rad)
    light_position[2] = R*sin(theta*deg2rad)*cos(phi*deg2rad)

    glTranslate(*light_position[:3])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 5, 6)
    gluDeleteQuadric(quadric)
    glTranslate(*[-x for x in light_position[:3]])
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    glRotatef(theta, 0.0, 1.0, 0.0)

    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 20, 20)
    # gluDeleteQuadric(quadric)

    glRotate(45, 1, 0, 0)
    egg_strips()
    egg_normals()

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
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


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

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
