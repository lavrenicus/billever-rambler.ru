from math import sqrt
import numpy


class BadParametersException(Exception):
    pass


class Vector(list):
    def __init__(self, *args):
        super().__init__(*args)

    def __sub__(self, vec):
        if isinstance(vec, float) or isinstance(vec, int):
            vec = self._scalarToVector(vec)
        if len(self) != len(vec):
            raise BadParametersException('Vector dimensions mismatch')
        resultVector = [0] * len(self)
        for index, value in enumerate(self):
            resultVector[index] = self[index] - vec[index]
        return Vector(resultVector)

    def __add__(self, vec):
        if isinstance(vec, float) or isinstance(vec, int):
            vec = self._scalarToVector(vec)

        resultVector = [0] * len(self)
        for index, value in enumerate(self):
            resultVector[index] = self[index] + vec[index]
        return Vector(resultVector)

    def __mul__(self, n):
        resultVector = [0] * len(self)
        for index, value in enumerate(self):
            if isinstance(n, float):
                resultVector[index] = self[index] * n
            elif isinstance(n, int):
                resultVector[index] = self[index] * n
            elif isinstance(n, list):
                resultVector[index] = self[index] * n[index]

        return Vector(resultVector)

    def __repr__(self) -> str:
        return 'Vector:({})'.format(super().__repr__()[1:-1])

    def __truediv__(self, n):
        return Vector([index * (1/n) for index in self])

    def _scalarToVector(self, value):
        return Vector([value] * len(self))

    def dot(self, vec):
        """Return dot product of two vectors
        >>> Vector((1,3,-5)).dot(Vector((4,-2,-1)))
        3
        """
        summ = 0
        for index, value in enumerate(self):
            summ += self[index] * vec[index]
        return summ

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
        result = Vector([0] * self.__len__())
        lenght = self.length
        invLenght = 1/lenght

        for i, val in enumerate(self):
            result[i] = self[i] * invLenght
        return result

    def distance(self, vec):
        summ = 0
        for index, value in enumerate(self):
            dif = self[index] - vec[index]
            summ += dif * dif
        return sqrt(summ)

    @property
    def length(self):
        """ return scalar length of vector
        :return: float
        """
        summ = 0
        for value in self:
            summ += value * value
        return sqrt(summ)

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
        self[2] = value


class VectorNP(numpy.ndarray):
    def __new__(cls, *args, **kwargs):
        self = numpy.asarray(*args).view(cls)
        return self

    def noramlized(self):
        return self/self.length

    def distance(self, vec):
        if self.shape != vec.shape:
            raise BadParametersException('Vector dimensions mismatch')
        summ = 0
        for index, value in enumerate(self):
            dif = self[index] - vec[index]
            summ += dif * dif
        return numpy.sqrt(summ)

    @property
    def length(self):
        summ = 0
        for value in self:
            summ += value * value
        return numpy.sqrt(summ)

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
