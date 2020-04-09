import math
import numpy


class BadParametersException(Exception):
    pass


class Vector(object):
    _array = None

    def __init__(self, array):

        self._array = numpy.array(array)

    def __len__(self):
        return self._array.__len__()

    def __iter__(self):
        return self._array.__iter__()

    def __getitem__(self, item):
        return self._array.__getitem__(item)

    def __sub__(self, vec):
        return Vector(self._array - vec)

    def __add__(self, vec):
        return Vector(self._array + vec)

    def __mul__(self, n):
        return Vector(self._array * n)

    def __repr__(self) -> str:
        return 'Vector:({})'.format(self._array[1:-1])

    def __truediv__(self, n):
        if isinstance(n, int) or isinstance(n, float):
            return Vector([index * (1/n) for index in self])
        elif isinstance(n, list):
            raise Exception('Vector div on vector not supported')

    def __setitem__(self, key, value):
        self._array[key] = value

    def _scalarToVector(self, value):
        newVec = Vector(numpy.zeros(len(self)))
        for i in range(len(self)):
            newVec[i] = value
        return newVec

    def append(self, value):
        self._array = numpy.array([*self._array, value])

    def dot(self, vec):
        """Return dot product of two vectors
        >>> Vector((1,3,-5)).dot(Vector((4,-2,-1)))
        3
        """
        # if len(self) != len(vec):
        #     raise BadParametersException('Vector dimensions mismatch')
        # summ = 0
        # for index, value in enumerate(self):
        #     summ += self[index] * vec[index]

        return self._array.dot(vec)

    def noramlized(self):
        """return normalized vector
        :return: Vector
        >>> Vector((0,2,0)).noramlized()
        Vector:(0.0, 1.0, 0.0)
        >>> Vector((156,0,0)).noramlized()
        Vector:(1.0, 0.0, 0.0)
        >>> Vector((0,0,5432)).noramlized()
        Vector:(0.0, 0.0, 1.0)
        """
        result = Vector(numpy.zeros(len(self)))
        lenght = self.length
        invLenght = 1/lenght

        for i, val in enumerate(self):
            result[i] = self[i] * invLenght
        return result

    def distance(self, vec):
        if len(self) != len(vec):
            raise BadParametersException('Vector dimensions mismatch')
        summ = 0
        for index, value in enumerate(self):
            dif = self[index] - vec[index]
            summ += dif ** 2
        return numpy.sqrt(summ)

    @property
    def length(self):
        """ return scalar length of vector
        :return: float
        """
        sum = 0
        for value in self:
            sum += value ** 2
        return numpy.sqrt(sum)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @x.setter
    def x(self, value):
        self[0] = value

    @y.setter
    def y(self, value):
        self[1] = value

    @z.setter
    def z(self, value):
        self[1] = value


class VectorNP(numpy.ndarray):
    def __new__(cls, *args, **kwargs):
        self = numpy.asarray(*args).view(cls)
        return self

    def noramlized(self):
        return self/self.length

    def distance(self, vec):
        if self.shape != vec.shape:
            raise BadParametersException('Vector dimensions mismatch')
        sum = 0
        for index, value in enumerate(self):
            dif = self[index] - vec[index]
            sum += dif ** 2
        return numpy.sqrt(sum)

    @property
    def length(self):
        sum = 0
        for value in self:
            sum += value ** 2
        return numpy.sqrt(sum)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @x.setter
    def x(self, value):
        self[0] = value

    @y.setter
    def y(self, value):
        self[1] = value

    @z.setter
    def z(self, value):
        self[1] = value


class Transform(object):
    _position = None

    def __init__(self, position):
        if len(position) != 3:
            raise BadParametersException()
        self._position = Vector(position)

    def getDistanceFromPointToSurface(self, point):
        NotImplementedError()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = Vector(value)

    def getNormal(self, point):
        raise NotImplementedError()


class Plane(Transform):
    def getDistanceFromPointToSurface(self, point: Vector):
        return point.y - self.position.y

    def getNormal(self, point):
        return Vector((0, 1, 0)).noramlized()


class Sphere(Transform):
    radius = 0

    def __init__(self, position, radius):
        super().__init__(position)
        self.radius = radius

    def getDistanceFromPointToSurface(self, point: Vector):
        distance = self.position.distance(point) - self.radius
        return distance

    def getNormal(self, point):
        return (self.position - point).noramlized()


class Camera(Transform):
    pass
