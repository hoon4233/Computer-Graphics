###################################################
# [Practice] First OpenGL Program
import glfw
from OpenGL.GL import *
import numpy as np


default = 4

types = {
    1: GL_POINTS,
    2: GL_LINES,
    3: GL_LINE_STRIP,
    4: GL_LINE_LOOP,
    5: GL_TRIANGLES,
    6: GL_TRIANGLE_STRIP,
    7: GL_TRIANGLE_FAN,
    8: GL_QUADS,
    9: GL_QUAD_STRIP,
    0: GL_POLYGON
}

def render() :
    global types
    global default
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    rad = np.arange(0,360,30)
    glBegin(types.get(default))

    x =np.cos(np.deg2rad(rad))
    y= np.sin(np.deg2rad(rad))
    for i in range(12):
        glVertex2f(x[i],y[i])

    glEnd()

def key_callback(window, key, scancode, action, mods):
    global default
    if action==glfw.PRESS and key>47 and key<58 : #아스키코드로 들어올테니 일반 숫자로 변환
        default = key-48

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2016025105", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()