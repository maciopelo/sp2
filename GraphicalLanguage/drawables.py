import pygame
from vpython import *
from math import sin, cos, radians

class Drawable:
    def draw(self, screen):
        pass

    def fill(self, color):
        self.color = color
    
    def move(self, x, y):
        pass
    
    def place(self, point):
        pass
    
    def rotate(self, point, angle):
        pass
    
    def scale(self, point, factor):
        pass

    def scale3d(self,factor):
        pass


    def normalize_rgb(self, color):
        return (color[0]/255,color[1]/255,color[2]/255)

    def rotate_single_point(self, point, pivot, angle):
        s = sin(radians(angle))
        c = cos(radians(angle))

        origin_x = point.x - pivot.x
        origin_y = point.y - pivot.y

        new_x = origin_x * c - origin_y * s
        new_y = origin_x * s + origin_y * c

        return new_x + pivot.x, new_y + pivot.y

    def scale_single_point(self, point, pivot, factor):
        vector_x = factor * (point.x - pivot.x)
        vector_y = factor * (point.y - pivot.y)

        return pivot.x + vector_x, pivot.y + vector_y


class Group(Drawable):
    def __init__(self, name, type_, members):
        self.name = name
        self.type = type_   
        self.members = members
    
    def __str__(self):
        ret = f'group<{self.type}>, {self.name}, [\n'
        for m in self.members:
            ret += '  ' + str(m) + ','
        return ret[:-2] + f'\n]'

    def draw(self, screen):
        for m in self.members:
            m.draw(screen)

    def fill(self, color):
        for m in self.members:
            m.fill(color)
    
    def move(self, x, y):
        for m in self.members:
            m.move(x, y)
    
    def place(self, point):
        for m in self.members:
            m.place(point)
    
    def rotate(self, point, angle):
        for m in self.members:
            m.rotate(point, angle)
    
    def scale(self, point, factor):
        for m in self.members:
            m.scale(point, factor)
        

class Point(Drawable):
    POINT_RADIUS = 3

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.color = (0, 0, 0)

    def get_coordination_tuple(self):
        return self.x, self.y

    def __str__(self):
        return f'<point, {self.name}, ({self.x}, {self.y}), #{self.color}>'

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.POINT_RADIUS)
    
    def move(self, x, y):
        self.x += x
        self.y += y
    
    def place(self, point):
        x = point.x - self.x
        y = point.y - self.y

        self.x += x
        self.y += y
    
    def rotate(self, point, angle):
        x, y = self.rotate_single_point(self, point, angle)

        self.x = x
        self.y = y
    
    def scale(self, point, factor):
        x, y = self.scale_single_point(self, point, factor)

        self.x = x
        self.y = y


class Segment(Drawable):
    SEGMENT_WIDTH = 1

    def __init__(self, name, start_point, end_point):
        self.name = name
        self.start_point = start_point
        self.end_point = end_point
        self.color = (0, 0, 0)
        self.width = self.SEGMENT_WIDTH
    
    def __str__(self):
        return f'<segment, {self.name}, {self.start_point}, {self.end_point}, #{self.color}>'

    def draw(self, screen):
        start_point = self.start_point.get_coordination_tuple()
        end_point = self.end_point.get_coordination_tuple()
        pygame.draw.line(screen, self.color, start_point, end_point, self.width)
 
    def move(self, x, y):
        self.start_point.x += x
        self.start_point.y += y
        self.end_point.x += x
        self.end_point.y += y
    
    def place(self, point):
        x = point.x - self.start_point.x
        y = point.y - self.start_point.y

        self.start_point.x += x
        self.start_point.y += y

        self.end_point.x += x
        self.end_point.y += y
    
    def rotate(self, point, angle):
        start_x, start_y = self.rotate_single_point(self.start_point, point, angle)
        end_x, end_y = self.rotate_single_point(self.end_point, point, angle)

        self.start_point.x = start_x
        self.start_point.y = start_y
        self.end_point.x = end_x
        self.end_point.y = end_y
    
    def scale(self, point, factor):
        start_x, start_y = self.scale_single_point(self.start_point, point, factor)
        end_x, end_y = self.scale_single_point(self.end_point, point, factor)

        self.start_point.x = start_x
        self.start_point.y = start_y
        self.end_point.x = end_x
        self.end_point.y = end_y


class Circle(Drawable):
    CIRCLE_WIDTH = 1

    def __init__(self, name, center_point, radius):
        self.name = name
        self.center_point = center_point
        self.radius = radius
        self.color = (0, 0, 0)
        self.width = self.CIRCLE_WIDTH

    def __str__(self):
        return f'<circle, {self.name}, {self.center_point}, {self.radius}, #{self.color}>'

    def draw(self, screen):
        center_point = self.center_point.get_coordination_tuple()
        pygame.draw.circle(screen, self.color, center_point, self.radius)
  
    def move(self, x, y):
        self.center_point.x += x
        self.center_point.y += y
    
    def place(self, point):
        x = point.x - self.center_point.x
        y = point.y - self.center_point.y

        self.center_point.x += x
        self.center_point.y += y
    
    def rotate(self, point, angle):
        x, y = self.rotate_single_point(self.center_point, point, angle)

        self.center_point.x = x
        self.center_point.y = y
    
    def scale(self, point, factor):
        x, y = self.scale_single_point(self.center_point, point, factor)

        self.center_point.x = x
        self.center_point.y = y
        self.radius *= abs(factor)


class Polygon(Drawable):
    POLYGON_WIDTH = 0

    def __init__(self, name, points):
        self.name = name
        self.points = points
        self.color = (0, 0, 0)
        self.width = self.POLYGON_WIDTH

    def __str__(self):
        ret = f'<polygon, {self.name}, ['
        for p in self.points:
            ret += str(p) + ', '
        return ret[:-2] + f'], #{self.color}>'

    def draw(self, screen):
        coordination_tuples_list = [point.get_coordination_tuple() for point in self.points]
        pygame.draw.polygon(screen, self.color, coordination_tuples_list, self.width)

    def move(self, x, y):
        for i in range(len(self.points)):
            self.points[i].x += x
            self.points[i].y += y
    
    def place(self, point):
        x = point.x - self.points[0].x
        y = point.y - self.points[0].y

        for i in range(len(self.points)):
            self.points[i].x += x
            self.points[i].y += y
    
    def rotate(self, point, angle):
        for i in range(len(self.points)):
            x, y = self.rotate_single_point(self.points[i], point, angle)

            self.points[i].x = x
            self.points[i].y = y
    
    def scale(self, point, factor):
        for i in range(len(self.points)):
            x, y = self.scale_single_point(self.points[i], point, factor)

            self.points[i].x = x
            self.points[i].y = y
    

class Vector(Drawable):

    def __init__(self, name, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.color = vec(1, 1, 1)
        self.obj = None
        self.radius = 0.5

    def get_coordination_tuple(self):
        return self.x, self.y, self.z

    def fill(self, color):
        self.color = vec(*self.normalize_rgb(color))

    def __str__(self):
        return f'vector, {self.name}, ({self.x}, {self.y}, {self.z}), #{self.color}'

    def draw(self, screen):
        self.obj = sphere(radius=self.radius, pos=vec(self.x, self.y, self.z), canvas=screen, color=self.color)
    
    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z
    
    def place(self, point):
        self.x = point.x
        self.y = point.y
        self.z = point.z
    
    def rotate(self, axis, angle):
        init = axis.get_axis_initial_vec()
        term = axis.get_axis_terminal_vec()
        axis = (term[0]-init[0],term[1]-init[1],term[2]-init[2])
        self.obj.rotate(angle=radians(angle), origin=vec(*init), axis=vector(*axis))
    
    def scale3d(self, factor):
        self.radius *= factor


class Box(Drawable):
    def __init__(self, name, position, size, screen):
        self.position = position
        self.size = size
        self.name = name
        self.color = vec(1, 1, 1)
        self.screen = screen
        self.obj = None
        self.update_shape()

    def update_shape(self):
        self.obj = box(pos = vec(*self.get_coordination_tuple()), size = vec(*self.get_size_tuple()), canvas=self.screen, color=self.color, visible=False)

    def get_coordination_tuple(self):
        return self.position.x, self.position.y, self.position.z
    
    def fill(self, color):
        self.color = vec(*self.normalize_rgb(color))
        self.update_shape()
    
    def get_size_tuple(self):
        return self.size.x, self.size.y, self.size.z

    def __str__(self):
        return f'box, {self.name}, [({self.position.x}, {self.position.y}, {self.position.z}),({self.size.x},{self.size.y}, {self.size.z})], #{self.color}'

    def draw(self, screen):
        copy = self.obj.clone()
        copy.visible = True


    def move(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z
        self.update_shape()
    
    def place(self, point):
        self.position.x = point.x
        self.position.y = point.y
        self.position.z = point.z
        self.update_shape()
    
    def rotate(self, axis, angle):
        init = axis.get_axis_initial_vec()
        term = axis.get_axis_terminal_vec()
        axis = (term[0]-init[0],term[1]-init[1],term[2]-init[2])
        self.obj.rotate(angle=radians(angle), origin=vec(*init), axis=vector(*axis))
    
    def scale3d(self, factor):
        self.size.x *= factor
        self.size.y *= factor
        self.size.z *= factor
        self.update_shape()



class Sphere(Drawable):
    def __init__(self,name, position, radius):
        self.position = position
        self.radius = radius
        self.name = name
        self.color = vec(1, 1, 1)
        self.obj = None

    def get_coordination_tuple(self):
        return self.position.x, self.position.y, self.position.z
    
    def get_radius(self):
        return self.radius
    
    def fill(self, color):
        self.color = vec(*self.normalize_rgb(color))

    def __str__(self):
        return f'sphere, {self.name}, ({self.position.x}, {self.position.y}, {self.position.z}),{self.radius}, #{self.color}'

    def draw(self, screen):
        self.obj = sphere(radius=self.radius, pos=vec(*self.get_coordination_tuple()), canvas=screen, color=self.color)
        

    def move(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z
    
    def place(self, point):
        self.x = point.x
        self.y = point.y
        self.z = point.z
    
    def rotate(self, axis, angle):
        init = axis.get_axis_initial_vec()
        term = axis.get_axis_terminal_vec()
        axis = (term[0]-init[0],term[1]-init[1],term[2]-init[2])
        self.obj.rotate(angle=radians(angle), origin=vec(*init), axis=vector(*axis))
    
    def scale3d(self, factor):
        self.radius *= factor



class Pyramid(Drawable):
    def __init__(self,name, position, size):
        self.position = position
        self.size = size
        self.name = name
        self.color = vec(1, 1, 1)
        self.obj = None

    def get_coordination_tuple(self):
        return self.position.x, self.position.y, self.position.z

    
    def fill(self, color):
        self.color = vec(*self.normalize_rgb(color))
    
    def get_size_tuple(self):
        return self.size.x, self.size.y, self.size.z

    def __str__(self):
        return f'pyramid, {self.name}, [({self.position.x}, {self.position.y}, {self.position.z}),({self.size.x},{self.size.y}, {self.size.z})], #{self.color}'

    def draw(self,screen):
        self.obj = pyramid(pos = vec(*self.get_coordination_tuple()), size = vec(*self.get_size_tuple()), canvas=screen, color=self.color)


    def move(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z
    
    def place(self, point):
        self.x = point.x
        self.y = point.y
        self.z = point.z
    
    def rotate(self, axis, angle):
        init = axis.get_axis_initial_vec()
        term = axis.get_axis_terminal_vec()
        axis = (term[0]-init[0],term[1]-init[1],term[2]-init[2])
        self.obj.rotate(angle=radians(angle), origin=vec(*init), axis=vector(*axis))
    
    def scale3d(self, factor):
        self.size.x *= factor
        self.size.y *= factor
        self.size.z *= factor




class Curve(Drawable):
    CURVE_WIDTH = 1
    
    def __init__(self, name, vectors):
        self.name = name
        self.vectors = vectors
        self.color = vec(1, 1, 1)
        self.width = self.CURVE_WIDTH
        self.obj = None

    def __str__(self):
        ret = f'curve, {self.name}, ['
        for p in self.vectors:
            ret += str(p) + ', '
        return ret[:-2] + f'], #{self.color}'

    def draw(self, screen):
        coordination_tuples_list = [vec(*vector.get_coordination_tuple()) for vector in self.vectors]
        self.obj = curve(coordination_tuples_list, color=self.color)
    
    def fill(self, color):
        self.color = vec(*self.normalize_rgb(color))

    def move(self, x, y, z):
        for v in self.vectors:
            v.x += x
            v.y += y
            v.z += z
    
    def place(self, point):
        for v in self.vectors:
            v.x += point.x
            v.y += point.y
            v.z += point.z

    def rotate(self, axis, angle):
        init = axis.get_axis_initial_vec()
        term = axis.get_axis_terminal_vec()
        axis = (term[0]-init[0],term[1]-init[1],term[2]-init[2])
        self.obj.rotate(angle=radians(angle), origin=vec(*init), axis=vector(*axis))
    
    def scale3d(self, factor):
        self.width *= factor




class Axis(Drawable):

    def __init__(self, name, inital_vec, terminal_vec, screen):
        self.name = name
        self.inital_vec = inital_vec
        self.terminal_vec = terminal_vec
        self.color = vec(1, 1, 1)
        self.screen = screen
        self.obj = None
        self.update_shape()

    def get_axis_length(self):
        return sqrt(
            (self.inital_vec.x - self.terminal_vec.x)**2 + 
            (self.inital_vec.y - self.terminal_vec.y)**2 + 
            (self.inital_vec.z - self.terminal_vec.z)**2
        )

    def get_axis_initial_vec(self):
        return self.inital_vec.x,self.inital_vec.y,self.inital_vec.z
    
    def get_axis_terminal_vec(self):
        return self.terminal_vec.x,self.terminal_vec.y,self.terminal_vec.z
    
    def fill(self, color):
        self.color = vec(*self.normalize_rgb(color))

    def __str__(self):
        return f'axis, {self.name}, ({self.inital_vec}, {self.terminal_vec}), length: {round(self.get_axis_length(),2)}, #{self.color}'

    def draw(self, screen):
        # copy = self.obj.clone()
        # copy.visible = True
        curve(pos=[vec(self.inital_vec.x,self.inital_vec.y,self.inital_vec.z), 
                vec(self.terminal_vec.x,self.terminal_vec.y,self.terminal_vec.z)], 
            canvas=self.screen, color=self.color)

    def update_shape(self):
        self.obj = curve(pos=[vec(self.inital_vec.x,self.inital_vec.y,self.inital_vec.z), 
                vec(self.terminal_vec.x,self.terminal_vec.y,self.terminal_vec.z)], 
            canvas=self.screen, color=self.color, visible=False)
    
    def move(self, x, y, z):
        a = self.inital_vec.x
        self.inital_vec.x += x
        self.inital_vec.y += y
        self.inital_vec.z += z

        self.terminal_vec.x += x
        self.terminal_vec.y += y
        self.terminal_vec.z += z
        
        self.update_shape()
    
    def place(self, point):
        self.inital_vec.x = point.x
        self.inital_vec.y = point.y
        self.inital_vec.z = point.z

        self.terminal_vec.x = point.x
        self.terminal_vec.y = point.y
        self.terminal_vec.z = point.z
        
        self.update_shape()
    
    def rotate(self, axis, angle):
        init = axis.get_axis_initial_vec()
        term = axis.get_axis_terminal_vec()
        axis = (term[0]-init[0],term[1]-init[1],term[2]-init[2])
        self.obj.rotate(angle=radians(angle), origin=vec(*init), axis=vector(*axis))
    
    def scale3d(self, factor):
        self.terminal_vec.x *= factor
        self.terminal_vec.y *= factor
        self.terminal_vec.z *= factor
        self.update_shape()




class Cylinder(Drawable):

    def __init__(self, name, inital_vec, terminal_vec, radius,screen):
        self.name = name
        self.inital_vec = inital_vec
        self.terminal_vec = terminal_vec
        self.radius = radius
        self.color = vec(1, 1, 1)
        self.screen = screen
        self.obj = None
        self.update_shape()

    def update_shape(self):
        self.obj = cylinder(radius=self.radius,
                pos=vec(self.inital_vec.x,self.inital_vec.y,self.inital_vec.z), 
                axis=vec(self.terminal_vec.x,self.terminal_vec.y,self.terminal_vec.z), 
                color=self.color, canvas=self.screen, visible=False)

    def __str__(self):
        return f'<axis, {self.name}, ({self.inital_vec}, {self.terminal_vec}), #{self.color}>'
    

    def fill(self, color):
        self.color = vec(*self.normalize_rgb(color))
        self.update_shape()

    def draw(self, screen):
        copy = self.obj.clone()
        copy.visible = True
    
    def move(self, x, y, z):
        self.inital_vec.x += x
        self.inital_vec.y += y
        self.inital_vec.z += z

        # self.terminal_vec.x += x
        # self.terminal_vec.y += y
        # self.terminal_vec.z += z

        self.update_shape()

    
    def place(self, point):
        self.inital_vec.x = point.x
        self.inital_vec.y = point.y
        self.inital_vec.z = point.z

        # self.terminal_vec.x = point.x
        # self.terminal_vec.y = point.y
        # self.terminal_vec.z = point.z
        
        self.update_shape()

    
    def rotate(self, axis, angle):
        init = axis.get_axis_initial_vec()
        term = axis.get_axis_terminal_vec()
        axis = (term[0]-init[0],term[1]-init[1],term[2]-init[2])
        self.obj.rotate(angle=radians(angle), origin=vec(*init), axis=vector(*axis))

    
    def scale3d(self, factor):
        self.radius *= factor
        
        self.update_shape()


class Ring(Drawable):

    def __init__(self, name, inital_vec, terminal_vec, radius, thickness):
        self.name = name
        self.inital_vec = inital_vec
        self.terminal_vec = terminal_vec
        self.radius = radius
        self.thickness = thickness
        self.color = vec(1, 1, 1)
        self.obj = None

    def __str__(self):
        return f'ring, {self.name}, ({self.inital_vec}, {self.terminal_vec}), r={self.radius}, thickness={self.thickness}, #{self.color}'

    def fill(self, color):
        self.color = vec(*self.normalize_rgb(color))

    def draw(self, screen):

        self.obj = ring(radius=self.radius,
            thickness=self.thickness,
            pos=vec(self.inital_vec.x,self.inital_vec.y,self.inital_vec.z), 
            axis=vec(self.terminal_vec.x,self.terminal_vec.y,self.terminal_vec.z), 
            canvas=screen, color=self.color)
    
    def move(self, x, y, z):
        self.inital_vec.x += x
        self.inital_vec.y += y
        self.inital_vec.z += z

        self.terminal_vec.x += x
        self.terminal_vec.y += y
        self.terminal_vec.z += z
    
    def place(self, point):
        self.inital_vec.x = point.x
        self.inital_vec.y = point.y
        self.inital_vec.z = point.z

        self.terminal_vec.x = point.x
        self.terminal_vec.y = point.y
        self.terminal_vec.z = point.z
    
    def rotate(self, axis, angle):
        init = axis.get_axis_initial_vec()
        term = axis.get_axis_terminal_vec()
        axis = (term[0]-init[0],term[1]-init[1],term[2]-init[2])
        self.obj.rotate(angle=radians(angle), origin=vec(*init), axis=vector(*axis))
    
    def scale3d(self, factor):
        self.radius *= factor
        self.thickness *= factor
    
