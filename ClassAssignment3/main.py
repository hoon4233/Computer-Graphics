import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import *
import ctypes
import math


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


gDepth = 0

obj = None
count = 0

gToggle = False

gVertexArrayIndexed = np.array([])
gIndexArray = np.array([])


class Joint:
    def __init__(self):
        self.name = None
        self.channels = []
        self.offset = []
        self.parent = None
        self.children = []
        self.frames = []
        self.idx = [0, 0]
        self.rot_mat = np.identity(4)
        self.trans_mat = np.identity(4)
        self.strans_mat = np.identity(4)
        self.localtoworld = np.identity(4)
        self.trtr = np.identity(4)
        self.worldpos = np.array([0, 0, 0, 0])


    def updateFrame(self, frame):
        pos = [0., 0., 0.]
        rot = [0., 0., 0.]

        rot_mat = np.identity(4)
        trans_mat = np.identity(4)

        for idx, channel in enumerate(self.channels):
            if channel == 'Xposition':
                pos[0] = self.frames[frame][idx]
                trans_mat[0, 3] = pos[0]
            elif channel == 'Yposition':
                pos[1] = self.frames[frame][idx]
                trans_mat[1, 3] = pos[1]
            elif channel == 'Zposition':
                pos[2] = self.frames[frame][idx]
                trans_mat[2, 3] = pos[2]
            else:
                rot[0] = self.frames[frame][idx]
                if channel == 'Xrotation':
                    rot_mat2 = np.identity(4)
                    rot_mat2[1, 1] = np.cos(np.radians(rot[0]))
                    rot_mat2[1, 2] = -np.sin(np.radians(rot[0]))
                    rot_mat2[2, 1] = np.sin(np.radians(rot[0]))
                    rot_mat2[2, 2] = np.cos(np.radians(rot[0]))
                elif channel == 'Yrotation':
                    rot_mat2 = np.identity(4)
                    rot_mat2[0, 0] = np.cos(np.radians(rot[0]))
                    rot_mat2[0, 2] = np.sin(np.radians(rot[0]))
                    rot_mat2[2, 0] = -np.sin(np.radians(rot[0]))
                    rot_mat2[2, 2] = np.cos(np.radians(rot[0]))
                elif channel == 'Zrotation':
                    rot_mat2 = np.identity(4)
                    rot_mat2[0, 0] = np.cos(np.radians(rot[0]))
                    rot_mat2[0, 1] = -np.sin(np.radians(rot[0]))
                    rot_mat2[1, 0] = np.sin(np.radians(rot[0]))
                    rot_mat2[1, 1] = np.cos(np.radians(rot[0]))
                rot_mat = np.dot(rot_mat, rot_mat2)

        self.rot_mat = rot_mat
        self.trans_mat = trans_mat

        if self.parent:
            self.localtoworld = np.dot(self.parent.trtr, self.strans_mat)
        else:
            self.localtoworld = np.dot(self.strans_mat, self.trans_mat)

        self.trtr = np.dot(self.localtoworld, self.rot_mat)

        self.worldpos = np.array([self.localtoworld[0, 3],
                                  self.localtoworld[1, 3],
                                  self.localtoworld[2, 3],
                                  self.localtoworld[3, 3]])

        for child in self.children:
            child.updateFrame(frame)




class ParseBvh:
    def __init__(self, filename, frames = 0, frame_per_s = .01):
        self.filename = filename
        self.__root = None
        self.stack = []
        self.channel_num = 0
        self.frames = frames
        self.frame_per_s = frame_per_s
        self.motions = []
        self.readBVH(self.filename)

    @property
    def root(self):
        return self.__root

    def printInfo(self,jointList):
        print("Number of frames: " + str(self.frames))
        print("FPS: " +  str((1 / self.frame_per_s)))
        print("Number of Joints: " + str(len(jointList)))
        print("List of all Joint names: " + str(jointList))
    
    def get_channel_data(self, joint, data):
        channels = len(joint.channels)
        joint.frames.append(data[0:channels])
        data = data[channels:]

        for child in joint.children:
            data = self.get_channel_data(child, data)

        return data

    def update_frame(self, frame):
        self.root.update_frame(frame)


    def readBVH(self, filename):
        global gDepth
        f = open(filename)
        lines = f.readlines()
        parent = None
        current = None
        jointList = []
        motion = False

        for line in lines[1:len(lines)]:
            tokens = line.split()
            if len(tokens) == 0:
                continue
            if tokens[0] in ["ROOT", "JOINT", "End"]:
                if current is not None:
                    parent = current

                current = Joint()
                current.name = tokens[1]
                jointList.append(current.name)

                current.parent = parent
                if len(self.stack) == 0:
                    self.__root = current

                if current.parent is not None:
                    current.parent.children.append(current)

                self.stack.append(current)
            elif "{" in tokens[0]:
                pass
            elif "OFFSET" in tokens[0]:
                offset = []
                for i in range(1, len(tokens)):
                    offset.append(float(tokens[i]))
                    if gDepth < abs(float(tokens[i])):
                        gDepth = abs(float(tokens[i]))
                current.offset = offset
                current.strans_mat[0, 3] = offset[0]
                current.strans_mat[1, 3] = offset[1]
                current.strans_mat[2, 3] = offset[2]
            elif "CHANNELS" in tokens[0]:
                current.channels = tokens[2:len(tokens)]
                current.idx = [self.channel_num,
                               self.channel_num + len(current.channels)]
                self.channel_num += len(current.channels)
            elif "}" in tokens[0]:
                current = current.parent
                if current:
                    parent = current.parent
            elif "MOTION" in tokens[0]:
                motion = True
            elif "Frames:" in tokens[0]:
                self.frames = int(tokens[1])
            elif "Frame" in tokens[0]:
                self.frame_per_s = float(tokens[2])
            elif motion:
                data = [float(token) for token in tokens]
                self.get_channel_data(self.__root, data)
                vals = []
                for token in tokens:
                    vals.append(float(token))
                self.motions.append(vals)
        self.printInfo(jointList)
        



def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-500.,0.,0.]))
    glVertex3fv(np.array([500.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,500.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,-500.]))
    glVertex3fv(np.array([0.,0.,500.]))
    glEnd()

def drawGrid():
    # Gray Color
    glColor3ub(255, 255, 255)
    glBegin(GL_QUADS)
    glVertex3f(500., 0., 500.)
    glVertex3f(-500., 0., 500.)
    glVertex3f(-500., 0., -500.)
    glVertex3f(500., 0., -500.)
    glEnd()

    glBegin(GL_LINES)
    for i in range(-500, 500, 50):
        if i == 0:
            continue
        glVertex3f(i, 0., -500.)
        glVertex3f(i, 0., 500.)
        glVertex3f(-500., 0., i)
        glVertex3f(500., 0., i)
    glEnd()

def rotationMatrix(rot_mat, xyz, r):
    cos = np.cos(r)
    sin = np.sin(r)
    if xyz == "X":
        rotation_matrix = np.array([[1., 0., 0., 0.],
                                     [0., cos, -sin, 0.],
                                     [0., sin, cos, 0.],
                                     [0., 0., 0., 1.]])
    elif xyz == "Y":
        rotation_matrix = np.array([[cos, 0., sin, 0.],
                                     [0., 1., 0, 0.],
                                     [-sin, 0, cos, 0.],
                                     [0., 0., 0., 1.]])
    elif xyz == "Z":
        rotation_matrix = np.array([[cos, -sin, 0., 0.],
                                     [sin, cos, 0., 0.],
                                     [0., 0., 1., 0.],
                                     [0., 0., 0., 1.]])
    return np.dot(rot_mat, rotation_matrix)


def createVertexAndIndexArrayIndexed(x, y, z):
    factor = max(abs(x),abs(y),abs(z)) 
    x = float(x) 
    y = float(y) 
    z = float(z) 

    if factor == abs(x) :
        x *= 0.85
    elif factor == abs(y) :
        y *= 0.85
    else:
        z *= 0.85 

    factor = (factor + gDepth) /15
            
    if abs(x) <= factor * 0.001:
        x = factor * np.sign(x) 
    if abs(y) <= factor * 0.001:
        y = factor * np.sign(y) 
    if abs(z) <= factor * 0.001:
        z = factor * np.sign(z) 

    x /= 2.5
    y /= 2.5
    z /= 2.5
    
    varr = np.array([
        ( -0.5773502691896258 , 0.5773502691896258 , 0.5773502691896258 ),
        [-x, y, z],
        ( 0.8164965809277261 , 0.4082482904638631 , 0.4082482904638631 ),
        [x, y, z],
        ( 0.4082482904638631 , -0.4082482904638631 , 0.8164965809277261 ),
        [x, -y, z],
        ( -0.4082482904638631 , -0.8164965809277261 , 0.4082482904638631 ),
        [-x, -y, z],
        ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
        [-x, y, -z],
        ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
        [x, y, -z],
        ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
        [x, -y, -z],
        ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
        [-x, -y,-z],
        ], 'float32')

   
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)


def drawObj(joint, obj, count, toggle):
    global gVertexArrayIndexed, gIndexArray
    global gToggle
    offset = joint.offset
    pos = [0, 0, 0]
    rot_mat = np.identity(4)

    offset = np.array([float(offset[0]), float(offset[1]), float(offset[2])])

    if gToggle == True:
        for j in range(len(joint.channels)):

            i = joint.idx[0] + j
            channel = joint.channels[j]

            if channel.upper() == "XPOSITION":
                pos[0] = obj.motions[count][i]
            elif channel.upper() == "YPOSITION":
                pos[1] = obj.motions[count][i]
            elif channel.upper() == "ZPOSITION":
                pos[2] = obj.motions[count][i]
            else:
                rot_mat = rotationMatrix(rot_mat, channel[0].upper(), np.radians(obj.motions[count][i]))

    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])


    # default
    # if toggle == True:
    #     glBegin(GL_LINES)
    #     glColor3ub(255, 255, 0)
    #     glVertex3f(0, 0, 0)
    #     glVertex3f(offset[0], offset[1], offset[2])
    #     glEnd()
    #     glTranslatef(offset[0], offset[1], offset[2])


    # # extra credit 1
    if toggle == True:
        gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed(offset[0], offset[1], offset[2])
        drawCube_glDrawElements()
        glTranslatef(offset[0], offset[1], offset[2])

    glMultMatrixf(rot_mat.T)

    for child in joint.children:
        drawObj(child, obj, count, True)
    glPopMatrix()


def render(count):
    global gCamAng, gCamHeight, Orbit, Panning, Zooming, gElevation, gAzimuth, gPanning_x, gPanning_y
    global mouse_x, mouse_y
    global obj

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 1, 1000000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(500*np.sin(gCamAng), gCamHeight,500*np.cos(gCamAng), 0,0,0, 0,1,0)
    glTranslatef(gPanning_x, -gPanning_y, Zooming)
    glRotatef(gAzimuth, 1, 0, 0)
    glRotatef(gElevation, 0, 1, 0)
    
    drawFrame()
    glColor3ub(255, 255, 255)
    drawGrid()

    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

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

    if obj is not None:
        if count == obj.frames:
            count = 0
        drawObj(obj.root, obj, int(count / 2) % obj.frames, False)

    glDisable(GL_LIGHTING)

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, gToggle, count
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_SPACE:
            if gToggle :
                gToggle = False
                count = 0
            else:
                gToggle = True
            

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
        # Zooming += 0.5
        Zooming += 5.
    if yoffset < 0:
        # Zooming -= 0.5
        Zooming -= 5.


def drop_callback(window, paths):
    global obj, count, gToggle
    gToggle = False
    count = 0
    
    if "/" in paths[0]:
            name = paths[0].split("/")
    elif "\\" in paths[0]:
        name = paths[0].split("\\")
    print("File name:" + name[len(name)-1])

    obj = ParseBvh(paths[0])




def main():
    global gToggle, count
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 800, "2016025105", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)

    

    # Loop until the user closes the window
    count = 0
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render(count)
        # Swap front and back buffers
        glfw.swap_buffers(window)
        if gToggle == True:
            count += 1

    glfw.terminate()
if __name__ == "__main__":
    main()