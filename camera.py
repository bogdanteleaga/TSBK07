from OpenGL.GL import *
from pyrr import Matrix44 as mat4
from pyrr import Vector3 as vec3
import math
import cyglfw3 as glfw

oldx, oldy = 0.0, 0.0
first = True
horizontalAngle = 3.14
verticalAngle = 0.0
speed = 0.166
mouseSpeed = 0.00008

def getNewViewMatrixAndEye(window, animation_speed, dt, position, width=1920.0, height=1080.0):
    """
    Kind of global function. 
    Mainly handles camera which behaves as an FPS camera.
    Additionally it had some input handling added to it(see animation_speed).
    """
    global horizontalAngle, verticalAngle
    global oldx, oldy, first

    if first:
        oldx, oldy = glfw.GetCursorPos(window)
        first = False

    dt = dt * 1000

    # Get mouse position
    x, y = glfw.GetCursorPos(window)

    # Reset mouse position for next frame
    #glfw.SetCursorPos(window, width/2.0, height/2.0);

    # Compute new orientation
    horizontalAngle += mouseSpeed * dt * float(oldx - x);
    verticalAngle   += mouseSpeed * dt * float(oldy - y);

    oldx = x
    oldy = y

    # Direction : Spherical coordinates to Cartesian coordinates conversion
    direction = vec3([
        math.cos(verticalAngle) * math.sin(horizontalAngle), 
        math.sin(verticalAngle),
        math.cos(verticalAngle) * math.cos(horizontalAngle)
    ], dtype='f')

    # Right vector
    right = vec3([
        math.sin(horizontalAngle - math.pi/2.0),
        0.0,
        math.cos(horizontalAngle - math.pi/2.0)
    ], dtype='f')

    # Up vector
    up = right ^ direction

    # Move forward
    if glfw.GetKey(window, glfw.KEY_UP) == glfw.PRESS or glfw.GetKey(window, glfw.KEY_W) == glfw.PRESS:
        position += direction * dt * speed

    # Move backward
    if glfw.GetKey(window, glfw.KEY_DOWN) == glfw.PRESS or glfw.GetKey(window, glfw.KEY_S) == glfw.PRESS:
        position -= direction * dt * speed

    # Strafe right
    if glfw.GetKey(window, glfw.KEY_RIGHT) == glfw.PRESS or glfw.GetKey(window, glfw.KEY_D) == glfw.PRESS:
        position += right * dt * speed

    # Strafe left
    if glfw.GetKey(window, glfw.KEY_LEFT) == glfw.PRESS or glfw.GetKey(window, glfw.KEY_A) == glfw.PRESS:
        position -= right * dt * speed
    if glfw.GetKey(window, glfw.KEY_Q) == glfw.PRESS or glfw.GetKey(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        exit()
    if glfw.GetKey(window, glfw.KEY_J) == glfw.PRESS:
        animation_speed += 100
    if glfw.GetKey(window, glfw.KEY_K) == glfw.PRESS:
        animation_speed -= 100


    # Camera matrix
    viewMatrix = lookAt(position, position + direction, up)

    return horizontalAngle, verticalAngle, position, direction, right, up, viewMatrix, animation_speed


def lookAt(eye, target, up):
    """
    Custom lookAt matrix implementation.
    Will be contributed back to pyrr and should be removed from here.
    """
    forward = (target - eye).normalised
    side = (forward ^ up).normalised
    up = (side ^ forward).normalised

    mat = mat4(dtype='f')
    mat[0][0] = side[0]
    mat[1][0] = side[1]
    mat[2][0] = side[2]

    mat[0][1] = up[0]
    mat[1][1] = up[1]
    mat[2][1] = up[2]

    mat[0][2] = -forward[0]
    mat[1][2] = -forward[1]
    mat[2][2] = -forward[2]

    mat[3][0] = - (side | eye)
    mat[3][1] = - (up | eye)
    mat[3][2] = forward | eye
    mat[3][3] = 1.0

    return mat
