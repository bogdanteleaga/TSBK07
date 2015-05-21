import math
from pyrr import Vector3 as vec3


def createSphereCoords(radius):
    latBands = 30
    longBands = 30

    vertexPos = []
    normals = []
    textureCoords = []

    for lat in range(0, latBands + 1):
        theta = lat * math.pi / latBands
        sinTheta = math.sin(theta)
        cosTheta = math.cos(theta)

        for lon in range(0, longBands + 1):
            phi = lon * 2 * math.pi / longBands
            sinPhi = math.sin(phi)
            cosPhi = math.cos(phi)

            x = cosPhi * sinTheta
            y = cosTheta
            z = sinPhi * sinTheta

            u = phi / (2 * math.pi)
            v = theta / math.pi

            normals.append(x)
            normals.append(y)
            normals.append(z)

            vx = x * radius
            vy = y * radius
            vz = z * radius
            vertexPos.append(vx)
            vertexPos.append(vy)
            vertexPos.append(vz)

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

    return vertexPos, normals, textureCoords, indexData



def generateTangents(vertexPos, textureCoords, indexData):
    tangents = [0 for i in vertexPos]
    # For each triangle
    for i in range(0, len(indexData), 3):
        v0 = vec3([
            vertexPos[indexData[i] * 3],
            vertexPos[indexData[i] * 3 + 1],
            vertexPos[indexData[i] * 3 + 2]
        ])
        v1 = vec3([
            vertexPos[indexData[i + 1] * 3],
            vertexPos[indexData[i + 1] * 3 + 1],
            vertexPos[indexData[i + 1] * 3 + 2]
        ])
        v2 = vec3([
            vertexPos[indexData[i + 2] * 3],
            vertexPos[indexData[i + 2] * 3 + 1],
            vertexPos[indexData[i + 2] * 3 + 2]
        ])

        edge1 = v1 - v0
        edge2 = v2 - v0

        dU1 = - (textureCoords[indexData[i + 1] * 2] -
                textureCoords[indexData[i] * 2])
        dV1 = - (textureCoords[indexData[i + 1] * 2 + 1] -
                textureCoords[indexData[i] * 2 + 1])

        dU2 = - (textureCoords[indexData[i + 2] * 2] -
                textureCoords[indexData[i] * 2])
        dV2 = - (textureCoords[indexData[i + 2] * 2 + 1] -
                textureCoords[indexData[i] * 2 + 1])

        f = 1.0 / (dU1 * dV2 - dU2 * dV1)

        tangent = f * (dV2 * edge1 - dV1 * edge2)

        tangents[indexData[i] * 3] += tangent[0]
        tangents[indexData[i] * 3 + 1] += tangent[1]
        tangents[indexData[i] * 3 + 2] += tangent[2]

        tangents[indexData[i + 1] * 3] += tangent[0]
        tangents[indexData[i + 1] * 3 + 1] += tangent[1]
        tangents[indexData[i + 1] * 3 + 2] += tangent[2]

        tangents[indexData[i + 2] * 3] += tangent[0]
        tangents[indexData[i + 2] * 3 + 1] += tangent[1]
        tangents[indexData[i + 2] * 3 + 2] += tangent[2]

    outTangents = [0 for i in tangents]
    # Normalize tangents
    for i in range(0, len(tangents), 3):
        x = float(tangents[i])
        y = float(tangents[i + 1])
        z = float(tangents[i + 2])

        if x == y == z == 0:
            outTangents[i] = 0.0
            outTangents[i + 1] = 0.0
            outTangents[i + 2] = 1.0
        else:
            length = math.sqrt(x ** 2 + y ** 2 + z ** 2)
            outTangents[i] = x / length
            outTangents[i + 1] = y / length
            outTangents[i + 2] = z / length

    return outTangents
