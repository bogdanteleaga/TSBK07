import math

def createSphereCoords(radius):
    latBands = 30
    longBands = 30

    vertexPos = []
    normals = []
    textureCoords = []

    for lat in range(latBands + 1):
        theta = lat * math.pi / latBands
        sinTheta = math.sin(theta)
        cosTheta = math.cos(theta)

        for lon in range(longBands + 1):
            phi = lon * 2 * math.pi / longBands
            sinPhi = math.sin(phi)
            cosPhi = math.cos(phi)

            x = cosPhi * sinTheta
            y = sinPhi * sinTheta
            z = cosTheta

            u = 1 - (lon / longBands)
            v = 1 - (lat / latBands)

            normals.append(x)
            normals.append(y)
            normals.append(z)

            vertexPos.append(x * radius)
            vertexPos.append(y * radius)
            vertexPos.append(z * radius)

            textureCoords.append(u)
            textureCoords.append(v)

    indexData = []
    for lat in range(latBands):
        for lon in range(longBands):
            x = lat * (longBands + 1) + lon
            y = x + longBands + 1

            indexData.append(x)
            indexData.append(y)
            indexData.append(x + 1)

            indexData.append(y)
            indexData.append(y + 1)
            indexData.append(x + 1)
    print indexData

    return vertexPos, normals, textureCoords, indexData

