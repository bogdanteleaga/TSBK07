from OpenGL.GL import *
import numpy as np
from OpenGL.arrays import vbo
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4

G = 6.67384e-11
METERS_PER_UNIT = 1000000000
SEC_PER_STEP = 8
STEPS_PER_FRAME = 5000

class Planet(GameObject):

    def __init__(self, name=None, origin=None, texImg=None, specTexImg=None,
            radius=None, parent=None, mass=None, velocity=None, distance=None,
            spin=None, shininess=None, ka=None, kd=None, ks=None):
        super(self, name, origin, texImg, specTexImg, shininess, ka, kd, ks)
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
        self.position = vec3([x, y, 0], dtype='f')

    def _initModel(self):
        latBands = 30
        longBands = 30

        vertexPos = []
        normals = []
        textureCoords = []

        for lat in range(latBands + 1):
            theta = lat * math.pi / latBands
            sinTheta = math.sin(theta)
            cosTheta = math.cos(theta)

            for lon in range(longBands + 1):
                phi = lon * 2 * math.pi / longBands
                sinPhi = math.sin(phi)
                cosPhi = math.cos(phi)

                x = cosPhi * sinTheta
                y = cosTheta
                z = sinPhi * cosTheta
                
                u = 1 - (lon / longBands)
                v = 1 - (lat / latBands)

                normals.append(x)
                normals.append(y)
                normals.append(z)

                vertexPos.append(x * self.radius)
                vertexPos.append(y * self.radius)
                vertexPos.append(z * self.radius)

                textureCoords.append(u)
                textureCoords.append(v)

            indexData = []
            for lat in range(latBands):
                for lon in range(longBands):
                    x = lat * (longBands + 1) + lon
                    y = x + longBands + 1

                    indexData.append(x)
                    indexData.append(y)
                    indexData.append(x + 1)

                    indexData.append(y)
                    indexData.append(y + 1)
                    indexData.append(x + 1)

            self.indexLen = len(indexData)
            self._initVAO(vertexPos, normals, textureCoords, indexData)

    def _initVAO(self, vertexPos, normals, textureCoords, indexData):
        names = ["inPos", "inNormal", "inTex"]
        posLoc, normalLoc, texLoc = [glGetAtrribLocation(program, name) for name in names]

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.posVBO = vbo.VBO(np.array(vertexPos, dtype='f'))
        self.posVBO.bind()
        glEnableVertexAttribArray(posLoc)
        glVertexAttribPointer(posLoc, 3, GL_FLOAT, GL_FALSE, 0, None)

        self.normalVBO = vbo.VBO(np.array(normals, dtype='f'))
        self.normalVBO.bind()
        glEnableVertexAttribArray(normalLoc)
        glVertexAttribPointer(posLoc, 3, GL_FLOAT, GL_FALSE, 0, None)

        self.texVBO = vbo.VBO(np.array(textureCoords, dtype='f'))
        self.texVBO.bind()
        glEnableVertexAttribArray(texLoc)
        glVertexAttribPointer(posLoc, 3, GL_FLOAT, GL_FALSE, 0, None)

        self.indexVBO = vbo.VBO(np.array(vertexPos, dtype=np.int32), target=GL_ELEMENT_ARRAY_BUFFER))
        self.indexVBO.bind()

        glBindVertexArray(0)



    def _acceleration(self, dist, mass):
        return G * mass / (dist * dist)

    def update(self):
        star = self.parent
        for i in range(STEPS_PER_FRAME):
            d = (self.position - star.position).length
            speed = self._acceleration(d * METERS_PER_UNIT, star.mass) * SEC_PER_STEP
            vel = (self.position - star.position).normalised * (speed / METERS_PER_UNIT)
            self.velocity += vel

            self.position += self.vel * SEC_PER_STEP

        self.spin += 0.001
        # TODO: maybe spin planet around another axis and add scaling
        rot = mat4.from_y_rotation(self.spin, dtype='f')
        trans = mat4.from_translation(self.position, dtype='f') 
        self.model = trans * rot


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
