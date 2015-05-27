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

def activateTexture(texture, index, program, name, nr):
    texLoc = program.glUniforms[name]
    glUniform1i(texLoc, nr)
    glActiveTexture(index)
    glBindTexture(GL_TEXTURE_2D, texture)
