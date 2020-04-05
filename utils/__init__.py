from typing import List
import objects


def rayMarch(
        camera: objects.Camera,
        camDirection: objects.Vector,
        scene: list,
        maxSteps=100,
        maxDistance=100,
        minDistance=.1
) -> float:
    dist = 0

    for i in range(maxSteps):
        curPoint = camera.position + camDirection * dist
        distSurf = getMinDistance(curPoint, scene)
        dist += distSurf
        if distSurf > maxDistance or distSurf < minDistance:
            break
    return dist


def getMinDistance(point: objects.Vector, scene: List[objects.Transform]) -> float:
    allDist = []
    for obj in scene:
        dist = obj.getDistanceFromPointToSurface(point)
        if dist >= 0:
            allDist.append(dist)
        else:
            allDist.append(0)

    return min(allDist)
