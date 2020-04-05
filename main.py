import os
import tempfile
import time
import sys
from asyncore import dispatcher

import numpy
import pygame
from pygame import gfxdraw

from PIL import Image, ImageDraw

import objects
import utils

HEIGHT = 480
WIDTH = 640

sphere = objects.Sphere(position=(0, 0, 20), radius=4)
sphere2 = objects.Sphere(position=(3, 0, 10), radius=3)
plane = objects.Plane(position=(0, -40, 0))
cam = objects.Camera(position=(0, 1, -10))

filePath = tempfile.mktemp(suffix='.jpg')
if not os.path.isfile(filePath):
    img = Image.new('RGB', (WIDTH, HEIGHT), color='white')
    print(filePath)
    point = cam.position
    scene = [sphere, sphere2, plane]

    pygame.init()
    surf = pygame.display.set_mode((WIDTH, HEIGHT))
    resolution = objects.Vector((WIDTH, HEIGHT))
    while 1:
        start = time.time()

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                fragCoord = objects.Vector((x, y))
                uv = (fragCoord - (resolution * 0.5))/HEIGHT
                camDirection = objects.Vector((uv.x, uv.y, 1)).noramlized()

                distance = utils.rayMarch(point=cam.position, scene=scene, camDirection=camDirection)
                point = cam.position + camDirection
                # light = utils.getNormal(point, scene)
                distance = utils.clamp(distance, 0, 255)
                # distance = 255 - distance
                # distance = max(0, (distance - 244) * 100)
                # light = (light + 1)/2
                sys.stdout.write(str(distance) + '\n')
                gfxdraw.pixel(surf, x, y, (int(distance), int(distance), int(distance)))
                img.putpixel((x, y), (int(distance), int(distance), int(distance)))

            pygame.display.update()
            pygame.event.pump()
        print(time.time() - start)
        img.save(filePath)
        break

os.system("start " + filePath)
