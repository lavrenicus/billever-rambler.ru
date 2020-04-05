import math
import numpy
from typing import List


class BadParametersException(Exception):
    pass


class Vector(list):
    def __init__(self, *args):
        super().__init__(*args)

    def __sub__(self, vec):
        if len(self) != len(vec):
            raise BadParametersException('Vector dimensions mismatch')
        resultVector = []
        for index, value in enumerate(self):
            resultVector.append(self[index] - vec[index])
        return Vector(resultVector)

    def __add__(self, vec):
        if len(self) != len(vec):
            raise BadParametersException('Vector dimensions mismatch')
        resultVector = []
        for index, value in enumerate(self):
            resultVector.append(self[index] + vec[index])
        return Vector(resultVector)

    def __mul__(self, n):
        if isinstance(n, list) and len(self) != len(n):
            raise BadParametersException('Vector dimensions mismatch')
        resultVector = []
        for index, value in enumerate(self):
            if isinstance(n, float):
                resultVector.append(self[index] * n)
            elif isinstance(n, int):
                resultVector.append(self[index] * n)
            elif isinstance(n, list):
                resultVector.append(self[index] * n[index])

        return Vector(resultVector)

    def __repr__(self) -> str:
        return 'Vector:({})'.format(super().__repr__()[1:-1])

    def __truediv__(self, n):
        if isinstance(n, int) or isinstance(n, float):
            return Vector([index * (1/n) for index in self])
        elif isinstance(n, list):
            raise Exception('Vector div on vector not supported')

    def noramlized(self):
        result = Vector()
        for i, val in enumerate(self):
            result.append(self[i]/self.length)
        return result

    def distance(self, vec):
        if len(self) != len(vec):
            raise BadParametersException('Vector dimensions mismatch')
        summ = 0
        for index, value in enumerate(self):
            dif = self[index] - vec[index]
            summ += dif ** 2
        return math.sqrt(summ)

    @property
    def length(self):
        sum = 0
        for value in self:
            sum += value ** 2
        return math.sqrt(sum)

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


class PLane(Transform):
    def getDistanceFromPointToSurface(self, point: Vector):
        return point.y - self.position.y


class Sphere(Transform):
    radius = 0

    def __init__(self, position, radius):
        super().__init__(position)
        self.radius = radius

    def getDistanceFromPointToSurface(self, point: Vector):
        distance = point.distance(self.position) - self.radius
        return distance


class Camera(Transform):
    @property
    def direction(self):
        normPos = self.position.noramlized()
        normPos.z = 1
        return normPos
