import sys
import cyglfw3 as glfw
import numpy as np

from OpenGL.GL import glClear, glEnable, glUseProgram, glGetAttribLocation, glUniform3fv,\
    GL_DEPTH_TEST, GL_FALSE, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from shaderutil import createProgram
from camera import getNewViewMatrixAndEye, lookAt
from planet import Planet, Sun
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


def initPlanets(classicProgram, normalMapProgram):

    sun = Sun(name="Sun",
              position=vec3([0, 0, 0]),
              texImg="textures/sun.jpg",
              radius=17.25,
              mass=1.988435e30,
              spin=0,
              shininess=30,
              ka=1.0,
              kd=0.9,
              ks=0.6,
              program=classicProgram)

    mercury = Planet(name="Mercury",
                     parent=sun,
                     texImg="textures/mercury.jpg",
                     radius=2.4,
                     mass=3.30104e23,
                     velocity=vec3([0, 0, 4.74e-5]),
                     distance=50.32,
                     spin=0,
                     shininess=30,
                     ka=0.5,
                     kd=0.9,
                     ks=0.6,
                     program=classicProgram)

    venus = Planet(name="Venus",
                   parent=sun,
                   texImg="textures/venus.jpg",
                   normalMap="textures/venusnormal.png",
                   radius=6.0,
                   mass=4.86732e24,
                   velocity=vec3([0, 0, 3.5e-5]),
                   distance=108.0,
                   spin=0,
                   shininess=30,
                   ka=0.5,
                   kd=0.9,
                   ks=0.6,
                   program=normalMapProgram)

    earth = Planet(name="Earth",
                   parent=sun,
                   texImg="textures/earth.png",
                   normalMap="textures/earthnormal.png",
                   radius=6.3,
                   mass=5.9722e24,
                   velocity=vec3([0, 0, 2.963e-5]),
                   distance=150,
                   spin=0,
                   shininess=30,
                   ka=0.5,
                   kd=0.9,
                   ks=0.6,
                   program=normalMapProgram)

    mars = Planet(name="Mars",
                  parent=sun,
                  texImg="textures/mars.png",
                  normalMap="textures/marsnormal.png",
                  radius=3.3,
                  mass=6.41693e23,
                  velocity=vec3([0, 0, 2.228175e-5]),
                  distance=227.94,
                  spin=0,
                  shininess=30,
                  ka=0.5,
                  kd=0.9,
                  ks=0.6,
                  program=normalMapProgram)

    return [sun, mercury, venus, earth, mars]

def initCamera():
    eye = vec3([5, 5, 5], dtype='f')
    target = vec3([0, 0, 0], dtype='f')
    up = vec3([0, 1, 0], dtype='f')

    viewMatrix = lookAt(eye, target, up)

    return eye, viewMatrix


def main():
    window = initWindow()
    classicProgram = createProgram('shaders/main.vert', 'shaders/main.frag')
    normalMapProgram = createProgram('shaders/normalMapping.vert',
            'shaders/normalMapping.frag')
    glEnable(GL_DEPTH_TEST)

    # Initialize objects
    planets = initPlanets(classicProgram, normalMapProgram)

    projMatrix = mat4.perspective_projection(60,
                                             float(WIDTH/HEIGHT),
                                             0.1,
                                             10000.0,
                                             dtype='f')

    eye, viewMatrix = initCamera()

    dt, oldTime = 0.0, glfw.GetTime()
    while not glfw.WindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        currentTime = glfw.GetTime()
        dt = currentTime - oldTime
        oldTime = currentTime

        eye, viewMatrix = getNewViewMatrixAndEye(window,
                                                 dt,
                                                 eye,
                                                 WIDTH,
                                                 HEIGHT)

        for planet in planets:
            planet.update()

            planet.draw(eye, viewMatrix, projMatrix)

        # Swap front and back buffers
        glfw.SwapBuffers(window)

        # Poll for and process events
        glfw.PollEvents()

    glfw.Terminate()

if __name__ == '__main__':
    main()
