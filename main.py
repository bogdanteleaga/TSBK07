import sys
import cyglfw3 as glfw
from OpenGL.GL import *
import shaders
from matrices import *
import numpy as np
import camera

version = 3, 2
WIDTH = 1920
HEIGHT = 1080

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
    glfw.SetInputMode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    return window

def initObjects():
    return

def initCamera():
    eye = vec3([5,5,5], dtype='f')
    target = vec3([0,0,0], dtype='f')
    up = vec3([0,1,0], dtype='f')

    viewMatrix = camera.lookAt(eye, target, up)

    return eye, viewMatrix

def main():
    window = initWindow()
    program = shaders.loadProgram('proj.vs', 'proj.fs')
    glUseProgram(program)

    # Initialize objects
    objects = initObjects()
    projMatrix = mat4.perspective_projection(FoV, float(width/height), 1.0, 1000.0, dtype='f')
    pMatrixPos = glGetAttribLocation(program, "pMatrix")
    vMatrixPos = glGetAttribLocation(program, "pMatrix")
    eyePos = glGetAttribLocation(program, "pMatrix")
    glUniform4fv(pMatrixPos, 1, GL_FALSE, projMatrix)

    eye, viewMatrix = initCamera()

    dt, oldtime = 0.0, 0.0
    while not glfw.WindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        currentTime = time.time()
        dt = currentTime - oldTime
        oldTime = currentTime

        eye, viewMatrix = getNewViewMatrixAndEye(window, dt, eye, WIDTH, HEIGHT)
        glUniform4v(vMatrixPos, 1, GL_FALSE, viewMatrix)
        glUniform3f(eyePos, 1, GL_FALSE, eye)

        for obj in objects:
            obj.update()
            obj.draw(program)

        # Swap front and back buffers
        glfw.SwapBuffers(window)

        # Poll for and process events
        glfw.PollEvents()

    glfw.Terminate()

if __name__ == '__main__':
    main()
