#!/usr/bin/python3 -i
import server
import gameObject
import logging
import numpy as np
import time
import atexit

logging.basicConfig(level=logging.INFO)
s = server.server()
s.tickRate = 30
s.start()
#Create asteroids in 100 km radius 
for i in range(100):
    pos = (np.random.rand(3) - 0.5) * 100000
    newAsteroid = gameObject.gameObject("ast", pos)

#stop server before quitting
atexit.register(s.stop)

print('ready!')
