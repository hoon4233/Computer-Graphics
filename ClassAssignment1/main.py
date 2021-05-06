import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

gCamAng = 0.
gCamHeight = 1.

Orbit = False
Panning = False
Zooming = 0.

gAzimuth = 0.
gElevation = 0.

gPanning_x = 0.
gPanning_y = 0.

mouse_x = 0.
mouse_y = 0.


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-15.,0.,0.]))
    glVertex3fv(np.array([15.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,15.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,-15.]))
    glVertex3fv(np.array([0.,0.,15.]))
    glEnd()

def drawGrid():
    # Gray Color
    glColor3ub(255, 255, 255)
    glBegin(GL_QUADS)
    glVertex3f(10., 0., 10.)
    glVertex3f(-10., 0., 10.)
    glVertex3f(-10., 0., -10.)
    glVertex3f(10., 0., -10.)
    glEnd()

    glBegin(GL_LINES)
    for i in range(-10, 10):
        if i == 0:
            continue
        glVertex3f(i, 0., -10.)
        glVertex3f(i, 0., 10.)
        glVertex3f(-10., 0., i)
        glVertex3f(10., 0., i)
    glEnd()

def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0) 
                             
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0) 
                             
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
                             
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
 
    glVertex3f(-1.0, 1.0, 1.0) 
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0) 
    glVertex3f(-1.0,-1.0, 1.0) 
                             
    glVertex3f( 1.0, 1.0,-1.0) 
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

def drawSphere(numLats = 12, numLongs = 12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)

        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def render():
    global gCamAng, gCamHeight, Panning, Zooming, gAzimuth, gElevation, gPanning_x, gPanning_y, mouse_x, mouse_y

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glLoadIdentity()

    gluPerspective(50, 1, 1, 40)
    gluLookAt(10*np.sin(gCamAng),gCamHeight,10*np.cos(gCamAng), 0,0,0, 0,1,0)
    glTranslatef(gPanning_x, -gPanning_y, Zooming)
    glRotatef(gAzimuth, 1, 0, 0)
    glRotatef(gElevation, 0, 1, 0)

    drawFrame()
    glColor3ub(255, 255, 255)
    drawGrid()

    #draw start
    t = glfw.get_time()
    glPushMatrix()
    glColor3ub(255, 192, 203)
    glTranslatef(0., 0., 0.1 * np.sin(t * 5))

    #body
    glPushMatrix()
    glScalef(0.7, 1.5, 0.7)
    drawSphere()
    glPopMatrix()
    

    #head
    glPushMatrix()
    glTranslatef(0., 2.3, 0.)

    glPushMatrix()
    glScalef(0.8, 0.8, 0.8)
    drawSphere()
    glPopMatrix()
    
    #right ear
    glPushMatrix()
    glTranslatef(0., 0., 0.2 * np.sin(t * 5))
    glTranslatef(-0.8, 0.8, .0)

    glPushMatrix()
    glScalef(0.3, 0.8, 0.3)
    drawSphere()
    glPopMatrix()

    glPopMatrix()


    #left ear
    glPushMatrix()
    glTranslatef(0., 0., -0.2 * np.sin(t * 5))
    glTranslatef(0.8, 0.8, .0)

    glPushMatrix()
    glScalef(0.3, 0.8, 0.3)
    drawSphere()
    glPopMatrix()

    glPopMatrix()

    glPopMatrix() #end head

    #right leg
    glPushMatrix()
    glRotatef(5. * np.cos(t * 5), 1., 0, 0)
    glTranslatef(-0.4, -2., 0.)

    glPushMatrix()
    glScalef(0.2, 1., 0.2)
    drawSphere()
    glPopMatrix()

    #right foot
    glPushMatrix()
    glTranslatef(0., -1., 0.5)
    glRotatef(-5. * np.cos(t), 1., 0, 0)

    glPushMatrix()
    glScalef(0.2, 0.1, 0.5)
    drawSphere()
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()  #end right leg

    #left leg
    glPushMatrix()
    glRotatef(-5. * np.cos(t * 5), 1., 0., 0.)
    glTranslatef(0.4, -2., 0.0)

    glPushMatrix()
    glScalef(0.2, 1., 0.2)
    drawSphere()
    glPopMatrix()

    #left foot
    glPushMatrix()
    glTranslatef(0.0, -1., 0.5)
    glRotatef(-5 * np.cos(t), 1., 0, 0)

    glPushMatrix()
    glScalef(0.2, 0.1, 0.5)
    drawSphere()
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()  #end left leg

    #right arm 
    glPushMatrix()
    glRotatef(5. * np.cos(t * 5), 0, 1., 0)
    glRotatef(30., 0, 0, 1.)
    glTranslatef(-0.8, 1.2, 0.)

    glPushMatrix()
    glScalef(1., 0.2, 0.2)
    drawSphere()
    glPopMatrix()

    #right hand
    glPushMatrix()
    glTranslatef(-1.15, -0.04, .0)

    glPushMatrix()
    glScalef(0.18, 0.18, 0.18)
    drawSphere()
    glPopMatrix()

    glPopMatrix()

    glPopMatrix() #end right arm


    #left arm 
    glPushMatrix()
    glRotatef(5. * np.cos(t * 5), 0, 1., 0)
    glRotatef(-30., 0, 0, 1.)
    glTranslatef(0.8, 1.2, 0.)

    glPushMatrix()
    glScalef(1., 0.2, 0.2)
    drawSphere()
    glPopMatrix()

    #left hand
    glPushMatrix()
    glTranslatef(1.15, 0.04, .0)

    glPushMatrix()
    glScalef(0.18, 0.18, 0.18)
    drawSphere()
    glPopMatrix()

    glPopMatrix()

    glPopMatrix() #end left arm

    glPopMatrix()  #end body



def cursor_callback(window, xpos, ypos):
    global Orbit, Panning, gAzimuth, gElevation, gPanning_x, gPanning_y, mouse_x, mouse_y

    x, y = glfw.get_cursor_pos(window)
    dx, dy = x - mouse_x, y - mouse_y


    if Orbit == True:
        gElevation = gElevation + (dx * (0.2))
        gAzimuth = gAzimuth + (dy * (0.2))
        
        mouse_x = x
        mouse_y = y

    elif Panning == True:
        gPanning_x = gPanning_x + (dx * (0.02))
        gPanning_y = gPanning_y + (dy * (0.02))
    
        mouse_x = x
        mouse_y = y

def button_callback(window, button, action, mod):
    global gCamAng, gCamHeight, Orbit, Panning, mouse_x, mouse_y
    
    mouse_x, mouse_y = glfw.get_cursor_pos(window)

    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_LEFT:
            Orbit = True
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            Panning = True
    elif action == glfw.RELEASE:
        Orbit = False
        Panning = False


def scroll_callback(window, xoffset, yoffset):
    global Zooming
    if yoffset > 0:
        Zooming += 0.5
    if yoffset < 0:
        Zooming -= 0.5


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 800, "2016025105", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render()
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == "__main__":
    main()