from typing import List
import objects
import math
import time
import sys


def profileTimer(fn):
    def inner(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        timeLeft = time.time() - start
        if timeLeft:
            sys.stdout.write(str(fn) + str(time.time() - start) + '\n')
        return result
    return inner


def rayMarch(
        point: objects.Vector,
        camDirection: objects.Vector,
        scene: list,
        maxSteps=100,
        maxDistance=255,
        minDistance=.1
) -> (float, objects.Vector):
    dist = 0

    for i in range(maxSteps):
        curPoint = point + camDirection * dist
        distSurf, normal = getDistance(curPoint, scene)  # type (float, objects.Transform())
        dist += distSurf
        if dist > maxDistance or distSurf < minDistance:
            break
    return dist, normal


def clamp(x, a, b):
    return max(a, min(b, x))


def getDistance(point: objects.Vector, scene: List[objects.Transform]) -> tuple:
    """ Calculate distance from all objects ещ point from scene and return that distance
    :param point: objects.Vector
    :param scene: list
    :return:
    >>> getDistance(objects.Vector((0, 0, 0)), [objects.Sphere((0,1,0), 1), objects.Plane((0, -40, 0))])
    0.7320508075688772
    """
    allDist = []
    for obj in scene:
        dist = obj.getDistanceFromPointToSurface(point)
        normal = obj.getNormal(point)
        allDist.append((dist, normal))
    allDist.sort(key=lambda x: x[0])
    return allDist[0]
