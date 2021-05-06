import glfw
from OpenGL.GL import *
import numpy as np

gComposedM = np.array([[1.,0.,0.],
                      [0.,1.,0.],
                      [0.,0.,1.]])


def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
 # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if action==glfw.PRESS and key==glfw.KEY_W : 
        gComposedM = np.array([[0.9,0.,0.],
                      [0.,1.,0.],
                      [0.,0.,1.]])@gComposedM
    elif action==glfw.PRESS and key==glfw.KEY_E : 
        gComposedM = np.array([[1.1,0.,0.],
                      [0.,1.,0.],
                      [0.,0.,1.]])@gComposedM
    elif action==glfw.PRESS and key==glfw.KEY_S : 
        t = np.deg2rad(10)
        gComposedM = np.array([[np.cos(t),-np.sin(t),0.],
                      [np.sin(t),np.cos(t),0.],
                      [0.,0.,1.]])@gComposedM
    elif action==glfw.PRESS and key==glfw.KEY_D : 
        t = np.deg2rad(-10) 
        gComposedM = np.array([[np.cos(t),-np.sin(t),0.],
                      [np.sin(t),np.cos(t),0.],
                      [0.,0.,1.]])@gComposedM
    elif action==glfw.PRESS and key==glfw.KEY_X : 
        gComposedM = np.array([[1.,-0.1,0.],
                      [0.,1.,0.],
                      [0.,0.,1.]])@gComposedM
    elif action==glfw.PRESS and key==glfw.KEY_C : 
        gComposedM = np.array([[1.,0.1,0.],
                      [0.,1.,0.],
                      [0.,0.,1.]])@gComposedM
    elif action==glfw.PRESS and key==glfw.KEY_R : 
        gComposedM = np.array([[1.,0.,0.],
                      [0.,-1.,0.],
                      [0.,0.,1.]])@gComposedM
    elif action==glfw.PRESS and key==glfw.KEY_1 : 
        gComposedM = np.array([[1,0.,0.],
                      [0.,1.,0.],
                      [0.,0.,1.]])


def main():
    global gComposedM
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
        
        render(gComposedM)

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()