from OpenGL.GL import *
import numpy as np
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4
from buffers import initializeVAO
from geometry import createSphereCoords, generateTangents
from gameobject import GameObject
import random
import math

G = 6.67384e-11
METERS_PER_UNIT = 1000000000
SEC_PER_STEP = 800
STEPS_PER_FRAME = 50
SEC_PER_DAY = 24.0 * 60.0 * 60.0

class Planet(GameObject):

    def __init__(self, name=None, position=None, texImg=None, specTexImg=None,
                 normalMap=None, radius=None, parent=None, mass=None,
                 velocity=None, distance=None, spin=None, shininess=None,
                 ka=None, kd=None, ks=None, program=None):
        GameObject.__init__(self, name=name, position=position, texImg=texImg,
                            specTexImg=specTexImg, normalMap=normalMap,
                            shininess=shininess, ka=ka, kd=kd,
                            ks=ks, program=program)
        self.parent = parent
        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        self.distance = distance
        self.spin = spin
        self.rot = 0
        self._setRandomStartingPoint()
        self._initModel()

    def _setRandomStartingPoint(self):
        # Using angle will place the planets on different planes
        #angle = random.randint(0, 360)
        x = self.distance * math.cos(0)
        y = self.distance * math.sin(0)
        self.position = vec3([x, y, 0]) + self.parent.position

    def _initModel(self):
        vertexPos, normals, textureCoords, indexData = createSphereCoords(self.radius)
        if self.normalMap:
            tangents = generateTangents(vertexPos, textureCoords, indexData)
            self.vao = initializeVAO(self.program, vertexPos, normals,
                                     textureCoords, indexData, tangents)
        else:
            self.vao = initializeVAO(self.program, vertexPos, normals,
                                     textureCoords, indexData)
        self.indexLen = len(indexData)

    def _acceleration(self, dist, mass):
        return G * mass / (dist * dist)

    def update(self, sec_per_step):
        star = self.parent
        for i in range(STEPS_PER_FRAME):
            d = (self.position - star.position).length
            speed = self._acceleration(d * METERS_PER_UNIT, star.mass) * sec_per_step
            vel = (star.position - self.position).normalised * (speed / METERS_PER_UNIT)
            self.velocity += vel

            self.position += self.velocity * sec_per_step

        sec_per_frame = sec_per_step * STEPS_PER_FRAME
        self.rot += sec_per_frame / (self.spin * SEC_PER_DAY) 

    def getModelMatrix(self):
        # TODO: maybe spin planet around another axis and add scaling
        rot = mat4.from_y_rotation(self.rot, dtype='f')
        trans = mat4.from_translation(self.position, dtype='f')
        return rot * trans


class Sun(GameObject):

    def __init__(self, name=None, position=None, texImg=None, specTexImg=None,
                 normalMap=None, radius=None, mass=None, spin=None, shininess=None,
                 ka=None, kd=None, ks=None, program=None):
        GameObject.__init__(self, name=name, position=position, texImg=texImg,
                            specTexImg=specTexImg, normalMap=None,
                            shininess=shininess, ka=ka, kd=kd, ks=ks,
                            program=program)
        self.velocity = vec3([0,0,0])
        self.radius = radius
        self.mass = mass
        self.spin = spin
        self.rot = 0
        self._initModel()

    def _initModel(self):
        vertexPos, normals, textureCoords, indexData = createSphereCoords(self.radius)
        self.vao = initializeVAO(self.program, vertexPos, normals, textureCoords, indexData)
        self.indexLen = len(indexData)

    def update(self, sec_per_step):
        sec_per_frame = sec_per_step * STEPS_PER_FRAME
        self.rot += sec_per_frame / (self.spin * SEC_PER_DAY) 

    def getModelMatrix(self):
        rot = mat4.from_y_rotation(self.rot, dtype='f')
        trans = mat4.from_translation(self.position, dtype='f')
        return rot * trans

class Cube(GameObject):
    """
    Used for testing purposes only.
    """

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
        vertexPos = [
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
        normals = [
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

        textureCoords = [
        0.0, 0.0,
        0.1, 0.1,
        0.2, 0.2,
        0.3, 0.3,
        0.4, 0.4,
        0.5, 0.5,
        0.6, 0.6,
        0.7, 0.7
        ]
        indexData = [
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

        self.vao = initializeVAO(self.program, vertexPos, normals, textureCoords, indexData)
        self.indexLen = len(indexData)

    def update(self):
        return

    def getModelMatrix(self):
        return mat4.identity(dtype='f')
