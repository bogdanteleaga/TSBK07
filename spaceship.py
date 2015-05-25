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
      scale = mat4.from_scale([0.3, 0.3, 0.3])
      trans = mat4.from_translation(self.position, dtype='f')
      return scale * trans
	
  def update(self, eye, target):
      self.position = eye + target.normalised * 5
