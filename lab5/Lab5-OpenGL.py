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

ortho = False
mv_x = 0
mv_y = 0
mv_z = 0
rot_x = 0
rot_y = 0
rot_z = 0

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

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation 

    
    #Your Code Here
    # from OpenGL.GL import glOrtho
    # from OpenGL.GLU import gluPerspective
    # from OpenGL.GL import glRotated
    # from OpenGL.GL import glTranslated
    # from OpenGL.GL import glLoadIdentity
    # from OpenGL.GL import glMatrixMode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if ortho:
        glOrtho(-10.0, 10.0, -10.0, 10.0, -100.0, 100.0)
    else:
        gluPerspective(45.0, DISPLAY_WIDTH / DISPLAY_HEIGHT, .1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslated(0.0,0.0,0.0)

    glRotated(-rot_y,0,1,0)

    glTranslated(mv_x,mv_y,mv_z)
    
    drawHouse()

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
        rot_y+=1
    if key == b'e':
        rot_y-=1
    if key == b'r':
        mv_y-=1
    if key == b'f':
        mv_y+=1
    if key == b'h':
        mv_x=0
        mv_y=-2
        mv_z=-20
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
glutMainLoop()