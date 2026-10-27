# Import a library of functions called 'pygame'
import math
import pygame
import numpy as np
from typing import List
# from math import pi


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Line3D:
    def __init__(self, start: Point3D, end: Point3D):
        self.start = start
        self.end = end


class Line4D:
    def __init__(self, start: list, end: list):
        self.start = start
        self.end = end


def load_obj(filename):
    vertices = []
    indices = []
    lines = []

    f = open(filename, "r")
    for line in f:
        t = str.split(line)
        if not t:
            continue
        if t[0] == "v":
            vertices.append(Point3D(float(t[1]), float(t[2]), float(t[3])))

        if t[0] == "f":
            for i in range(1, len(t) - 1):
                index1 = int(str.split(t[i], "/")[0])
                index2 = int(str.split(t[i + 1], "/")[0])
                indices.append((index1, index2))

    f.close()

    # Add faces as lines
    for index_pair in indices:
        index1 = index_pair[0]
        index2 = index_pair[1]
        lines.append(Line3D(vertices[index1 - 1], vertices[index2 - 1]))

    # Find duplicates
    duplicates = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            line1 = lines[i]
            line2 = lines[j]

            # Case 1 -> Starts match
            if (
                line1.start.x == line2.start.x
                and line1.start.y == line2.start.y
                and line1.start.z == line2.start.z
            ):
                if (
                    line1.end.x == line2.end.x
                    and line1.end.y == line2.end.y
                    and line1.end.z == line2.end.z
                ):
                    duplicates.append(j)
            # Case 2 -> Start matches end
            if (
                line1.start.x == line2.end.x
                and line1.start.y == line2.end.y
                and line1.start.z == line2.end.z
            ):
                if (
                    line1.end.x == line2.start.x
                    and line1.end.y == line2.start.y
                    and line1.end.z == line2.start.z
                ):
                    duplicates.append(j)

    duplicates = list(set(duplicates))
    duplicates.sort()
    duplicates = duplicates[::-1]

    # Remove duplicates
    for j in range(len(duplicates)):
        del lines[duplicates[j]]

    return lines


def load_house():
    house = []
    # Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    # Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    # Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    # Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    # Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))

    return house


def load_car():
    car = []
    # Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    # Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))

    # Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car


def load_tire():
    tire = []
    # Front Side
    tire.append(Line3D(Point3D(-1, 0.5, 0.5), Point3D(-0.5, 1, 0.5)))
    tire.append(Line3D(Point3D(-0.5, 1, 0.5), Point3D(0.5, 1, 0.5)))
    tire.append(Line3D(Point3D(0.5, 1, 0.5), Point3D(1, 0.5, 0.5)))
    tire.append(Line3D(Point3D(1, 0.5, 0.5), Point3D(1, -0.5, 0.5)))
    tire.append(Line3D(Point3D(1, -0.5, 0.5), Point3D(0.5, -1, 0.5)))
    tire.append(Line3D(Point3D(0.5, -1, 0.5), Point3D(-0.5, -1, 0.5)))
    tire.append(Line3D(Point3D(-0.5, -1, 0.5), Point3D(-1, -0.5, 0.5)))
    tire.append(Line3D(Point3D(-1, -0.5, 0.5), Point3D(-1, 0.5, 0.5)))

    # Back Side
    tire.append(Line3D(Point3D(-1, 0.5, -0.5), Point3D(-0.5, 1, -0.5)))
    tire.append(Line3D(Point3D(-0.5, 1, -0.5), Point3D(0.5, 1, -0.5)))
    tire.append(Line3D(Point3D(0.5, 1, -0.5), Point3D(1, 0.5, -0.5)))
    tire.append(Line3D(Point3D(1, 0.5, -0.5), Point3D(1, -0.5, -0.5)))
    tire.append(Line3D(Point3D(1, -0.5, -0.5), Point3D(0.5, -1, -0.5)))
    tire.append(Line3D(Point3D(0.5, -1, -0.5), Point3D(-0.5, -1, -0.5)))
    tire.append(Line3D(Point3D(-0.5, -1, -0.5), Point3D(-1, -0.5, -0.5)))
    tire.append(Line3D(Point3D(-1, -0.5, -0.5), Point3D(-1, 0.5, -0.5)))

    # Connectors
    tire.append(Line3D(Point3D(-1, 0.5, 0.5), Point3D(-1, 0.5, -0.5)))
    tire.append(Line3D(Point3D(-0.5, 1, 0.5), Point3D(-0.5, 1, -0.5)))
    tire.append(Line3D(Point3D(0.5, 1, 0.5), Point3D(0.5, 1, -0.5)))
    tire.append(Line3D(Point3D(1, 0.5, 0.5), Point3D(1, 0.5, -0.5)))
    tire.append(Line3D(Point3D(1, -0.5, 0.5), Point3D(1, -0.5, -0.5)))
    tire.append(Line3D(Point3D(0.5, -1, 0.5), Point3D(0.5, -1, -0.5)))
    tire.append(Line3D(Point3D(-0.5, -1, 0.5), Point3D(-0.5, -1, -0.5)))
    tire.append(Line3D(Point3D(-1, -0.5, 0.5), Point3D(-1, -0.5, -0.5)))

    return tire


mv_x = 0
mv_y = 0
mv_z = 0
rot_x = 0
rot_y = 0
rot_z = 0
cam_speed = 1
universal_scale = [10, 10, 10]


def homogenize(orig_o: List[Line3D]):
    o: List[Line4D] = []

    for line3d in orig_o:
        start = [line3d.start.x, line3d.start.y, line3d.start.z, 1]
        end = [line3d.end.x, line3d.end.y, line3d.end.z, 1]
        o.append(Line4D(start, end))
    return o


def make_x_rotate_matrix(rx):
    return np.array(
        [
            [1, 0, 0, 0],
            [0, math.cos(rx), -math.sin(rx), 0],
            [0, math.sin(rx), math.cos(rx), 0],
            [0, 0, 0, 1],
        ]
    )


def make_y_rotate_matrix(ry):
    return np.array(
        [
            [math.cos(ry), 0, math.sin(ry), 0],
            [0, 1, 0, 0],
            [-math.sin(ry), 0, math.cos(ry), 0],
            [0, 0, 0, 1],
        ]
    )


def make_z_rotate_matrix(rz):
    return np.array(
        [
            [math.cos(rz), -math.sin(rz), 0, 0],
            [math.sin(rz), math.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def make_scale_matrix(x, y, z):
    return np.array([[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])


def make_translate_matrix(x, y, z):
    return np.array([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])


def make_transformation_matrix(
    t: list = [0, 0, 0], r: list = [0, 0, 0], s: list = universal_scale
):
    rx = math.radians(r[0])
    ry = math.radians(r[1])
    rz = math.radians(r[2])
    translate_matrix = make_translate_matrix(t[0], t[1], t[2])
    scale_matrix = make_scale_matrix(s[0], s[1], s[2])
    x_rotate_matrix = make_x_rotate_matrix(rx)
    y_rotate_matrix = make_y_rotate_matrix(ry)
    z_rotate_matrix = make_z_rotate_matrix(rz)
    rotate_matrix = np.matmul(z_rotate_matrix, np.matmul(y_rotate_matrix, x_rotate_matrix))

    return np.matmul(translate_matrix, np.matmul(rotate_matrix, scale_matrix))


# Object space to world space
def object_to_world(
    orig_o: List[Line3D],
    t: List[float] = [0, 0, 0],
    r: List[float] = [0, 0, 0],
    s: List[float] = universal_scale,
    transform_matrix=None,
) -> List[Line3D]:
    world_space_lines: List[Line3D] = []
    if transform_matrix is None:
        rx = math.radians(r[0])
        ry = math.radians(r[1])
        rz = math.radians(r[2])
        translate_matrix = make_translate_matrix(t[0], t[1], t[2])
        scale_matrix = make_scale_matrix(s[0], s[1], s[2])
        x_rotate_matrix = make_x_rotate_matrix(rx)
        y_rotate_matrix = make_y_rotate_matrix(ry)
        z_rotate_matrix = make_z_rotate_matrix(rz)
        rotate_matrix = np.matmul(z_rotate_matrix, np.matmul(y_rotate_matrix, x_rotate_matrix))

        transform_matrix = np.matmul(translate_matrix, np.matmul(rotate_matrix, scale_matrix))

    for line in orig_o:
        start = np.array([line.start.x, line.start.y, line.start.z, 1])
        end = np.array([line.end.x, line.end.y, line.end.z, 1])

        new_line_start_vector = np.matmul(transform_matrix, start)[:-1]
        new_line_end_vector = np.matmul(transform_matrix, end)[:-1]

        new_start = Point3D(new_line_start_vector[0], new_line_start_vector[1], new_line_start_vector[2])
        new_end = Point3D(new_line_end_vector[0], new_line_end_vector[1], new_line_end_vector[2])
        world_space_lines.append(Line3D(new_start, new_end))

    return world_space_lines


def world_to_camera(
    orig_o: List[Line3D],
    p_from: List[float] = [0, 0, 0],
    p_at: List[float] = [0, 0, 1],
    v_up: List[float] = [0, 1, 0],
):
    p_from = np.array(p_from)
    p_at = np.array(p_at)
    v_up = np.array(v_up)

    e3 = (p_at - p_from) / np.linalg.norm(p_at - p_from)
    e1 = (np.cross(e3, v_up)) / np.linalg.norm(np.cross(e3, v_up))
    e2 = (np.cross(e1, e3)) / np.linalg.norm(np.cross(e1, e3))

    translate_matrix = make_translate_matrix(-p_from[0], -p_from[1], -p_from[2])
    rotate_matrix = np.array(
        [
            [e1[0], e1[1], e1[2], 0],
            [e2[0], e2[1], e2[2], 0],
            [e3[0], e3[1], e3[2], 0],
            [0, 0, 0, 1],
        ]
    )
    transform_matrix = np.matmul(rotate_matrix, translate_matrix)

    o: List[Line4D] = []

    hom_o = homogenize(orig_o)

    for line in hom_o:
        start = np.matmul(transform_matrix, line.start)
        end = np.matmul(transform_matrix, line.end)
        o.append(Line4D(start, end))
    return o


def check_clipping(p0, p1, n, f):
    x0, x1 = p0[0], p1[0]
    y0, y1 = p0[1], p1[1]
    z0, z1 = p0[2], p1[2]

    if x0 > size[0] or x1 > size[0]:
        return None
    if x0 < -size[0] or x1 < -size[0]:
        return None
    if y0 > size[1] or y1 > size[1]:
        return None
    if y0 < -size[1] or y1 < -size[1]:
        return None
    if (z0 < n or z1 < n) or (z0 > f and z1 > f):
        return None

    return p0, p1


def project_with_clipping(orig_o: List[Line4D], f: float, n: float, zoom_x, zoom_y):
    clip_matrix = np.array(
        [
            [zoom_x, 0, 0, 0],
            [0, zoom_y, 0, 0],
            [0, 0, (f + n) / (f - n), (-2 * n * f) / (f - n)],
            [0, 0, 1, 0],
        ]
    )
    o: List[Line3D] = []
    for line in orig_o:
        clipped = check_clipping(line.start[:3], line.end[:3], n, f)
        if clipped is None:
            continue
        start = np.matmul(clip_matrix, line.start)
        end = np.matmul(clip_matrix, line.end)
        start /= start[3]
        end /= end[3]
        o.append(
            Line3D(Point3D(start[0], start[1], start[2]), Point3D(end[0], end[1], end[2]))
        )
    return o


def clip_to_screen(orig_o: List[Line3D], size):
    o = []
    screen_map_matrix = np.array([[size[0] / 2, 0, size[0] / 2], [0, -size[1] / 2, size[1] / 2], [0, 0, 1]])
    for line in orig_o:
        new_start_coords = np.matmul(screen_map_matrix, np.array([line.start.x, line.start.y, 1]))
        new_end_coords = np.matmul(screen_map_matrix, np.array([line.end.x, line.end.y, 1]))
        o.append(Line(Point(new_start_coords[0], new_start_coords[1]), Point(new_end_coords[0], new_end_coords[1])))
    return o


def draw(
    o: List[Line3D],
    pos: list = [0, 0, 0],
    rot: list = [0, 0, 0],
    scale: list = universal_scale,
    transformation_matrix=None,
):
    world_space = object_to_world(o, pos, rot, scale, transformation_matrix)
    camera_space = world_to_camera(world_space, cam_from, cam_at, cam_up)
    clipped = project_with_clipping(camera_space, far_plane, near_plane, zoom_x, zoom_y)
    return clip_to_screen(clipped, size)


# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")

# Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0, 0.0)
end = Point(0.0, 0.0)
house = load_house()
car = load_car()
tire = load_tire()
# obj = load_obj()

time_zero = pygame.time.get_ticks()

# Loop until the user clicks the close button.
while not done:
    # This limits the while loop to a max of 100 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(100)
    time_ = -(pygame.time.get_ticks() - time_zero) / 100.0

    # Clear the screen and set the screen background
    screen.fill(BLACK)

    # Controller Code#
    #####################################################################

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            done = True

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_q]:
        rot_y += cam_speed / math.pi
    if pressed[pygame.K_e]:
        rot_y -= cam_speed / math.pi

    ry = math.radians(rot_y)
    fwd = np.array([math.sin(ry), 0.0, math.cos(ry)])
    right = np.array([math.cos(ry), 0.0, -math.sin(ry)])

    if pressed[pygame.K_a]:
        mv_x += right[0] * cam_speed
        mv_z += right[2] * cam_speed
    if pressed[pygame.K_d]:
        mv_x -= right[0] * cam_speed
        mv_z -= right[2] * cam_speed
    if pressed[pygame.K_w]:
        mv_x += fwd[0] * cam_speed
        mv_z += fwd[2] * cam_speed
    if pressed[pygame.K_s]:
        mv_x -= fwd[0] * cam_speed
        mv_z -= fwd[2] * cam_speed

    if pressed[pygame.K_r]:
        mv_y += cam_speed
    if pressed[pygame.K_f]:
        mv_y -= cam_speed

    if pressed[pygame.K_h]:
        mv_x = 0
        mv_y = 0
        mv_z = 0
        rot_y = 0
        time_zero = pygame.time.get_ticks()

    cam_from = [mv_x, mv_y, mv_z]
    cam_at = np.array(cam_from) + fwd.tolist()
    cam_up = [0, 1, 0]
    far_plane = 1000
    near_plane = 0.1
    fov_y_deg = 60.0
    aspect_ratio = size[0] / size[1]
    focal_y = 1.0 / math.tan(math.radians(fov_y_deg) / 2.0)
    zoom_y = focal_y
    zoom_x = focal_y * aspect_ratio

    # Viewer Code#
    #####################################################################

    houses: List[Line] = []

    # 0, 1, 2, 3
    # 4, 0, 0, 0
    # 0, 5, 6, 7

    house1 = draw(house, [0, 0, 200], [0, 180, 0])
    houses.extend(house1)

    house2 = draw(house, [-150, 0, 200], [0, 180, 0])
    houses.extend(house2)

    house3 = draw(house, [-300, 0, 200], [0, 180, 0])
    houses.extend(house3)

    house4 = draw(house, [150, 0, 50], [0, -90, 0])
    houses.extend(house4)

    house5 = draw(house, [0, 0, -100])
    houses.extend(house5)

    house6 = draw(house, [-150, 0, -100])
    houses.extend(house6)

    house7 = draw(house, [-300, 0, -100])
    houses.extend(house7)

    for line in houses:
        pygame.draw.line(screen, RED, (line.start.x, line.start.y), (line.end.x, line.end.y))

    car_lines: List[Line] = []
    tire_lines: List[Line] = []

    tire_radius = 0.2
    car_trans = 2
    tire_rot = -car_trans / tire_radius

    # 1 0 2
    # 0 c 0
    # 3 0 4

    car_transformation_matrix = make_transformation_matrix([car_trans * time_, 0, 50])
    car1 = draw(car, transformation_matrix=car_transformation_matrix)
    car_lines.extend(car1)

    tire1_transformation_matrix = np.matmul(
        car_transformation_matrix, make_transformation_matrix([2.5, 0, 1.5], [0, 0, tire_rot * time_], [1, 1, 1])
    )
    tire1 = draw(tire, transformation_matrix=tire1_transformation_matrix)
    tire_lines.extend(tire1)

    tire2_transformation_matrix = np.matmul(
        car_transformation_matrix, make_transformation_matrix([-2.5, 0, 1.5], [0, 0, tire_rot * time_], [1, 1, 1])
    )
    tire2 = draw(tire, transformation_matrix=tire2_transformation_matrix)
    tire_lines.extend(tire2)

    tire3_transformation_matrix = np.matmul(
        car_transformation_matrix, make_transformation_matrix([2.5, 0, -1.5], [0, 0, tire_rot * time_], [1, 1, 1])
    )
    tire3 = draw(tire, transformation_matrix=tire3_transformation_matrix)
    tire_lines.extend(tire3)

    tire4_transformation_matrix = np.matmul(
        car_transformation_matrix, make_transformation_matrix([-2.5, 0, -1.5], [0, 0, tire_rot * time_], [1, 1, 1])
    )
    tire4 = draw(tire, transformation_matrix=tire4_transformation_matrix)
    tire_lines.extend(tire4)

    for line in car_lines:
        pygame.draw.line(screen, GREEN, (line.start.x, line.start.y), (line.end.x, line.end.y))
    for line in tire_lines:
        pygame.draw.line(screen, BLUE, (line.start.x, line.start.y), (line.end.x, line.end.y))

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
