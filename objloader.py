#Loading OBJ files 
#Based on Jon implementation http://www.nandnor.net/?p=86 

def loadObj(filename):
    """Loads a Wavefront OBJ file. """
    vertices = []
    normals = []
    texCoords = []

    verticesOut = []
    normalsOut = []
    texCoordsOut = []

    for line in open(filename,"r"):
        if line.startswith('#'): 
            continue #for comments
        values = line.split()
        if not values: 
            continue
        if values[0] == "v":			#Vertices
            v = map(float, values[1:4])
            vertices.append(v)
        elif values[0] == "vn":		#Normals
            n = map(float, values[1:4])
            normals.append(n)
        elif values[0] == "vt":		#Textures
            t = map(float, values[1:4])
            texCoords.append(t)
        elif values[0] == "f":		#Faces

            for face in values[1:]:
              w = face.split('/')
              #OBJ Files are 1-indexed so we must substract 1 
              for vertex in vertices[int(w[0])-1]:
                  verticesOut.append(vertex)
              for texCoord in texCoords[int(w[1])-1]:
                  texCoordsOut.append(texCoord)
              for normal in normals[int(w[2])-1]:
                  normalsOut.append(normal)

    return verticesOut, normalsOut, texCoordsOut
