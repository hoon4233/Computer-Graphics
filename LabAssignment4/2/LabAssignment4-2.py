import glfw
from OpenGL.GL import *
import numpy as np



def render(M):
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
    glColor3ub(255, 255, 255)
# draw point p
    glBegin(GL_POINTS)
    glVertex2fv(np.array(M@[0.5,0.,1.])[:-1])
# your implementation
    glEnd()
# draw vector v
    glBegin(GL_LINES)
    glVertex2fv(np.array(M@[0.0,0.,0.])[:-1])
    glVertex2fv(np.array(M@[0.5,0.,0.])[:-1])
# your implementation
    glEnd()
            
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016025105", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)


    while not glfw.window_should_close(window):
        glfw.poll_events()

        t = glfw.get_time()
        s = np.sin(t)
        c = np.cos(t)

        M =np.array([[c,-s,0.],
                    [s,c,0.],
                    [0.,0.,1.]])
        S = np.array([[1.,0.,0.5],
                    [0.,1.,0.],
                    [0.,0.,1.]])
        
        render(M@S)

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()