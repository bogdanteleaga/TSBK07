import sys
import cyglfw3 as glfw
import numpy as np
from objloader import *
from OpenGL.GL import glClear, glEnable, glUseProgram, glGetAttribLocation, glUniform3fv,\
    GL_DEPTH_TEST, GL_FALSE, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from shaderutil import Shader
from camera import getNewViewMatrixAndEye, lookAt
from init import initObjects
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4

VERSION = 3, 2
WIDTH = 1920    
HEIGHT = 1080


def initWindow():
    glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, VERSION[0])
    glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, VERSION[1])

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


def initCamera():
    eye = vec3([5, 5, 5], dtype='f')
    target = vec3([0, 0, 0], dtype='f')
    up = vec3([0, 1, 0], dtype='f')

    viewMatrix = lookAt(eye, target, up)

    return eye, viewMatrix

def initShaders():
    classicProgram = Shader('shaders/main.vert',
                            'shaders/main.frag')

    normalMapProgram = Shader('shaders/normalMapping.vert',
                              'shaders/normalMapping.frag')

    skyboxProgram = Shader('shaders/skybox.vert',
                           'shaders/skybox.frag')

    classicProgram.initializeAttribs("inPos", "inTex", "inNormal")
    classicProgram.initializeUniforms("mvpMatrix", "mMatrix", "ka", "kd", "ks",
                                      "shininess", "tex", "eye")

    normalMapProgram.initializeAttribs("inPos", "inTex", "inNormal", "inTan")
    normalMapProgram.initializeUniforms("mvpMatrix", "mMatrix", "ka", "kd",
                                        "ks", "shininess", "tex", "normalTex", "eye")

    skyboxProgram.initializeAttribs("inPos");
    skyboxProgram.initializeUniforms("vMatrix", "pMatrix", "tex")

    return classicProgram, normalMapProgram, skyboxProgram
 

def main():
    window = initWindow()
    classicProgram, normalMapProgram, skyboxProgram = initShaders()
    glEnable(GL_DEPTH_TEST)

    # Initialize objects
    planets, spaceship, skybox = initObjects(classicProgram, normalMapProgram,
                                             skyboxProgram)

    projMatrix = mat4.perspective_projection(60,
                                             float(WIDTH/HEIGHT),
                                             0.1,
                                             10000.0,
                                             dtype='f')
    eye, viewMatrix = initCamera()

    dt, oldTime = 0.0, glfw.GetTime()
    animation_speed = 800
    while not glfw.WindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        currentTime = glfw.GetTime()
        dt = currentTime - oldTime
        oldTime = currentTime

        hAngle, vAngle, eye, direction, right, up, viewMatrix, animation_speed = getNewViewMatrixAndEye(window,
                                                                  animation_speed,
                                                                  dt,
                                                                  eye,
                                                                  WIDTH,
                                                                  HEIGHT)

        skybox.draw(viewMatrix, projMatrix)
        for planet in planets:
            planet.update(animation_speed)
            planet.draw(eye, viewMatrix, projMatrix)

        spaceship.update(eye, direction, right, up, hAngle, vAngle)
        spaceship.draw(eye, viewMatrix, projMatrix)
        # Swap front and back buffers
        glfw.SwapBuffers(window)

        # Poll for and process events
        glfw.PollEvents()

    glfw.Terminate()

if __name__ == '__main__':
    main()
