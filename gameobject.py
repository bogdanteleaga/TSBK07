"""

  File that contains a game object, which is the general representation of an
  object.

"""

from OpenGL.GL import *
from pyrr import Matrix44 as mat4
from texture import activateTexture, loadTexture


class GameObject:

    def __init__(self, name=None, position=None, texImg=None, specTexImg=None,
                 normalMap=None, shininess=None, ka=None, kd=None, ks=None,
                 program=None):
        self.model = mat4.identity(dtype='f')
        self.name = name
        self.position = position
        self.texImg = texImg
        self.specTexImg = specTexImg
        self.normalMap = normalMap
        self.shininess = shininess
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.program = program
        self.initTextures()

    def initTextures(self):
        self.texture = loadTexture(self.texImg, self.program) if self.texImg else None
        self.specTex = loadTexture(self.specTexImg, self.program) if self.specTexImg else None
        self.normalTex = loadTexture(self.normalMap, self.program) if self.normalMap else None

    def _bindTextures(self):
        if self.texture:
            activateTexture(self.texture, GL_TEXTURE0, self.program, "tex", 0)
        if self.normalTex:
            activateTexture(self.normalTex, GL_TEXTURE1, self.program,
            "normalTex", 1)
        # Will probably drop specular map?
        if self.specTex:
            activateTexture(self.specTex, GL_TEXTURE1, self.program)

    def _sendLightningParameters(self):
        names = ["ka", "kd", "ks", "shininess"]
        kaLoc, kdLoc, ksLoc, shininessLoc = [glGetUniformLocation(self.program, name) for name in names]
        glUniform1f(kaLoc, self.ka)
        glUniform1f(kdLoc, self.kd)
        glUniform1f(ksLoc, self.ks)
        glUniform1f(shininessLoc, self.shininess)

    def drawCall(self):
        glDrawElements(GL_TRIANGLES, self.indexLen, GL_UNSIGNED_INT, None)

    def draw(self, eye, viewMatrix, projMatrix):
        glUseProgram(self.program)
        glBindVertexArray(self.vao)

        eyePos = glGetAttribLocation(self.program, "eye")
        glUniform3fv(eyePos, 1, GL_FALSE, eye)

        modelMatrix = self.getModelMatrix()
        mvpMatrix = modelMatrix * viewMatrix * projMatrix
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mMatrix"), 1,
                           GL_FALSE, modelMatrix)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mvpMatrix"), 1,
                           GL_FALSE, mvpMatrix)

        self._bindTextures()
        self._sendLightningParameters()

        self.drawCall()

        glBindVertexArray(0)
        glUseProgram(0)
