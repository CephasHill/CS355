import sys
import math

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except:
    print("ERROR: PyOpenGL not installed properly. ")

DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0

M_SECONDS = 10
time = 0 # in seconds

ortho = False
mv_x = 0
mv_y = 0
mv_z = 0
rot_x = 0
rot_y = 0
rot_z = 0

wheel_radius = 2
wheel_trans = 4
wheel_rot = -wheel_trans/wheel_radius


def incrementTime(value):
    global time
    time+=.01
    glutTimerFunc(M_SECONDS, incrementTime, value)
    glutPostRedisplay()
    # print(time)


def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

 
def drawCar():
	glLineWidth(2.5)
	glColor3f(0.0, 1.0, 0.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-3, 2, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 2, 2)
	#Back Side
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 2, -2)
	#Connectors
	glVertex3f(-3, 2, 2)
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, -2)
	glEnd()
	
def drawTire():
	glLineWidth(2.5)
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-1, .5, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, .5, .5)
	#Back Side
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, .5, -.5)
	#Connectors
	glVertex3f(-1, .5, .5)
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, -.5)
	glEnd()
		


def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation 

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if ortho:
        glOrtho(-10.0, 10.0, -10.0, 10.0, -100.0, 100.0)
    else:
        gluPerspective(45.0, DISPLAY_WIDTH / DISPLAY_HEIGHT, .1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # INITIAL POS + ROT LOGIC
    glPushMatrix()
    glRotatef(-rot_y,0,1,0)
    glTranslatef(mv_x,mv_y,mv_z-40)

        # HOUSES
        # 0 1 2 3 4
        # 5 0 0 0 0
        # 0 6 7 8 9
    # 1
    glPushMatrix()
    glTranslatef(mv_x,mv_y,mv_z)
    drawHouse()
    glPopMatrix()

    # 2
    glPushMatrix()
    glTranslatef(mv_x + 15, mv_y, mv_z)
    drawHouse()
    glPopMatrix()

    # 3
    glPushMatrix()
    glTranslatef(mv_x+30, mv_y, mv_z)
    drawHouse()
    glPopMatrix()

    # 4
    glPushMatrix()
    glTranslatef(mv_x+45, mv_y, mv_z)
    drawHouse()
    glPopMatrix()

    # 5
    glPushMatrix()
    glTranslatef(mv_x-15, mv_y, mv_z+15)
    glRotatef(90, 0, 1, 0)
    drawHouse()
    glPopMatrix()

    # 6
    glPushMatrix()
    glTranslatef(mv_x, mv_y, mv_z+30)
    glRotatef(180, 0, 1, 0)
    drawHouse()
    glPopMatrix()

    # 7
    glPushMatrix()
    glTranslatef(mv_x+15, mv_y, mv_z+30)
    glRotatef(180, 0, 1, 0)
    drawHouse()
    glPopMatrix()

    # 8
    glPushMatrix()
    glTranslatef(mv_x+30, mv_y, mv_z+30)
    glRotatef(180, 0, 1, 0)
    drawHouse()
    glPopMatrix()

    # 9
    glPushMatrix()
    glTranslatef(mv_x+45, mv_y, mv_z+30)
    glRotatef(180, 0, 1, 0)
    drawHouse()
    glPopMatrix()

        # CAR
    glPushMatrix()
    glTranslatef(mv_x,mv_y+1,mv_z+20) # initial pos
    glTranslatef(wheel_trans*time,0,0)
    drawCar()

            # TIRES
    glPushMatrix()
    glTranslatef(2.5,0,1.5)
    glRotatef(wheel_rot*time*100,0,0,1)
    drawTire()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2.5,0,-1.5)
    glRotatef(wheel_rot*time*100,0,0,1)
    drawTire()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-2.5,0,1.5)
    glRotatef(wheel_rot*time*100,0,0,1)
    drawTire()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-2.5,0,-1.5)
    glRotatef(wheel_rot*time*100,0,0,1)
    drawTire()
    glPopMatrix()

    # INIT POP
    glPopMatrix()

    # EVERYTHING POP
    glPopMatrix()

    glFlush()
    

def keyboard(key, x, y):
    global mv_x, mv_y, mv_z, rot_y, ortho
    
    if key == chr(27):
        import sys
        sys.exit(0)
  
    if key == b'a':
        mv_x += math.cos(math.radians(rot_y))
        mv_z -= math.sin(math.radians(rot_y))
    if key == b'd':
        mv_x -= math.cos(math.radians(rot_y))
        mv_z += math.sin(math.radians(rot_y))
    if key == b'w':
        mv_x += math.sin(math.radians(rot_y))
        mv_z += math.cos(math.radians(rot_y))
    if key == b's':
        mv_x -= math.sin(math.radians(rot_y))
        mv_z -= math.cos(math.radians(rot_y))
    if key == b'q':
        rot_y+=3.65
    if key == b'e':
        rot_y-=3.65
    if key == b'r':
        mv_y-=1
    if key == b'f':
        mv_y+=1
    if key == b'h':
        mv_x=0
        mv_y=0
        mv_z=0
        rot_y=0
    if key == b'o':
        ortho = True
    if key == b'p':
        ortho = False
  
    #Your Code Here
  
    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

glutTimerFunc(M_SECONDS, incrementTime, 1)

glutMainLoop()