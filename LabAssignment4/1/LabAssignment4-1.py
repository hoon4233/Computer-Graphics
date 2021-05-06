import glfw
from OpenGL.GL import *
import numpy as np

keys = list()

def render():
    global keys
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
 ###########################
 # implement here
    for i in range(len(keys)-1,-1,-1):
        if keys[i] == 81:
            glTranslatef(-0.1,0.,0.)
        elif keys[i] == 69:
            glTranslatef(0.1,0.,0.)
        elif keys[i] == 65:
            glRotatef(10.,0.,0.,1.)
        elif keys[i] == 68:
            glRotatef(-10.,0.,0.,1.)
        elif keys[i] ==49:
            keys.clear()
            break
    # if keys : glloadidentity()실험하려고, 이놈은 매 render마다 current m을 identity로 만들어준다
    #     if keys[0] == 81:
    #         glTranslatef(-0.1,0.,0.)
    #     elif keys[0] == 69:
    #         glTranslatef(0.1,0.,0.)
    #     elif keys[0] == 65:
    #         glRotatef(10.,0.,0.,1.)
    #     elif keys[0] == 68:
    #         glRotatef(-10.,0.,0.,1.)
    #     elif keys[0] ==49:
    #         keys.clear()
        
 ###########################
    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global keys
    if action==glfw.PRESS and (key==glfw.KEY_Q or key==glfw.KEY_E or key==glfw.KEY_A or key==glfw.KEY_D or key==glfw.KEY_1 ) : 
        keys.append(key)
        # keys.insert(0,key) glloadidentity()실험하려고, 이놈은 매 render마다 current m을 identity로 만들어준다
        
        
    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016025105", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()