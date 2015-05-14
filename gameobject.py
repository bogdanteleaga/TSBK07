"""

  File that contains a game object, which is the general representation of an
  object.

"""

from pyrr import Matrix44 as mat4
from pyrr import Vector3 as vec3

class GameObject:

    def __init__(self, name=None, position=None, texImg=None, specularTexImg=None, shininess=None, ka=None, kd=None, ks=None):
        self.model = mat4(dtype='f')
        self.name = name
        self.position = position
        self.texImg = texImg
        self.specularTexImg = specularTexImg
        self.shininess = shininess
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.initTextures()
        self.matrixPos = glGetAttribLocation(program, "mMatrix")

    def initTextures(self):
        self.texture = loadTexture(self.texImg)
        self.specTex = loadTexture(self.specularTexImg) if self.specularTexImg else None

    def _bindTextures(self):
        # TODO: send some uniform to shader to inform it of textures passed
        activateTexture(self.texture, GL_TEXTURE0)
        if self.specTex:
            activateTexture(self.specTex, GL_TEXTURE1)

    def _sendLightningParameters(self):
        # TODO: send lightning parameters to shader such as kd, ka, ks, shininess
        # It would be easier on the shader if everybody sent a value
        return

    def draw(self, program):
    
        glBindVertexArray(self.vao)

        glUniformMatrix4fv(self.matrixPos, 1, GL_FALSE, self.model)    

        self._bindTextures()
        self._sendLightningParameters()

        glDrawElements(GL_TRIANLES, self.indexLen, GL_UNSIGNED_INT, None)


