import math

class Quaternion:
    '''
    The class represents a quaternion and provides methods for quaternion operations.
    '''
    def __init__(self, w = None, v = None, angle = None, axis = None):
        '''
        Constructor for the Quaternion class.
        A quaternion can be initialized using either the w and v components or the angle and axis of rotation.
        '''
        if angle is not None and axis is not None:
            angle = math.radians(angle)
            self.w = math.cos(angle / 2)
            s = math.sin(angle / 2)
            self.v = (s * axis[0], s * axis[1], s * axis[2])
        elif w is not None and v is not None:
            self.w = w
            self.v = (v[0], v[1], v[2])
            
    def __str__(self):
        '''
        String representation of the quaternion.
        It is represented as w + xi + yj + zk.
        If any of the components are negative, that part is represented as -.
        '''
        return f"{self.w} {'+ ' if self.v[0] >= 0 else '- '}{abs(self.v[0])}i {'+ ' if self.v[1] >= 0 else '- '}{abs(self.v[1])}j {'+ ' if self.v[2] >= 0 else '- '}{abs(self.v[2])}k"

            
    def __add__(self, other):
        '''
        Overloaded + operator for quaternion addition.
        '''
        return Quaternion(self.w + other.w, (self.v[0] + other.v[0], self.v[1] + other.v[1], self.v[2] + other.v[2]))
    
    def __sub__(self, other):
        '''
        Overloaded - operator for quaternion subtraction.
        '''
        return Quaternion(self.w - other.w, (self.v[0] - other.v[0], self.v[1] - other.v[1], self.v[2] - other.v[2]))
    
    def __mul__(self, other):
        '''
        Overloaded * operator for multiplication with another quaternion or a scalar.
        '''
        if isinstance(other, Quaternion): # if other is a quaternion perform quaternion multiplication
            nw = self.w * other.w - self.v[0] * other.v[0] - self.v[1] * other.v[1] - self.v[2] * other.v[2]
            nx = self.w * other.v[0] + self.v[0] * other.w + self.v[1] * other.v[2] - self.v[2] * other.v[1]
            ny = self.w * other.v[1] + self.v[1] * other.w + self.v[2] * other.v[0] - self.v[0] * other.v[2]
            nz = self.w * other.v[2] + self.v[2] * other.w + self.v[0] * other.v[1] - self.v[1] * other.v[0]
            return Quaternion(nw, (nx, ny, nz))
        elif isinstance(other, (int, float)): # if other is a scalar perform scalar multiplication
            return Quaternion(self.w * other, tuple(v * other for v in self.v))
        else: # cant multiply with this type
            raise TypeError("Multiplication with type {} not supported".format(type(other)))
        
    def __rmul__(self, other):
        '''
        Overloaded * operator for multiplication with a scalar from the right.
        '''
        if isinstance(other, (int, float)):
            return self * other
        
    def __neg__(self):
        '''
        Overloaded negate operator for negation of the quaternion.
        '''
        return Quaternion(-self.w, tuple(-v for v in self.v))
        
    def __invert__(self):
        '''
        Overloaded ~ operator for inverse of the quaternion.
        '''
        mag = self.magnitude()
        conj = self.conjugate(self)
        return Quaternion(conj.w/ mag ** 2, tuple(v / mag ** 2 for v in conj.v))   
    
    def conjugate(self):
        '''
        Conjugate of the quaternion.
        '''
        return Quaternion(self.w, (-self.v[0], -self.v[1], -self.v[2]))
    
    def difference(self, other):
        '''
        Difference of two quaternions. 
        q1/q2 = q1 * ~q2.
        '''        
        return self * ~other

    def magnitude(self):
        '''
        Magnitude of the quaternion.
        '''
        return math.sqrt(self.w ** 2 + self.v[0] ** 2 + self.v[1] ** 2 + self.v[2] ** 2)
    
    def normalize(self):
        '''
        Normalizes the quaternion to have unit magnitude.
        '''
        mag = self.magnitude()
        return Quaternion(self.w / mag, (self.v[0] / mag, self.v[1] / mag, self.v[2] / mag))
    
    def dot(self, other):
        '''
        Dot product of two quaternions.
        Multiplies the corresponding components and sums them up.
        '''
        return self.w * other.w + self.v[0] * other.v[0] + self.v[1] * other.v[1] + self.v[2] * other.v[2]
    
    def transform(self, pt):
        '''
        Transforms a point using the quaternion.
        '''
        q = Quaternion(0, pt)
        return (self * q * ~self).v
    
    def slerp(self, other, t):
        '''
        Spherical linear interpolation between two quaternions.
        '''
        self = self.normalize() 
        other = other.normalize()
        
        dot = self.dot(other)
        
        if dot < 0: # if the dot product is negative, negate the other quaternion and the dot product
            other = -other
            dot = -dot
            
        if dot > 0.9995: # if the dot product is very close to 1, use linear interpolation
            return self + (other - self) * t
        
        theta = math.acos(dot)
        
        return self * (math.sin((1-t) * theta) / math.sin(theta)) + other * (math.sin(t * theta) / math.sin(theta))
    
    def toAngleAxis(self):
        '''
        Converts the quaternion to angle-axis representation.
        '''
        angle = math.degrees(2 * math.acos(self.w))
        s = math.sqrt(1 - self.w ** 2)
        if s < 0.001:
            return angle, (self.v[0], self.v[1], self.v[2])
        else:
            return angle, (self.v[0] / s, self.v[1] / s, self.v[2] / s)      