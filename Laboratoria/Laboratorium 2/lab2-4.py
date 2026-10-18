#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

random.seed(None,2)
randomColor = [random.random(),random.random(),random.random()] # losowanie koloru

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


# funkcja generujaca rekurencyjnie kolejne wyciecia
def carpetStep(n, i, origin_size, old_x, old_y, shift):

    origin_size /= 3 # pomniejszenie rozmiarow bokow nastepnych kwadratow

    create_rectangle_white(old_x-shift, old_y, origin_size/3, origin_size/3)
    create_rectangle_white(old_x-shift, old_y+shift, origin_size/3, origin_size/3)
    create_rectangle_white(old_x, old_y+shift, origin_size/3, origin_size/3)
    create_rectangle_white(old_x+shift, old_y+shift, origin_size/3, origin_size/3)
    create_rectangle_white(old_x+shift, old_y, origin_size/3, origin_size/3)
    create_rectangle_white(old_x+shift, old_y-shift, origin_size/3, origin_size/3)
    create_rectangle_white(old_x, old_y-shift, origin_size/3, origin_size/3)
    create_rectangle_white(old_x-shift, old_y-shift, origin_size/3, origin_size/3)

    if not i == n: # jezeli brakuje kwadratow, to generuj dla kazdego poprzedniego kwadratu kolejne kwadraty
        carpetStep(n, i+1, origin_size, old_x-shift, old_y, shift/3)
        carpetStep(n, i+1, origin_size, old_x-shift, old_y+shift, shift/3)
        carpetStep(n, i+1, origin_size, old_x, old_y+shift, shift/3)
        carpetStep(n, i+1, origin_size, old_x+shift, old_y+shift, shift/3)
        carpetStep(n, i+1, origin_size, old_x+shift, old_y, shift/3)
        carpetStep(n, i+1, origin_size, old_x+shift, old_y-shift, shift/3)
        carpetStep(n, i+1, origin_size, old_x, old_y-shift, shift/3)
        carpetStep(n, i+1, origin_size, old_x-shift, old_y-shift, shift/3)
    
# funkcja rysujaca dywan Sierpińskiego (wersja z wycieciami)
def sierpinskiCarpet(n): # n - stopien samopodobienstwa
    origin_size = 180 # rozmiar pierwotnego prostokata (kwadratru)
    create_rectangle(0,0,origin_size,origin_size) # kwadrat startowy (dla n >= 0)
    
    if n > 0: # pierwsze wyciecie
        create_rectangle_white(0,0,origin_size/3,origin_size/3)
        old_x = 0
        old_y = 0
        shift = origin_size/3

    if n > 1: # kolejne wyciecia
        i = 2
        carpetStep(n, i, origin_size, old_x, old_y, shift) # rekurencyjne generowanie wyciec


# funkcja rysujaca BIALY prostokat (wersja origin point)
def create_rectangle_white(x, y, a, b, d = 0.0):
    
    a = a*(1+d) # deformacja wysokosci
    b = b*(1+d) # deformacja szerokosci
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x-b/2, y-a/2)
    glVertex2f(x-b/2, y+a/2)
    glVertex2f(x+b/2, y-a/2)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+b/2, y+a/2)
    glVertex2f(x-b/2, y+a/2)
    glVertex2f(x+b/2, y-a/2)
    glEnd()


# funkcja rysujaca prostokat (wersja origin point)
def create_rectangle(x, y, a, b, d = 0.0):
    
    a = a*(1+d) # deformacja wysokosci
    b = b*(1+d) # deformacja szerokosci
    glBegin(GL_TRIANGLES)
    glColor3f(randomColor[0], randomColor[1], randomColor[2]) # losowy kolor
    glVertex2f(x-b/2, y-a/2)
    glVertex2f(x-b/2, y+a/2)
    glVertex2f(x+b/2, y-a/2)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+b/2, y+a/2)
    glVertex2f(x-b/2, y+a/2)
    glVertex2f(x+b/2, y-a/2)
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    sierpinskiCarpet(5) # generowanie dywanu Sierpinskiego o zadanym stopniu samopodobienstwa

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
