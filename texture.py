"""
This has been split from another file
Author: Mahesh Venkitachalam
Some OpenGL utilities.
"""

import OpenGL
from OpenGL.GL import *

import math
import numpy as np

from PIL import Image

def loadTexture(filename, program):
    """load OpenGL 2D texture from given image file"""
    img = Image.open(filename) 
    imgData = np.array(list(img.getdata()), np.int8)
    texture = glGenTextures(1)

    glUseProgram(program.pointer)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 
                 0, GL_RGB, GL_UNSIGNED_BYTE, imgData)

    glUseProgram(0)
    return texture

def activateTexture(texture, index, program, name, nr, texType=GL_TEXTURE_2D):
    texLoc = program.glUniforms[name]
    glUniform1i(texLoc, nr)
    glActiveTexture(index)
    glBindTexture(texType, texture)

def loadCubeMap(program, filenames):
    texture = glGenTextures(1)

    glUseProgram(program.pointer)
    glBindTexture(GL_TEXTURE_CUBE_MAP, texture)
    print filenames
    for i, filename in enumerate(filenames):
        print filename
        img = Image.open(filename)
        imgData = np.array(list(img.getdata()), np.int8)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB,
                     img.size[0], img.size[1], 0, GL_RGB, 
                     GL_UNSIGNED_BYTE, imgData)

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glUseProgram(0)
    return texture
 
