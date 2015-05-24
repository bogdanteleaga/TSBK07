from OpenGL.GL import *
import numpy as np
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4
from buffers import initializeVAO
from gameobject import GameObject
from objloader import loadObj
import random
import math

class Spaceship(GameObject):

  def __init__(self, filename=None,  program=None, texImg=None, specTexImg=None,
               normalMap=None, shininess=None, ka=None, kd=None, ks=None):
        GameObject.__init__(self, name=None, position=None, texImg=texImg,
                            specTexImg=specTexImg, normalMap=normalMap,
                            shininess=shininess, ka=ka, kd=kd, ks=ks, 
                            program=program)
        self.vertices, self.normals, self.texCoords = loadObj(filename)

        self._initModel()

  def _initModel(self):
      self.vao = initializeVAO(self.program, self.vertices,
                               self.texCoords, self.normals)
      self.count = len(self.vertices) / 3
      
  def drawCall(self):
      glDrawArrays(GL_TRIANGLES, 0, self.count)
			       
  def getModelMatrix(self):
      scale = mat4.from_scale([0.2, 0.2, 0.2])
      roty = mat4.from_y_rotation(-self.hAngle)
      rotx = mat4.from_x_rotation(self.vAngle)
      trans = mat4.from_translation(self.position, dtype='f')
      return scale * rotx * roty * trans
	
  def update(self, eye, target, right, up, hAngle, vAngle):
      self.vAngle = vAngle
      self.hAngle = hAngle
      self.position = eye + target.normalised * 7 + up.normalised * -2
