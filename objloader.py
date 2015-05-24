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
        self._initModel()
        
        for line in open(filename,"r"):
	  if line.startswith('#'): continue #for comments
          values = line.split()
          if not values: continue
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
	      self.verticesOut.append(list(self.vertices[int(w[0])-1]))
	      self.texcoordsOut.append(list(self.texcoords[int(w[1])-1]))
	      self.normalsOut.append(list(self.normals[int(w[2])-1]))

	    self.indexData.append((self.verticesOut,self.texcoordsOut,self.normalsOut))  
	    
	    #print(self.indexData)
  def _initModel(self):
      self.vao = initializeVAO(self.program, self.vertices, self.texcoords, self.normals, self.verticesOut)
      self.indexLen = len(self.verticesOut) #self.indexData
      
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
      self._sendLightningParameters()
      
      glDrawElements(GL_TRIANGLES, self.indexLen, GL_UNSIGNED_INT, None)
      glBindVertexArray(0)
			       
  def getModelMatrix(self):
      trans = mat4.from_translation(self.position, dtype='f')
      return trans
	
	    
