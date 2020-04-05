import os
import tempfile
import time
import numpy

from PIL import Image, ImageDraw

import objects
import utils

HEIGHT = 480
WIDTH = 640

sphere = objects.Sphere(position=(0, 10, 6), radius=0.1)
plane = objects.PLane(position=(0, -10, 0))
cam = objects.Camera(position=(0, 1, 0))

filePath = tempfile.mktemp(suffix='.jpg')
if not os.path.isfile(filePath):
    img = Image.new('RGB', (WIDTH, HEIGHT), color='white')
    print(filePath)
    start = time.time()
    point = cam.position
    scene = [sphere, plane]
    camDirection = cam.direction

    resolution = objects.Vector((WIDTH, HEIGHT))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            fragCoord = objects.Vector((x, y))
            uv = (fragCoord - (resolution * 0.5))#/HEIGHT
            camDirection.x = uv.x
            camDirection.y = uv.y

            distance = utils.rayMarch(camera=cam, scene=scene, camDirection=camDirection)
            distance /= 6
            img.putpixel((x, y), (int(distance), int(distance), int(distance)))
    print(time.time() - start)
    img.save(filePath)

os.system("start " + filePath)
