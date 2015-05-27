from OpenGL.GL import glGetAttribLocation, glEnableVertexAttribArray,\
    glVertexAttribPointer, glBindVertexArray, glGenVertexArrays,\
    glUseProgram, GL_FLOAT, GL_FALSE, GL_ELEMENT_ARRAY_BUFFER
from OpenGL.arrays import vbo
import numpy as np


def initializeVAO(program, vertexPos, normals, textureCoords, indexData=None,
                  tangents=None):
    glUseProgram(program.pointer)
    names = ["inPos", "inNormal", "inTex"]
    posLoc, normalLoc, texLoc = [program.glAttribs[name]
                                 for name in names]
    print program
    print posLoc, normalLoc, texLoc

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

    if tangents:
        tanVBO = vbo.VBO(np.array(tangents, dtype='f'))
        tanVBO.bind()
        tanLoc = program.glAttribs["inTan"]
        glEnableVertexAttribArray(tanLoc)
        glVertexAttribPointer(tanLoc, 3, GL_FLOAT, GL_FALSE, 0, None)

    if indexData:
        indexVBO = vbo.VBO(np.array(indexData, dtype='uint32'),
                           target=GL_ELEMENT_ARRAY_BUFFER)
        indexVBO.bind()

    glBindVertexArray(0)
    glUseProgram(0)

    return vao
