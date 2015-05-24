from OpenGL.GL import *
import numpy as np
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4
from buffers import initializeVAO
from gameobject import GameObject
from objloader import loadObj
from pyrr import euler as euler
import random
import math


class Asteroids(GameObject):

  def __init__(self, filename=None,  program=None, texImg=None, specTexImg=None,
               normalMap=None, shininess=None, ka=None, kd=None, ks=None, amount=None, radius=None, offset=None):
        GameObject.__init__(self, name=None, position=None, texImg=texImg,
                            specTexImg=specTexImg, normalMap=normalMap,
                            shininess=shininess, ka=ka, kd=kd, ks=ks, 
                            program=program)
	self.rot = 0
	self.amount = amount
	self.radius = radius
	self.offset = offset
        self.vertices, self.normals, self.texCoords = loadObj(filename)
        self._initModel()
        self._createAsteroids()

  def _initModel(self):

      self.vao = initializeVAO(self.program, self.vertices,
                               self.normals, self.texCoords)
      glBindVertexArray(self.vao)
      matVBO = vbo.VBO(np.array(self.getModelMatrices(), dtype='f'))
      matVBO.bind()
      
      glEnableVertexAttribArray(3)
      glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, 16*4, None)
      
      glEnableVertexAttribArray(4)
      glVertexAttribPointer(4, 4, GL_FLOAT, GL_FALSE, 16*4, 4)
      
      glEnableVertexAttribArray(5)
      glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, 16*4, 2*4)
      
      glEnableVertexAttribArray(6)
      glVertexAttribPointer(6, 4, GL_FLOAT, GL_FALSE, 16*4, 3*4)
      
      glVertexAttribDivisor(3,1)
      glVertexAttribDivisor(4,1)
      glVertexAttribDivisor(5,1)
      glVertexAttribDivisor(6,1)
      glBindVertexArray(0)
      self.count = len(self.vertices) / 3
      
  def drawCall(self):
      glDrawElementsInstanced(GL_TRIANGLES, self.count, GL_UNSIGNED_INT, 0 , amount)
      
  def getModelMatrices(self):
      return self.modelMatrices
    
  def draw(self, eye, viewMatrix, projMatrix):
      glUseProgram(self.program)
      glBindVertexArray(self.vao)

      eyePos = glGetAttribLocation(self.program, "eye")
      glUniform3fv(eyePos, 1, GL_FALSE, eye)

      vpMatrix = viewMatrix * projMatrix
      glUniformMatrix4fv(glGetUniformLocation(self.program, "vpMatrix"), 1,
                         GL_FALSE, vpMatrix)

      self._bindTextures()
      self._sendLightningParameters()

      self.drawCall()

      glBindVertexArray(0)
      glUseProgram(0)
          
  def update(self, dt):
      self.rot += dt

  def _createAsteroids(self):
      self.modelMatrices = [0 for k in range(amount)]

      for i in range(self.amount):
	#translation displace along circle 
	angle = 1%(i*1.0/self.amount)*360
	displacement = (random()%(1*self.offset*100))/100.0 - self.offset
	x = sin(angle) * self.radius + displacement
	displacement = (random()%(1*self.offset*100))/100.0 - self.offset
	y = displacement * 0.4
	displacement = (random()%(1*self.offset*100))/100.0 - self.offset
	z = cos(angle) * self.radius + displacement
	translation = mat4.from_translation(vec3([x,y,z])))
	#scale between 0.05 and 0.25
	scale = (random()%20)/100.0 + 0.05
	#add random rotation around x
	rotation = mat4.from_x_rotation(self.rot)
	#add to list of matrices
	self.modelMatrices[i] = scale * rotation * translation
	