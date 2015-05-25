#Loading OBJ files 
#Based on Jon implementation http://www.nandnor.net/?p=86 
from OpenGL.GL import *
import numpy as np
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4
from buffers import initializeVAO
from geometry import createSphereCoords
from gameobject import GameObject
import random
import math

class OBJ:
  def __init__(self, filename,  program=None, shininess=None, ka=None, kd=None, ks=None):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.indexData = []
        self.verticesOut = []
	self.texcoordsOut = []
	self.normalsOut = []
	self.shininess = shininess
        self.ka = ka
        self.kd = kd
        self.ks = ks
	self.position = vec3([-30,0,0])
        self.program = program
        
        for line in open(filename,"r"):
	    if line.startswith('#'): 
                continue #for comments
            values = line.split()
            if not values: 
                continue
            if values[0] == "v":			#Vertices
                v = map(float, values[1:4])
	        self.vertices.append(v)
	    elif values[0] == "vn":		#Normals
	        n = map(float, values[1:4])
	        self.normals.append(n)
	    elif values[0] == "vt":		#Textures
	        t = map(float, values[1:4])
	        self.texcoords.append(t)
	    elif values[0] == "f":		#Faces

                for face in values[1:]:
                  w = face.split('/')
                  #OBJ Files are 1-indexed so we must substract 1 
                  for vertex in self.vertices[int(w[0])-1]:
                      self.verticesOut.append(vertex)
                  #self.verticesOut.append(vertices[int(w[0])-1])
                  for vertex in self.texcoords[int(w[1])-1]:
                      self.texcoordsOut.append(vertex)
                  #self.texcoordsOut.append(self.texcoords[int(w[1])-1])
                  for vertex in self.normals[int(w[2])-1]:
                      self.normalsOut.append(vertex)
                  #self.normalsOut.append(self.normals[int(w[2])-1])

                  self.indexData.append((self.verticesOut,self.texcoordsOut,self.normalsOut))  
                
        self._initModel()
	    #print(self.indexData)
  def _initModel(self):
      self.vao = initializeVAO(self.program, self.verticesOut,
              self.texcoordsOut, self.normalsOut)
      self.indexLen = len(self.indexData) #self.indexData
      print self.verticesOut
      print self.indexLen
      
  def _sendLightningParameters(self):
      names = ["ka", "kd", "ks", "shininess"]
      kaLoc, kdLoc, ksLoc, shininessLoc = [glGetUniformLocation(self.program, name) for name in names]
      glUniform1f(kaLoc, self.ka)
      glUniform1f(kdLoc, self.kd)
      glUniform1f(ksLoc, self.ks)
      glUniform1f(shininessLoc, self.shininess)
        
  def draw(self, viewMatrix, projMatrix):
      glBindVertexArray(self.vao)
      glUseProgram(self.program)
      modelMatrix = self.getModelMatrix()
      mvpMatrix = modelMatrix * viewMatrix * projMatrix
      glUniformMatrix4fv(glGetUniformLocation(self.program, "mMatrix"), 1,
              GL_FALSE, modelMatrix)
      glUniformMatrix4fv(glGetUniformLocation(self.program, "mvpMatrix"), 1, GL_FALSE, mvpMatrix)
      self._sendLightningParameters()
      
      glDrawArrays(GL_TRIANGLES, 0, self.indexLen)
      glUseProgram(0)
      glBindVertexArray(0)
			       
  def getModelMatrix(self):
      scale = mat4.from_scale([0.3, 0.3, 0.3])
      trans = mat4.from_translation(self.position, dtype='f')
      return scale * trans
	
  def update(self, eye, target):
      self.position = eye + (target - eye).normalised * vec3([0, -1, 5])
      
	    

