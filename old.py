import sys
import cyglfw3 as glfw
from OpenGL.GL import *
from OpenGL.arrays import vbo
import shaderutil
import numpy as np
from pyrr import Matrix44 as mat4
from pyrr import Vector3 as vec3
import camera

version = 3, 2
WIDTH = 1920.0
HEIGHT = 1080.0

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

def initCamera():
    eye = vec3([3,3,3], dtype='f')
    target = vec3([0,0,-4], dtype='f')
    up = vec3([0,1,0], dtype='f')

    viewMatrix = camera.lookAt(eye, target, up)

    return eye, viewMatrix

def init():
    window = initWindow()
    program = shaderutil.createProgram('shaders/old.vert', 'shaders/old.frag')
    glUseProgram(program)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    vertices = [
    # front
    -1.0, -1.0,  1.0,
     1.0, -1.0,  1.0,
     1.0,  1.0,  1.0,
    -1.0,  1.0,  1.0,
    # back
    -1.0, -1.0, -1.0,
     1.0, -1.0, -1.0,
     1.0,  1.0, -1.0,
    -1.0,  1.0, -1.0,
    ]
    vertexData = np.array(vertices, dtype='f')
    indices = [
        # front
        0, 1, 2,
        2, 3, 0,
        # top
        3, 2, 6,
        6, 7, 3,
        # back
        7, 6, 5,
        5, 4, 7,
        # bottom
        4, 5, 1,
        1, 0, 4,
        # left
        4, 0, 3,
        3, 7, 4,
        # right
        1, 5, 6,
        6, 2, 1,
    ]
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

    vertices = [
    -0.3,-0.3,-0.3,
    -0.3,-0.3, 0.3,
    -0.3, 0.3, 0.3,
    0.3, 0.3,-0.3,
    -0.3,-0.3,-0.3,
    -0.3, 0.3,-0.3,
    0.3,-0.3, 0.3,
    -0.3,-0.3,-0.3,
    0.3,-0.3,-0.3,
    0.3, 0.3,-0.3,
    0.3,-0.3,-0.3,
    -0.3,-0.3,-0.3,
    -0.3,-0.3,-0.3,
    -0.3, 0.3, 0.3,
    -0.3, 0.3,-0.3,
    0.3,-0.3, 0.3,
    -0.3,-0.3, 0.3,
    -0.3,-0.3,-0.3,
    -0.3, 0.3, 0.3,
    -0.3,-0.3, 0.3,
    0.3,-0.3, 0.3,
    0.3, 0.3, 0.3,
    0.3,-0.3,-0.3,
    0.3, 0.3,-0.3,
    0.3,-0.3,-0.3,
    0.3, 0.3, 0.3,
    0.3,-0.3, 0.3,
    0.3, 0.3, 0.3,
    0.3, 0.3,-0.3,
    -0.3, 0.3,-0.3,
    0.3, 0.3, 0.3,
    -0.3, 0.3,-0.3,
    -0.3, 0.3, 0.3,
    0.3, 0.3, 0.3,
    -0.3, 0.3, 0.3,
    0.3,-0.3, 0.3
    ]

    vertexData = np.array(vertices, np.float32)

    vao2 = glGenVertexArrays(1)
    glBindVertexArray(vao2)

    vBuffer = vbo.VBO(vertexData)
    vBuffer.bind()
    glEnableVertexAttribArray(glGetAttribLocation(program, "inPos"))
    glVertexAttribPointer(glGetAttribLocation(program, "inPos"), 3,
            GL_FLOAT, GL_FALSE, 0, None)
    glBindVertexArray(0)
    eye, viewMatrix = initCamera()

    dt, oldTime = 0.0, 0.0
    while not glfw.WindowShouldClose(window):
        #glfw.SetCursorPos(window, 300.0, 200.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        currentTime = glfw.GetTime()
        dt = currentTime - oldTime
        oldTime = currentTime

        mvpLoc = glGetUniformLocation(program, "mvpMatrix")
        #modelMatrix = mat4.from_translation(vec3([0,0, -2]), dtype='f') * mat4.from_y_rotation(10, dtype='f')
        modelMatrix = mat4.from_scale(vec3([0.8, 0.8, 0.8]), dtype='f') *\
        mat4.from_y_rotation(currentTime, dtype='f') *\
        mat4.from_x_rotation(currentTime, dtype='f') *\
        mat4.from_translation(vec3([0,0, -4]), dtype='f') 
        projMatrix = mat4.perspective_projection(60, 16.0/9.0, 0.1, 10000.0, dtype='f')
        eye, viewMatrix = camera.getNewViewMatrixAndEye(window, dt, eye, WIDTH, HEIGHT)

        glUniformMatrix4fv(mvpLoc, 1, GL_FALSE, modelMatrix * viewMatrix * projMatrix)


        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, len(indexData), GL_UNSIGNED_INT, None)

        #glDrawArrays(GL_TRIANGLES, 0, 12*3)

        # Swap front and back buffers
        glfw.SwapBuffers(window)

        # Poll for and process events
        glfw.PollEvents()

    glfw.Terminate()

if __name__ == '__main__':
    init()
