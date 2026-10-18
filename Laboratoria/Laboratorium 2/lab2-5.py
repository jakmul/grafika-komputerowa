#!/usr/bin/env python3
import sys
import random
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

random.seed(None,2)

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def wFunction(x):   # funkcja logistyczna dla koloru w srodku boku
    return 0.500062 / (1 + math.exp(0.06*(x-45)))

def wCFunction(x):  # funkcja logistyczna dla koloru w srodku kwadratu
    return 0.250031 / (1 + math.exp(0.06*(x-45)))


def newColorMiddle(x,c1,c2):    # kolor w srodku boku
    return (1-2*wFunction(x))*random.random()+wFunction(x)*c1+wFunction(x)*c2


def newColorCenter(x,c1,c2,c3,c4):  # kolor w srodku boku
    return (1-4*wCFunction(x))*random.random()+wCFunction(x)*c1+wCFunction(x)*c2+wCFunction(x)*c3+wCFunction(x)*c4


def middlePoint(x, y, c1, c2, width):   # punkt w srodku boku

    glBegin(GL_POINTS)
    newColor = newColorMiddle(width,c1,c2)
    glColor3f(newColor, newColor, newColor) # losowy kolor
    glVertex2f(x, y)
    glEnd()
    return newColor

def centralPoint(x, y, c1, c2, c3, c4, width):  # punkt w srodku kwadratu

    glBegin(GL_POINTS)
    newColor = newColorCenter(width,c1,c2,c3,c4)
    glColor3f(newColor, newColor, newColor) # losowy kolor
    glVertex2f(x, y)
    glEnd()
    return newColor

# funkcja generujaca kwadraty fraktala plazmowego
def create_rectangle(x, y, n, c1, c2, c3, c4):

    c12 = middlePoint(x, y-n/2, c1, c2, n/2) # dolny kolor
    c23 = middlePoint(x+n/2, y, c2, c3, n/2) # prawy kolor
    c34 = middlePoint(x, y+n/2, c3, c4, n/2) # gorny kolor
    c41 = middlePoint(x-n/2, y, c4, c1, n/2) # lewy kolor

    c5 = centralPoint(x, y, c1, c2, c3, c4, n/2) # srodkowy kolor

    if (n-n/4)>1.00 :
        create_rectangle(x+n/4, y+n/4, n/2, c5, c23, c3, c34) # prawy gorny kwadrat
        create_rectangle(x-n/4, y+n/4, n/2, c41, c5, c34, c4) # lewy gorny kwadrat
        create_rectangle(x+n/4, y-n/4, n/2, c12, c2, c23, c5) # prawy dolny kwadrat
        create_rectangle(x-n/4, y-n/4, n/2, c1, c12, c5, c41) # lewy dolny kwadrat


# funkcja generujaca fraktal plazmowy (monochromatyczny, skala szarosci)
def plasmaFractal(x, y, n, d = 0.0):
    
    c1 = random.random() # lewy dolny kolor
    c2 = random.random() # prawy dolny kolor
    c3 = random.random() # prawy gorny kolor
    c4 = random.random() # lewy gorny kolor

    n = n*(1+d) # deformacja rozmiaru

    glBegin(GL_POINTS)
    glColor3f(c1, c1, c1) # losowy kolor
    glVertex2f(x-n/2, y-n/2)
    glEnd()

    glBegin(GL_POINTS)
    glColor3f(c2, c2, c2) # losowy kolor
    glVertex2f(x+n/2, y-n/2)
    glEnd()

    glBegin(GL_POINTS)
    glColor3f(c3, c3, c3) # losowy kolor
    glVertex2f(x+n/2, y+n/2)
    glEnd()

    glBegin(GL_POINTS)
    glColor3f(c4, c4, c4) # losowy kolor
    glVertex2f(x-n/2, y+n/2)
    glEnd()

    create_rectangle(x, y, n, c1, c2, c3, c4)



def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    plasmaFractal(0,0,64) # fraktal plazmowy (zad.2.1)

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

    window = glfwCreateWindow(400, 400, __file__, None, None)
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
