import sys
import time
from typing import List

from objects import Vector, Sphere, Transform, Plane


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
        point: Vector,
        camDirection: Vector,
        scene: list,
        maxSteps=100,
        maxDistance=255,
        minDistance=.1
) -> (float, Vector):
    dist = 0
    normal = 0
    for i in range(maxSteps):
        curPoint = point + camDirection * dist
        distSurf, normal = getDistance(curPoint, scene)  # type (float, Transform())
        dist += distSurf
        if dist > maxDistance or distSurf < minDistance:
            break
    return dist, normal


def clamp(x, a, b):
    return max(a, min(b, x))


def calculate_time(seconds):
    """Return formatted string of time
    :param seconds:
    :return: formatted time
    """
    seconds = int(seconds)

    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60

    if hours:
        result_str = f'{hours}h : {minutes}m : {seconds}s'
    elif minutes:
        result_str = f'{minutes}m : {seconds}s'
    else:
        result_str = f'{seconds}s'

    return result_str


def getDistance(point, scene: List[Transform]) -> tuple:
    """ Calculate distance from all objects ещ point from scene and return that distance
    :param point: Vector
    :param scene: list
    :return:
    >>> getDistance(Vector((0, 0, 0)), [Sphere((0,1,0), 1), Plane((0, -40, 0))])
    0.7320508075688772
    """
    allDist = {}
    for obj in scene:
        dist = obj.getDistanceFromPointToSurface(point)
        normal = obj.getNormal(point)
        allDist[dist] = normal
    minimal = min(allDist.keys())
    return minimal, allDist[minimal]
