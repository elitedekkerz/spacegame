#!/usr/bin/python3
import server
import gameObject
import logging
import numpy as np
import time

logging.basicConfig(level=logging.INFO)
s = server.server()
s.tickRate = 30
s.start()
#Create asteroids in 100 km radius 
for i in range(100):
    pos = (np.random.rand(3) - 0.5) * 100000
    newAsteroid = gameObject.gameObject("ast", pos)
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
s.stop()
