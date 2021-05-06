import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = 0.
gCamHeight = 1.


Orbit = False
Panning = False
Zooming = 0.
Toggle = 1
Smoothing = 1

gElevation = 0.
gAzimuth = 0.
gPanning_x = 0.
gPanning_y = 0.


mouse_x = 0.
mouse_y = 0.


gVertexArrayIndexed_main = np.array([])
gVertexArraySeperate_main = np.array([])
gNormalArray = np.array([])

gVertexArrayIndexed = np.array([])
gVertexArraySeperate = np.array([])
gNormalArray = np.array([])

gVertexArrayIndexed = np.array([])
gVertexArraySeperate = np.array([])
gNormalArray = np.array([])


def drawElement(Smoothing) :
    global gVertexArraySeperate, gNormalArray, gVertexArrayIndexed
    if Smoothing:
        varr = gVertexArraySeperate
        vnarr = gNormalArray
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 0, vnarr)
        glVertexPointer(3, GL_FLOAT, 0, varr)
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))
    else:
        varr = gVertexArrayIndexed
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
        glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
        glDrawArrays(GL_TRIANGLES,0,int(varr.size/6))

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

def toggleZ(Toggle) :
    if Toggle:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )


def render():
    global gCamAng, gCamHeight, Orbit, Panning, Toggle, Smoothing, gElevation, gAzimuth, gPanning_x, gPanning_y
    global mouse_x, mouse_y

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 1, 45)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10*np.sin(gCamAng), gCamHeight,10*np.cos(gCamAng), 0,0,0, 0,1,0)
    glTranslatef(gPanning_x, -gPanning_y, Zooming)
    glRotatef(gAzimuth, 1, 0, 0)
    glRotatef(gElevation, 0, 1, 0)
    
    drawFrame()
    glColor3ub(255, 255, 255)
    drawGrid()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_RESCALE_NORMAL)


    glPushMatrix()

    lightPos0 = (3., 0., 0., 0.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    lightPos1 = (0., 3., 0., 0.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    lightPos2 = (0., 0., 3., 0.)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos2)

    glPopMatrix()


    lightColor0 = (1., 0., 0., 1.)
    ambientLightColor0 = (.1, .0, .0, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)

    lightColor1 = (0., 1., 0., 1.)
    ambientLightColor1 = (.0, .1, .0, 1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)

    lightColor2 = (0., 0., 1., 1.)
    ambientLightColor2 = (.0, .0, .1, 1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor2)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor2)


    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 0., 0., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)


    toggleZ(Toggle)


    glPushMatrix()
    drawElement(Smoothing)
    glPopMatrix()

    glDisable(GL_LIGHTING)

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, Toggle, Smoothing
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_Z:
            if Toggle:
                Toggle = 0
            else:
                Toggle = 1
        elif key==glfw.KEY_S:
            if Smoothing:
                Smoothing = 0
            else:
                Smoothing = 1

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

def normalized(v):
    l = np.sqrt(np.dot(v,v))
    return 1/l *np.array(v)

def printInfo(paths,tri,quad,over):
    if "/" in paths[0]:
        name = paths[0].split("/")
    elif "\\" in paths[0]:
        name = paths[0].split("\\")

    print("File name: " + name[len(name) - 1])
    print("Total number of faces: " + str(tri+quad+over))
    print("Number of faces with 3 vertices: " + str(tri))
    print("Number of faces with 4 vertices: " + str(quad))
    print("Number of faces with more than 4 vertices: " + str(over))


def load_file(paths):
    global gVertexArrayIndexed, gVertexArraySeperate, gNormalArray

    obj_file = open(paths[0], 'r')
    lines = obj_file.readlines()

    vertex = []
    vnormal = []

    tri = 0
    quad = 0
    over = 0

    varr = []
    vnarr = []


    for line in lines:
        line = line.split()
        if not len(line):
            continue
    
        elif line[0] == "v":
            vertex.append(list(map(float, line[1:])))
    
        elif line[0] == "vn":
            vnormal.append(list(map(float, line[1:])))
    
        elif line[0] == "f":

            if len(line) == 4:
                tri += 1
                for v in line[1:]:
                    tmp = v.split('/')
                    if int(tmp[0]) < 0:
                        varr.append(vertex[int(tmp[0])])
                    else:
                        varr.append(vertex[int(tmp[0]) - 1])
                    if len(tmp) > 2:
                        if int(tmp[2]) < 0:
                            vnarr.append(vnormal[int(tmp[2])])
                        else:
                            vnarr.append(vnormal[int(tmp[2]) - 1])
            elif len(line) > 4:
                if len(line) == 5:
                    quad += 1
                elif len(line) > 5:
                    over += 1

                for i in range(2, len(line) - 1, 1):
                    for j in [0, i - 1, i]:
                        tmp = line[1:][j].split('/')
                        if int(tmp[0]) < 0 :
                            varr.append(vertex[int(tmp[0])])
                        else:
                            varr.append(vertex[int(tmp[0]) - 1])
                        if len(tmp) > 2:
                            if int(tmp[2]) < 0:
                                vnarr.append(vnormal[int(tmp[2])])
                            else:
                                vnarr.append(vnormal[int(tmp[2]) - 1])
    

    gVertexArraySeperate = np.array(varr,'float32')
    gNormalArray = np.array(vnarr)

    lst = []
    for i in varr :
        lst.append(normalized(i))
        lst.append(i)
    gVertexArrayIndexed = np.array(lst,'float32')


    printInfo(paths,tri,quad,over)

    obj_file.close()


def main():
    global gVertexArraySeperate, gNormalArray, gVertexArrayIndexed
    if not glfw.init():
        return
    window = glfw.create_window(800,800,'2016025105', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()