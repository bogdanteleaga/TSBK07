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
	self.variables = dict([(x,True)for x in ["hAngle", "vAngle", "right"]])
	self.oldhAngle = 0
	self.oldvAngle = 0
	self.zRotAngle = 0
	self.xRotAngle = 0
        self.vertices, self.normals, self.texCoords = loadObj(filename)

        self._initModel()

  def _initModel(self):
      self.vao = initializeVAO(self.program, self.vertices,
                               self.normals, self.texCoords)
      self.count = len(self.vertices) / 3
      
  def drawCall(self):
      glDrawArrays(GL_TRIANGLES, 0, self.count)
			   
  def getzRot(self, diff):
      if diff > 0:
        self.zRotAngle -= 0.05
        if self.zRotAngle <= -1:
	  self.zRotAngle = -1
      if diff < 0:
	self.zRotAngle += 0.05
	if self.zRotAngle >= 1:
	  self.zRotAngle = 1
      if diff == 0:
	if self.zRotAngle > 0.1:
	  self.zRotAngle -= 0.09
	elif self.zRotAngle < -0.1:
	  self.zRotAngle += 0.09
	else:
	  self.zRotAngle = 0
      return self.zRotAngle
    
  def getxRot(self, diff):
      if diff > 0:
        self.xRotAngle -= 0.05
        if self.xRotAngle <= -1:
	  self.xRotAngle = -1
      if diff < 0:
	self.xRotAngle += 0.05
        if self.xRotAngle >= 1:
	  self.xRotAngle = 1
      if diff == 0:
	if self.xRotAngle > 0.1:
	  self.xRotAngle -= 0.09
	elif self.xRotAngle < -0.1:
	  self.xRotAngle += 0.09
	else:
	  self.xRotAngle = 0
      return -self.xRotAngle + self.vAngle
    
  def getModelMatrix(self):
      scale = mat4.from_scale([0.2, 0.2, 0.2])
      
      roty = mat4.from_y_rotation(-self.hAngle)

      vdiff = self.vAngle - self.oldvAngle
      rotx = mat4.from_x_rotation(self.getxRot(vdiff))
      
      zdiff = self.hAngle - self.oldhAngle
      rotz = mat4.from_z_rotation(-self.getzRot(zdiff))

      trans = mat4.from_translation(self.position, dtype='f')
      self.oldhAngle = self.hAngle
      self.oldvAngle = self.vAngle
      
      return scale * rotz * rotx * roty * trans
    
  def update(self, eye, direction, right, up, hAngle, vAngle):
      self.vAngle = vAngle
      self.hAngle = hAngle
      self.position = eye + direction.normalised * 7 + up.normalised * -2
      
  
