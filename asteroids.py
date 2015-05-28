from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy as np
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4
from buffers import initializeVAO
from gameobject import GameObject
from objloader import loadObj
from pyrr import euler as euler
from random import random
from math import sin, cos


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
        self._createAsteroids()
        self._initModel()

  def _initModel(self):

      self.vao = glGenVertexArrays(1)
      glUseProgram(self.program.pointer)
      glBindVertexArray(self.vao)

      posVBO = vbo.VBO(np.array(self.vertices, dtype='f'))
      posVBO.bind()
      glEnableVertexAttribArray(0)
      glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
  
      normalVBO = vbo.VBO(np.array(self.normals, dtype='f'))
      normalVBO.bind()
      glEnableVertexAttribArray(1)
      glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
  
      texVBO = vbo.VBO(np.array(self.texCoords, dtype='f'))
      texVBO.bind()
      glEnableVertexAttribArray(2)
      glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None)


      #matVBO = glGenBuffers(1)
      #glBindBuffer(GL_ARRAY_BUFFER, matVBO)
      #glBufferData(GL_ARRAY_BUFFER, self.amount * 16*4,
              #np.array(self.getModelMatrices(), dtype='f'), GL_STATIC_DRAW)
      matVBO = vbo.VBO(np.array(self.getModelMatrices(), dtype='f'))
      matVBO.bind()
      glEnableVertexAttribArray(3)
      glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, 16*4, matVBO)
      
      glEnableVertexAttribArray(4)
      glVertexAttribPointer(4, 4, GL_FLOAT, GL_FALSE, 16*4, matVBO + 4*4)
      
      glEnableVertexAttribArray(5)
      glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, 16*4, matVBO + 8*4)
      
      glEnableVertexAttribArray(6)
      glVertexAttribPointer(6, 4, GL_FLOAT, GL_FALSE, 16*4, matVBO + 12*4)
      
      glVertexAttribDivisor(3,1)
      glVertexAttribDivisor(4,1)
      glVertexAttribDivisor(5,1)
      glVertexAttribDivisor(6,1)
      glBindVertexArray(0)
      glUseProgram(0)
      self.count = len(self.vertices) / 3
      
  def drawCall(self):
      glDrawArraysInstanced(GL_TRIANGLES, 0, self.count, self.amount)
      
  def getModelMatrices(self):
      return self.modelMatrices
    
  def draw(self, eye, viewMatrix, projMatrix):
      glUseProgram(self.program.pointer)
      glBindVertexArray(self.vao)

      eyePos = self.program.glUniforms["eye"]
      glUniform3fv(eyePos, 1, GL_FALSE, eye)

      vpMatrix = viewMatrix * projMatrix
      glUniformMatrix4fv(self.program.glUniforms["vpMatrix"], 1,
                         GL_FALSE, vpMatrix)

      self._bindTextures()
      self._sendLightningParameters()

      self.drawCall()

      glBindVertexArray(0)
      glUseProgram(0)
          
  def update(self, dt):
      self.rot += dt

  def _createAsteroids(self):
      self.modelMatrices = [0 for k in range(self.amount)]

      for i in range(self.amount):
	#translation displace along circle 
	angle = (i/float(self.amount))*360
	displacement = (random() * (2 * self.offset)) - self.offset
	x = sin(angle) * self.radius + displacement
        rx = mat4.from_x_rotation(displacement, dtype='f')
	displacement = (random() * (2 * self.offset)) - self.offset
	y = displacement * 0.2
        ry = mat4.from_y_rotation(displacement, dtype='f')
	displacement = (random() * (2 * self.offset)) - self.offset
	z = cos(angle) * self.radius + displacement
        rz = mat4.from_z_rotation(displacement, dtype='f')
	translation = mat4.from_translation(vec3([x,y,z]), dtype='f')
	#scale between 0.05 and 0.25
        scaleFactor = random() * 2000 / 100.0 + 0.05
        scale = mat4.from_scale(vec3([scaleFactor, scaleFactor, scaleFactor]), dtype='f')
	#add random rotation around x
        rotation = rx * ry * rz
	#add to list of matrices
        self.modelMatrices[i] = scale * rotation * translation
