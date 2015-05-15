import sys
import pygame
from pygame.locals import *
from pygame.constants import *
#import cyglfw3 as glfw
from OpenGL.GL import *
from OpenGL.arrays import vbo
import shaderutil
import numpy as np

version = 3, 2
WIDTH = 640
HEIGHT = 480

def on_key(window, key, scancode, action, mods):
    if glfw.GetKey(window, glfw.KEY_W) == glfw.PRESS:
        print 'w'
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.SetWindowShouldClose(window, 1)

def on_mouse(window, x, y):
    print glfw.GetCursorPos(window)

def initWindow():
    glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, version[0])
    glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, version[1])

    if not glfw.Init():
        sys.exit()

    window = glfw.CreateWindow(WIDTH, HEIGHT, "Space Explorer", None, None)
    if not window:
        glfw.Terminate()
        sys.exit()

    # Make the window's context current
    glfw.MakeContextCurrent(window)

    # Install a key handler
    glfw.SetKeyCallback(window, on_key)
    glfw.SetCursorPosCallback(window, on_mouse)
    glfw.SetInputMode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    return window

def initPygame():
    pygame.display.set_mode((WIDTH, HEIGHT), OPENGL|DOUBLEBUF)

def init():
    #window = initWindow()
    initPygame()
    program = shaderutil.createProgram('shaders/old.vert', 'shaders/old.frag')
    glUseProgram(program)

    vertices = [-0.5, -0.5, 0.0,
                -0.5, 0.5, 0.0,
                0.5, -0.5, 0.0]
    vertexData = np.array(vertices, dtype='f')
    indices = [0,1,2]
    indexData = np.array(indices, dtype='uint32')

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vBuffer = vbo.VBO(vertexData)
    vBuffer.bind()
    glEnableVertexAttribArray(glGetAttribLocation(program, "inPos"))
    glVertexAttribPointer(glGetAttribLocation(program, "inPos"), 3,
            GL_FLOAT, GL_FALSE, 0, None)

    iBuffer = vbo.VBO(indexData, target=GL_ELEMENT_ARRAY_BUFFER)
    iBuffer.bind()
    glBindVertexArray(0)

    vertices = [0.5, 0.5, 0.0,
                -0.5, 0.5, 0.0,
                0.5, -0.5, 0.0]
    vertexData = np.array(vertices, np.float32)

    vao2 = glGenVertexArrays(1)
    glBindVertexArray(vao2)

    vBuffer = vbo.VBO(vertexData)
    vBuffer.bind()
    glEnableVertexAttribArray(glGetAttribLocation(program, "inPos"))
    glVertexAttribPointer(glGetAttribLocation(program, "inPos"), 3,
            GL_FLOAT, GL_FALSE, 0, None)
    glBindVertexArray(0)


    #while not glfw.WindowShouldClose(window):
    while 1:
        #glfw.SetCursorPos(window, 300.0, 200.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)

        glBindVertexArray(vao2)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Swap front and back buffers
        #glfw.SwapBuffers(window)
        pygame.display.flip()

        # Poll for and process events
        #glfw.PollEvents()
        pygame.time.wait(10)

    #glfw.Terminate()

if __name__ == '__main__':
    init()
