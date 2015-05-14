import sys
import cyglfw3 as glfw
from OpenGL.GL import *
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

def init():
    window = initWindow()
    program = shaderutil.createProgram('v.s', 'f.s')
    glUseProgram(program)

    vertices = [-0.5, -0.5, 0.0,
                -0.5, 0.5, 0.0,
                0.5, -0.5, 0.0]
    vertexData = np.array(vertices, np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 4 * 9, vertexData,
            GL_STATIC_DRAW)
    glVertexAttribPointer(glGetAttribLocation(program, "inPos"), 3,
            GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(glGetAttribLocation(program, "inPos"))
    glBindVertexArray(0)

    vertices = [0.5, 0.5, 0.0,
                -0.5, 0.5, 0.0,
                0.5, -0.5, 0.0]
    vertexData = np.array(vertices, np.float32)

    vao2 = glGenVertexArrays(1)
    glBindVertexArray(vao2)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 4 * 9, vertexData,
            GL_STATIC_DRAW)
    glVertexAttribPointer(glGetAttribLocation(program, "inPos"), 3,
            GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(glGetAttribLocation(program, "inPos"))
    glBindVertexArray(0)


    while not glfw.WindowShouldClose(window):
        glfw.SetCursorPos(window, 300.0, 200.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glBindVertexArray(vao2)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Swap front and back buffers
        glfw.SwapBuffers(window)

        # Poll for and process events
        glfw.PollEvents()

    glfw.Terminate()

if __name__ == '__main__':
    init()
