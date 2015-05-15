from OpenGL.GL import *
import numpy as np
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4
from buffers import initializeVAO
from geometry import createSphereCoords
from gameobject import GameObject
import random
import math

G = 6.67384e-11
METERS_PER_UNIT = 1000000000
SEC_PER_STEP = 800
STEPS_PER_FRAME = 50

class Planet(GameObject):

    def __init__(self, name=None, position=None, texImg=None, specTexImg=None,
            radius=None, parent=None, mass=None, velocity=None, distance=None,
            spin=None, shininess=None, ka=None, kd=None, ks=None,
            program=None):
        GameObject.__init__(self, name=name, position=position, texImg=texImg,
                specTexImg=specTexImg, shininess=shininess, ka=ka, kd=kd,
                ks=ks, program=program)
        self.parent = parent
        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        self.distance = distance
        self.spin = spin
        self._setRandomStartingPoint()
        self._initModel()

    def _setRandomStartingPoint(self):
        angle = random.randint(0, 360)
        x = self.distance * math.cos(angle)
        y = self.distance * math.sin(angle)
        self.position = vec3([x, y, 0])
    def _initModel(self):
        vertexPos, normals, textureCoords, indexData = createSphereCoords(self.radius)
        self.vao = initializeVAO(self.program, vertexPos, normals, textureCoords, indexData)
        self.indexLen = len(indexData)

    def _acceleration(self, dist, mass):
        return G * mass / (dist * dist)

    def update(self):
        star = self.parent
        for i in range(STEPS_PER_FRAME):
            d = (self.position - star.position).length
            speed = self._acceleration(d * METERS_PER_UNIT, star.mass) * SEC_PER_STEP
            vel = (star.position - self.position).normalised * (speed / METERS_PER_UNIT)
            self.velocity += vel

            self.position += self.velocity * SEC_PER_STEP

        self.spin += 0.001

    def getModelMatrix(self):
        # TODO: maybe spin planet around another axis and add scaling
        #rot = mat4.from_y_rotation(self.spin, dtype='f')
        trans = mat4.from_translation(self.position, dtype='f')
        return trans

class Sun(GameObject):

    def __init__(self, name=None, position=None, texImg=None, specTexImg=None, radius=None,
                       mass=None, spin=None, shininess=None, ka=None, kd=None,
                       ks=None, program=None):
        GameObject.__init__(self, name=name, position=position, texImg=texImg,
                specTexImg=specTexImg, shininess=shininess, ka=ka, kd=kd,
                ks=ks, program=program)
        self.radius = radius
        self.mass = mass
        self.spin = spin
        self._initModel()

    def _initModel(self):
        vertexPos, normals, textureCoords, indexData = createSphereCoords(self.radius)
        self.vao = initializeVAO(self.program, vertexPos, normals, textureCoords, indexData)
        self.indexLen = len(indexData)

    def update(self):
        self.spin += 0.001

    def getModelMatrix(self):
        # TODO: re-enable spin once it shows up
        rot = mat4.from_y_rotation(self.spin, dtype='f')
        trans = mat4.from_translation(self.position, dtype='f')
        return trans
"""
Maybe do a map for every attribute and the name that it has in the shader. Making it the same would be easier though.

Mesh is done
Drawing is semi-done:
    - need to handle textures
    - need to handle shininess and kd,ke,etc stuff

Need to think about light in the scene(probably will just be one)

Implement update method for physics.

Then:
    - Instantiate sun
    - Instantiate planets with proper data
    - Everything is in a gameobj list
    - Iterate through list and call update and draw
    - Everything works?

- Should be able to take out draw in the other class, since it should work for everything
- Buffers should also be in some sort of geometry location, we only use vbos here
- The update method is probably the only thing that differentiates the planet from everything else (that is the model matrix)

- For the ship:
    - It should still have everything we give need in draw. So it should implement an update method and a proper initVBOs method(initVBOS should probably take some sort of geometry but this is not completely clear at this point)


Still left besides whats above:
g    - Camera. There is a prototype in that guys tutorial that follows exactly what I did in C
half    - Projection. I guess it is not that important. Both camera and projection probably belong to a scene.
g    - Handle mouse events somehow

"""
