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

gElevation = 0.
gAzimuth = 0.
gPanning_x = 0.
gPanning_y = 0.


mouse_x = 0.
mouse_y = 0.

Smoothing = 0

gVertexArrayIndexed_main = np.array([])
gVertexArraySeperate_main = np.array([])
gNormalArray_main = np.array([])

gVertexArrayIndexed_sub1 = np.array([])
gVertexArraySeperate_sub1 = np.array([])
gNormalArray_sub1 = np.array([])

gVertexArrayIndexed_sub2 = np.array([])
gVertexArraySeperate_sub2 = np.array([])
gNormalArray_sub2 = np.array([])

gVertexArrayIndexed_hie = np.array([])
gVertexArraySeperate_hie = np.array([])
gNormalArray_hie = np.array([])

gVertexArrayIndexed_hie1 = np.array([])
gVertexArraySeperate_hie1 = np.array([])
gNormalArray_hie1 = np.array([])

gVertexArrayIndexed_hie2 = np.array([])
gVertexArraySeperate_hie2 = np.array([])
gNormalArray_hie2 = np.array([])

gVertexArrayIndexed_curve = np.array([])
gVertexArraySeperate_curve = np.array([])
gNormalArray_curve = np.array([])

gVertexArrayIndexed_hie3 = np.array([])
gVertexArraySeperate_hie3 = np.array([])
gNormalArray_hie3 = np.array([])

mv_matrix = np.identity(4)
mv_sub1 = np.identity(4)
mv_sub2 = np.identity(4)

cam_matrix = np.identity(4)

select_v = 2

th = 0.
count = 0



def drawElement(Smoothing,gVertexArraySeperate,gNormalArray,gVertexArrayIndexed) :
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

def select_view(select_v) :
    if select_v == 3:
        gluLookAt(mv_matrix[0][3], 10+mv_matrix[1][3],mv_matrix[2][3], mv_matrix[0][3],-1,mv_matrix[2][3], 0,0,1)
    elif select_v == 1 :
        at = np.array([0,0,1,1])
        at = mv_matrix@at
        up = np.array([0,1,0,1])
        up = cam_matrix@up
        gluLookAt(mv_matrix[0][3], mv_matrix[1][3], mv_matrix[2][3], at[0], at[1], at[2], up[0],up[1],up[2])
    else :
        gluLookAt(10*np.sin(gCamAng), gCamHeight,10*np.cos(gCamAng), 0,0,0, 0,1,0)
        glTranslatef(gPanning_x, -gPanning_y, Zooming)
        glRotatef(gAzimuth, 1, 0, 0)
        glRotatef(gElevation, 0, 1, 0)


def render():
    global gCamAng, gCamHeight, Orbit, Panning, Toggle, Smoothing, gElevation, gAzimuth, gPanning_x, gPanning_y
    global mouse_x, mouse_y
    global gVertexArraySeperate_main, gNormalArray_main, gVertexArrayIndexed_main
    global gVertexArraySeperate_sub1, gNormalArray_sub1, gVertexArrayIndexed_sub1
    global gVertexArraySeperate_sub2, gNormalArray_sub2, gVertexArrayIndexed_sub2
    global gVertexArraySeperate_hie, gNormalArray_hie, gVertexArrayIndexed_hie
    global gVertexArraySeperate_hie1, gNormalArray_hie1, gVertexArrayIndexed_hie1
    global gVertexArraySeperate_hie2, gNormalArray_hie2, gVertexArrayIndexed_hie2
    global gVertexArraySeperate_curve, gNormalArray_curve, gVertexArrayIndexed_curve
    global gVertexArraySeperate_hie3, gNormalArray_hie3, gVertexArrayIndexed_hie3
    global mv_matrix, mv_sub1, mv_sub2, cam_matrix
    global select_v, th, count

    t = glfw.get_time()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 1, 45)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    select_view(select_v)
    
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
    lightPos1 = (0., 3., 3.*np.cos(t), 0.)
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

    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )


    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 0., 0., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()  #main object
    glMultMatrixf(np.ravel(mv_matrix.T,order='C')) 
    drawElement(Smoothing,gVertexArraySeperate_main,gNormalArray_main,gVertexArrayIndexed_main)
    
    glPushMatrix() #hierarchical model
    glMultMatrixf([0.2,0.,0.,0., 0.,0.2,0.,0., 0.,0.,0.2,0., 0.,0.,0.,1.,]) #scaling
    glRotatef(25*np.cos(t),1.,0.,0.) # rotate
    glTranslatef(0.,4.,10.)  #translation
    drawElement(Smoothing,gVertexArraySeperate_hie,gNormalArray_hie,gVertexArrayIndexed_hie)
    glPopMatrix()

    glPopMatrix()

    objectColor = (0., 1., 1., 1.)
    specularObjectColor = (1., 0., 0., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)


    glPushMatrix()
    glTranslatef(-3.,3.,3.*np.cos(t))
    glRotatef(100.*np.cos(t),0.,0.,1.)
    glMultMatrixf(np.ravel(mv_sub1.T,order='C'))    #sub1 object
    drawElement(Smoothing,gVertexArraySeperate_sub1,gNormalArray_sub1,gVertexArrayIndexed_sub1)

    glPushMatrix() #hierarchical model
    glMultMatrixf([0.2,0.,0.,0., 0.,0.2,0.,0., 0.,0.,0.2,0., 0.,0.,0.,1.,]) #scaling
    glRotatef(25*np.cos(t),0.,1.,0.) # rotate
    glTranslatef(0.,0.,10.)  #translation
    drawElement(Smoothing,gVertexArraySeperate_hie1,gNormalArray_hie1,gVertexArrayIndexed_hie1)
    glPopMatrix()

    glPopMatrix()

    objectColor = (1., 1., 0., 1.)
    specularObjectColor = (1., 0., 0., 1.) 
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    glTranslatef(3.,3.,-3.*np.cos(t))
    glMultMatrixf(np.ravel(mv_sub2.T,order='C'))    #sub2 object
    drawElement(Smoothing,gVertexArraySeperate_sub2,gNormalArray_sub2,gVertexArrayIndexed_sub2)

    glPushMatrix() #hierarchical model
    glMultMatrixf([0.2,0.,0.,0., 0.,0.2,0.,0., 0.,0.,0.2,0., 0.,0.,0.,1.,]) #scaling
    glRotatef(50*np.cos(t),0.,0.,1.) # rotate
    glTranslatef(10.,0.,0.)  #translation
    drawElement(Smoothing,gVertexArraySeperate_hie2,gNormalArray_hie2,gVertexArrayIndexed_hie2)
    glPopMatrix()


    glPopMatrix()

    objectColor = (1., 0., 1., 1.)
    specularObjectColor = (1., 0., 0., 1.) 
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    p0 = np.array([0.,0.,-5.,0.])
    p1 = np.array([-12.,0.,10.,0.])
    p2 = np.array([12.,0.,10.,0.])
    p3 = np.array([0.,0.,-5.,0.])
    if count == 200:
        th = 0
        count = 0
    else :
        th += 0.005
        count += 1
    
    tmp_vector = np.array([th*th*th, th*th, th, 1])@np.array([ [-1.,3.,-3.,1.], [3.,-6.,3.,0.], [-3.,3.,0.,0.], [1.,0.,0.,0.] ]) @ ([p0,p1,p2,p3])
    cur_mat = np.identity(4)
    cur_mat[0][3] = tmp_vector[0]
    cur_mat[1][3] = tmp_vector[1]
    cur_mat[2][3] = tmp_vector[2]
    glMultMatrixf(np.ravel(cur_mat.T,order='C'))  #object with moving curve
    drawElement(Smoothing,gVertexArraySeperate_curve,gNormalArray_curve,gVertexArrayIndexed_curve)
    
    glPushMatrix() #hierarchical model
    glMultMatrixf([0.2,0.,0.,0., 0.,0.2,0.,0., 0.,0.,0.2,0., 0.,0.,0.,1.,]) #scaling
    glRotatef(500*np.cos(t),0.,1.,0.) # rotate
    glTranslatef(10.,0.,0.)  #translation
    drawElement(Smoothing,gVertexArraySeperate_hie3,gNormalArray_hie3,gVertexArrayIndexed_hie3)
    glPopMatrix()
    
    glPopMatrix()

    glDisable(GL_LIGHTING)
    

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, Smoothing
    global mv_matrix, mv_sub1, mv_sub2, cam_matrix
    global select_v
    tmp_mat = np.identity(4)
    tmp_mat2 = np.identity(4)
    flag = False
    t = glfw.get_time()
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_S:
            if Smoothing:
                Smoothing = 0
            else:
                Smoothing = 1

        elif key==glfw.KEY_U:  #go
            tmp_mat[2][3] = 0.5
            flag = True
        elif key==glfw.KEY_J:  #back
            tmp_mat[2][3] = -0.5
            flag = True
        elif key==glfw.KEY_H:  #left
            tmp_mat[0][3] = 0.5
            flag = True
        elif key==glfw.KEY_K:  #right
            tmp_mat[0][3] = -0.5
            flag = True
        elif key==glfw.KEY_N:  #up
            tmp_mat[1][3] = 0.5
            flag = True
        elif key==glfw.KEY_M:  #down
            tmp_mat[1][3] = -0.5
            flag = True

        elif key==glfw.KEY_Y:  #rotate left
            tmp_mat[0][0] = np.cos(0.5)
            tmp_mat[0][2] = np.sin(0.5)
            tmp_mat[2][0] = -np.sin(0.5)
            tmp_mat[2][2] = np.cos(0.5)
            tmp_mat2[0][0] = np.cos(-0.5)
            tmp_mat2[0][2] = np.sin(-0.5)
            tmp_mat2[2][0] = -np.sin(-0.5)
            tmp_mat2[2][2] = np.cos(-0.5)
            flag = True
        elif key==glfw.KEY_I:  #rotate right
            tmp_mat[0][0] = np.cos(-0.5)
            tmp_mat[0][2] = np.sin(-0.5)
            tmp_mat[2][0] = -np.sin(-0.5)
            tmp_mat[2][2] = np.cos(-0.5)
            tmp_mat2[0][0] = np.cos(0.5)
            tmp_mat2[0][2] = np.sin(0.5)
            tmp_mat2[2][0] = -np.sin(0.5)
            tmp_mat2[2][2] = np.cos(0.5)
            flag = True

        elif key==glfw.KEY_O:  #size up
            tmp_mat[0][0] = 1.5
            tmp_mat[1][1] = 1.5
            tmp_mat[2][2] = 1.5
            flag = True
        elif key==glfw.KEY_P:  #size down
            tmp_mat[0][0] = 0.5
            tmp_mat[1][1] = 0.5
            tmp_mat[2][2] = 0.5
            flag = True
            

        elif key==glfw.KEY_V:  #shear x
            tmp_mat[0][1] = 0.1
            flag = True
        elif key==glfw.KEY_B:  #shear x
            tmp_mat[0][1] = -0.1
            flag = True

        elif key==glfw.KEY_G:  #reflect xz
            tmp_mat[1][1] = -1
            tmp_mat2[1][1] = -1
            flag = True

        elif key==glfw.KEY_8:  #default view
            select_v = 2
        elif key==glfw.KEY_9:  #first person view
            select_v = 1
        elif key==glfw.KEY_0:  #quarter view
            select_v = 3
        
            
        mv_matrix = mv_matrix@tmp_mat
        cam_matrix =cam_matrix@tmp_mat2
        

        if(flag) :
            tmp_sub1 = np.identity(4)
            tmp_sub1[2][3] = np.cos(t)
            tmp_sub1[0][3] = np.cos(t)
            mv_sub1 = mv_sub1@tmp_sub1

            tmp_sub2 = np.identity(4)
            tmp_sub2[2][3] = -np.cos(t)
            tmp_sub2[0][3] = -np.cos(t)
            mv_sub2 = mv_sub2@tmp_sub2
            

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


def load_file(paths):
    obj_file = open(paths, 'r')
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

    obj_file.close()
    return  gVertexArraySeperate, gNormalArray, gVertexArrayIndexed



def main():
    global gVertexArraySeperate_main, gNormalArray_main, gVertexArrayIndexed_main
    global gVertexArraySeperate_sub1, gNormalArray_sub1, gVertexArrayIndexed_sub1
    global gVertexArraySeperate_sub2, gNormalArray_sub2, gVertexArrayIndexed_sub2
    global gVertexArraySeperate_hie, gNormalArray_hie, gVertexArrayIndexed_hie
    global gVertexArraySeperate_hie1, gNormalArray_hie1, gVertexArrayIndexed_hie1
    global gVertexArraySeperate_hie2, gNormalArray_hie2, gVertexArrayIndexed_hie2
    global gVertexArraySeperate_curve, gNormalArray_curve, gVertexArrayIndexed_curve
    global gVertexArraySeperate_hie3, gNormalArray_hie3, gVertexArrayIndexed_hie3

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

    gVertexArraySeperate_main, gNormalArray_main, gVertexArrayIndexed_main = load_file("./cat.obj")
    gVertexArraySeperate_sub1, gNormalArray_sub1, gVertexArrayIndexed_sub1 = load_file("./cube2.obj")
    gVertexArraySeperate_sub2, gNormalArray_sub2, gVertexArrayIndexed_sub2 = load_file("./cube1.obj")
    gVertexArraySeperate_hie, gNormalArray_hie, gVertexArrayIndexed_hie = load_file("./sphere.obj")
    gVertexArraySeperate_hie1, gNormalArray_hie1, gVertexArrayIndexed_hie1 = load_file("./sphere.obj")
    gVertexArraySeperate_hie2, gNormalArray_hie2, gVertexArrayIndexed_hie2 = load_file("./sphere.obj")
    gVertexArraySeperate_curve, gNormalArray_curve, gVertexArrayIndexed_curve = load_file("./sphere.obj")
    gVertexArraySeperate_hie3, gNormalArray_hie3, gVertexArrayIndexed_hie3 = load_file("./sphere.obj")

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()