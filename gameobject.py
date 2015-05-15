"""

  File that contains a game object, which is the general representation of an
  object.

"""

from OpenGL.GL import *
from pyrr import Matrix44 as mat4
from pyrr import Vector3 as vec3
from texture import activateTexture, loadTexture

class GameObject:

    def __init__(self, name=None, position=None, texImg=None, specTexImg=None,
            shininess=None, ka=None, kd=None, ks=None, program=None):
        self.model = mat4.identity(dtype='f')
        self.name = name
        self.position = position
        self.texImg = texImg
        self.specTexImg = specTexImg
        self.shininess = shininess
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.program = program
        self.initTextures()

    def initTextures(self):
        self.texture = loadTexture(self.texImg)
        self.specTex = loadTexture(self.specTexImg) if self.specTexImg else None

    def _bindTextures(self):
        # TODO: send some uniform to shader to inform it of textures passed
        activateTexture(self.texture, GL_TEXTURE0)
        if self.specTex:
            activateTexture(self.specTex, GL_TEXTURE1)

    def _sendLightningParameters(self):
        names = ["ka", "kd", "ks", "shininess"]
        kaLoc, kdLoc, ksLoc, shininessLoc = [glGetUniformLocation(self.program, name) for name in names]
        glUniform1f(kaLoc, self.ka)
        glUniform1f(kdLoc, self.kd)
        glUniform1f(ksLoc, self.ks)
        glUniform1f(shininessLoc, self.shininess)

    def draw(self, viewMatrix, projMatrix):
        glBindVertexArray(self.vao)

        modelMatrix = self.getModelMatrix()
        mvpMatrix = modelMatrix * viewMatrix * projMatrix
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mMatrix"), 1, GL_FALSE, modelMatrix)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mvpMatrix"), 1, GL_FALSE, mvpMatrix)

        self._bindTextures()
        self._sendLightningParameters()

        glDrawElements(GL_TRIANGLES, self.indexLen, GL_UNSIGNED_INT, None)

        glBindVertexArray(0)
