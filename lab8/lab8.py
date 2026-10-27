""" Modified code from Peter Colling Ridge 
	Original found at http://www.petercollingridge.co.uk/pygame-3d-graphics-tutorial
"""

import pygame
import math
import numpy as np
import wireframe as wf
import basicShapes as shape

class WireframeViewer(wf.WireframeGroup):
    """ A group of wireframes which can be displayed on a Pygame screen """
    
    def __init__(self, width, height, name="Wireframe Viewer"):
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        
        self.wireframes = {}
        self.wireframe_colours = {}
        self.object_to_update = []
        
        self.displayNodes = False
        self.displayEdges = True
        self.displayFaces = True
        
        self.perspective = False
        self.eyeX = self.width/2
        self.eyeY = 100
        self.light_color = np.array([1,1,1])
        self.view_vector = np.array([0, 0, -1])        
        self.light_vector = np.array([0, 0, -1])  

        self.background = (10,10,50)
        self.nodeColour = (250,250,250)
        self.nodeRadius = 4
        
        self.control = 0
        self.rotx = 0
        self.roty = 0
        self.rotz = 0
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
        #   If colour is set to None, then wireframe is not displayed
        self.wireframe_colours[name] = (250,250,250)
    
    def addWireframeGroup(self, wireframe_group):
        # Potential danger of overwriting names
        for name, wireframe in wireframe_group.wireframes.items():
            self.addWireframe(name, wireframe)

    def make_x_rotate_matrix(self,rx):
        return np.array(
            [
                [1, 0, 0, 0],
                [0, math.cos(rx), -math.sin(rx), 0],
                [0, math.sin(rx), math.cos(rx), 0],
                [0, 0, 0, 1],
            ]
        )


    def make_y_rotate_matrix(self,ry):
        return np.array(
            [
                [math.cos(ry), 0, math.sin(ry), 0],
                [0, 1, 0, 0],
                [-math.sin(ry), 0, math.cos(ry), 0],
                [0, 0, 0, 1],
            ]
        )


    def make_z_rotate_matrix(self,rz):
        return np.array(
            [
                [math.cos(rz), -math.sin(rz), 0, 0],
                [math.sin(rz), math.cos(rz), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )


    def phongDiffuse(self,kd,lp,od,N,L):
        N = N/np.linalg.norm(N)
        L = L/np.linalg.norm(L)
        nl = max(np.dot(N,L),0.0)
        return kd*lp*od*nl
    
    def phongSpecular(self,ks,lp,os,V,R,kgls):
        V = V/np.linalg.norm(V)
        R = R/np.linalg.norm(R)
        vr = max(np.dot(V,R),0.0)
        return ks*lp*os*(vr)**kgls

    def display(self):
        self.screen.fill(self.background)

        for name, wireframe in self.wireframes.items():
            nodes = wireframe.nodes
            
            if self.displayFaces:
                for (face, colour) in wireframe.sortedFaces():
                    v1 = (nodes[face[1]] - nodes[face[0]])[:3]
                    v2 = (nodes[face[2]] - nodes[face[0]])[:3]

                    normal = np.cross(v1, v2)
                    normal /= np.linalg.norm(normal)
                    towards_us = np.dot(normal, self.view_vector)

                    # Only draw faces that face us
                    if towards_us > 0:
                        m_ambient = 0.1
                        ambient = self.light_color * (m_ambient * colour)

                        #Your lighting code here
                        #Make note of the self.view_vector and self.light_vector 
                        #Use the Phong model
                        if (np.dot(normal,self.light_vector) < 0):
                            diffuse = 0
                            specular = 0
                        else:
                            kd = .6
                            diffuse = self.phongDiffuse(kd,self.light_color,colour,normal,self.light_vector)

                            ks = .3
                            kgls = 16
                            r = 2*(np.dot(self.light_vector,normal))*normal-self.light_vector
                            specular = self.phongSpecular(ks,self.light_color,colour,self.view_vector,r,kgls)

						#Once you have implemented diffuse and specular lighting, you will want to include them here
                        light_total = ambient + diffuse + specular
                        light_total = np.clip(light_total,0,255)

                        pygame.draw.polygon(self.screen, light_total, [(nodes[node][0], nodes[node][1]) for node in face], 0)

                if self.displayEdges:
                    for (n1, n2) in wireframe.edges:
                        if self.perspective:
                            if wireframe.nodes[n1][2] > -self.perspective and nodes[n2][2] > -self.perspective:
                                z1 = self.perspective/ (self.perspective + nodes[n1][2])
                                x1 = self.width/2  + z1*(nodes[n1][0] - self.width/2)
                                y1 = self.height/2 + z1*(nodes[n1][1] - self.height/2)
                    
                                z2 = self.perspective/ (self.perspective + nodes[n2][2])
                                x2 = self.width/2  + z2*(nodes[n2][0] - self.width/2)
                                y2 = self.height/2 + z2*(nodes[n2][1] - self.height/2)
                                
                                pygame.draw.aaline(self.screen, colour, (x1, y1), (x2, y2), 1)
                        else:
                            pygame.draw.aaline(self.screen, colour, (nodes[n1][0], nodes[n1][1]), (nodes[n2][0], nodes[n2][1]), 1)

            if self.displayNodes:
                for node in nodes:
                    pygame.draw.circle(self.screen, colour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
        
        pygame.display.flip()

    def keyEvent(self, key):
        #Your code here
        mag = 15 # how much to rotate in degrees
        lv_homo = np.append(self.light_vector,1)
        if key == pygame.K_a:
            rot_matrix = self.make_y_rotate_matrix(math.radians(mag))
            temp = np.matmul(rot_matrix,lv_homo)[:-1]
            self.light_vector = temp / np.linalg.norm(temp)
        if key == pygame.K_d:
            rot_matrix = self.make_y_rotate_matrix(math.radians(-mag))
            temp = np.matmul(rot_matrix,lv_homo)[:-1]
            self.light_vector = temp / np.linalg.norm(temp)
        if key == pygame.K_w:
            rot_matrix = self.make_x_rotate_matrix(math.radians(-mag))
            temp = np.matmul(rot_matrix,lv_homo)[:-1]
            self.light_vector = temp / np.linalg.norm(temp)
        if key == pygame.K_s:
            rot_matrix = self.make_x_rotate_matrix(math.radians(mag))
            temp = np.matmul(rot_matrix,lv_homo)[:-1]
            self.light_vector = temp / np.linalg.norm(temp)
        if key == pygame.K_q:
            rot_matrix = self.make_z_rotate_matrix(math.radians(-mag))
            temp = np.matmul(rot_matrix,lv_homo)[:-1]
            self.light_vector = temp / np.linalg.norm(temp)
        if key == pygame.K_e:
            rot_matrix = self.make_z_rotate_matrix(math.radians(mag))
            temp = np.matmul(rot_matrix,lv_homo)[:-1]
            self.light_vector = temp / np.linalg.norm(temp)

        return

    def run(self):
        """ Display wireframe on screen and respond to keydown events """
        
        running = True
        key_down = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_down = event.key
                elif event.type == pygame.KEYUP:
                    key_down = None
            
            if key_down:
                self.keyEvent(key_down)
            
            self.display()
            self.update()
            
        pygame.quit()

		
resolution = 52
viewer = WireframeViewer(600, 400)
viewer.addWireframe('sphere', shape.Spheroid((300,200, 20), (160,160,160), resolution=resolution))

# Colour ball
faces = viewer.wireframes['sphere'].faces
for i in range(int(resolution/4)):
	for j in range(resolution*2-4):
		f = i*(resolution*4-8) +j
		faces[f][1][1] = 0
		faces[f][1][2] = 0
	
viewer.displayEdges = False
viewer.run()
