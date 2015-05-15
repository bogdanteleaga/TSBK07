from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy as np

def initializeVAO(program, vertexPos, normals, textureCoords, indexData):
    names = ["inPos", "inNormal", "inTex"]
    posLoc, normalLoc, texLoc = [glGetAttribLocation(program, name) for name in names]

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    posVBO = vbo.VBO(np.array(vertexPos, dtype='f'))
    posVBO.bind()
    glEnableVertexAttribArray(posLoc)
    glVertexAttribPointer(posLoc, 3, GL_FLOAT, GL_FALSE, 0, None)

    normalVBO = vbo.VBO(np.array(normals, dtype='f'))
    normalVBO.bind()
    glEnableVertexAttribArray(normalLoc)
    glVertexAttribPointer(normalLoc, 3, GL_FLOAT, GL_FALSE, 0, None)

    texVBO = vbo.VBO(np.array(textureCoords, dtype='f'))
    texVBO.bind()
    glEnableVertexAttribArray(texLoc)
    glVertexAttribPointer(texLoc, 2, GL_FLOAT, GL_FALSE, 0, None)

    indexVBO = vbo.VBO(np.array(indexData, dtype='uint32'), target=GL_ELEMENT_ARRAY_BUFFER)
    indexVBO.bind()

    glBindVertexArray(0)

    return vao
