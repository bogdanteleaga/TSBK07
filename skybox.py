from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy as np
from pyrr import Vector3 as vec3
from pyrr import Matrix44 as mat4
from buffers import initializeVAO
from gameobject import GameObject
from objloader import loadObj
from pyrr import euler as euler
from texture import loadCubeMap, activateTexture
import random
import math


class Skybox():

    def __init__(self, filenames=None, program=None):
        self.program = program
        self._initModel()
        self.initTextures(filenames)

    def initTextures(self, filenames):
        self.texture = loadCubeMap(self.program, filenames)

    def _initModel(self):
        skyboxVertices = [
            -1.0,  1.0, -1.0,
            -1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
             1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
      
            -1.0, -1.0,  1.0,
            -1.0, -1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,
            -1.0, -1.0,  1.0,
      
             1.0, -1.0, -1.0,
             1.0, -1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0, -1.0,
             1.0, -1.0, -1.0,
       
            -1.0, -1.0,  1.0,
            -1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0, -1.0,  1.0,
            -1.0, -1.0,  1.0,
      
            -1.0,  1.0, -1.0,
             1.0,  1.0, -1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            -1.0,  1.0, -1.0,
      
            -1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
             1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
             1.0, -1.0,  1.0
        ]
        
        self.vao = glGenVertexArrays(1)
        glUseProgram(self.program.pointer)
        glBindVertexArray(self.vao)

        posVBO = vbo.VBO(np.array(skyboxVertices, dtype='f'))
        posVBO.bind()
        glEnableVertexAttribArray(self.program.glAttribs['inPos'])
        glVertexAttribPointer(self.program.glAttribs['inPos'], 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindVertexArray(0)
        glUseProgram(0)

        self.count = len(skyboxVertices) / 3
        
    def drawCall(self):
        glDrawArrays(GL_TRIANGLES, 0, self.count)
                             
    def draw(self, viewMatrix, projMatrix):
        glUseProgram(self.program.pointer)
        glBindVertexArray(self.vao)
        glDepthFunc(GL_LEQUAL)
  
        glUniformMatrix4fv(self.program.glUniforms["vMatrix"], 1,
                           GL_FALSE, viewMatrix)
        glUniformMatrix4fv(self.program.glUniforms["pMatrix"], 1,
                           GL_FALSE, projMatrix)
  
        activateTexture(self.texture, GL_TEXTURE0, self.program, "tex", 0, texType=GL_TEXTURE_CUBE_MAP)
        self.drawCall()

        glDepthFunc(GL_LESS) # Back to default
  
        glBindVertexArray(0)
