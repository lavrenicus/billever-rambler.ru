from typing import List
import objects


def rayMarch(
        point: objects.Vector,
        camDirection: objects.Vector,
        scene: list,
        maxSteps=100,
        maxDistance=255,
        minDistance=.1
) -> float:
    dist = 0

    for i in range(maxSteps):
        curPoint = point + camDirection * dist
        distSurf = getDistance(curPoint, scene)
        dist += distSurf
        if dist > maxDistance or distSurf < minDistance:
            break
    return dist


def clamp(x, a, b):
    return max(a, min(b, x))


def getDistance(point: objects.Vector, scene: List[objects.Transform]) -> float:
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
        allDist.append(dist)
    return min(allDist)
