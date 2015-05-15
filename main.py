import sys
import time
import cyglfw3 as glfw
from OpenGL.GL import *
import shaderutil
import numpy as np
import camera
import planet
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4

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
    #glfw.SetInputMode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    return window

def initPlanets(program):
    sun = planet.Sun(name="Sun",
                     position=vec3([0,0,0]),
                     texImg="textures/sun.jpg",
                     radius=37.25,
                     mass=1.988435e30,
                     spin=0,
                     shininess=30,
                     ka=0.01,
                     kd=0.9,
                     ks=0.6,
                     program=program)

    earth = planet.Planet(name="Earth",
                          parent=sun,
                          texImg="textures/earth.jpg",
                          radius=20,
                          mass=5.9722e24,
                          velocity=vec3([0,0,-2.963e-5]),
                          distance=150,
                          spin=0,
                          shininess=30,
                          ka=0.1,
                          kd=0.9,
                          ks=0.6,
                          program=program)

    return [sun, earth]

def initCamera():
    eye = vec3([5,5,5], dtype='f')
    target = vec3([0,0,0], dtype='f')
    up = vec3([0,1,0], dtype='f')

    viewMatrix = camera.lookAt(eye, target, up)

    return eye, viewMatrix

def main():
    window = initWindow()
    program = shaderutil.createProgram('shaders/main.vert', 'shaders/main.frag')
    glEnable(GL_DEPTH_TEST)

    # Initialize objects
    planets = initPlanets(program)

    mvpMatrixPos = glGetUniformLocation(program, "mvpMatrix")
    projMatrix = mat4.perspective_projection(60, float(WIDTH/HEIGHT), 0.1, 10000.0, dtype='f')
    eyePos = glGetAttribLocation(program, "eye")

    eye, viewMatrix = initCamera()

    dt, oldTime = 0.0, glfw.GetTime()
    while not glfw.WindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(program)

        currentTime = glfw.GetTime()
        dt = currentTime - oldTime
        oldTime = currentTime

        eye, viewMatrix = camera.getNewViewMatrixAndEye(window, dt, eye, WIDTH, HEIGHT)
        glUniform3fv(eyePos, 1, GL_FALSE, eye)

        for planet in planets:
            planet.update()

            #mvpMatrix = projMatrix * viewMatrix * planet.getModelMatrix()
            mvpMatrix = planet.getModelMatrix() * viewMatrix * projMatrix
            glUniformMatrix4fv(mvpMatrixPos, 1, GL_FALSE, mvpMatrix)

            planet.draw()

        # Swap front and back buffers
        glfw.SwapBuffers(window)

        # Poll for and process events
        glfw.PollEvents()

    glfw.Terminate()

if __name__ == '__main__':
    main()
