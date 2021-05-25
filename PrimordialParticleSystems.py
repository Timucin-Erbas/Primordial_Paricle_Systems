import math
import random
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------#
# Creating Particles and Visual                                                #
#------------------------------------------------------------------------------#
def createParticles(x, y, alpha, plane):
  plane.append([x, y, alpha])

def show(plane, iter):
  x = []
  y = []
  for i in plane:
    x.append(i[0])
    y.append(i[1])
  plt.scatter(x, y, s=1, c=(0,0,1), alpha=0.8)

  tag = ""
  for i in range(len(str(iter)), 7, 1):
    tag += "0";
  tag += str(iter)

  plt.show()
  
  #------------------------------------------------------------------------------#
# Trans-Particular Variable Derevations                                        #
#------------------------------------------------------------------------------#

def distance(x1, y1, x2, y2):
  square1 = (x1 - x2) * (x1 - x2)
  square2 = (y1 - y2) * (y1 - y2)
  return math.sqrt(square1 + square2)

def shortDistanceCoords(x1, y1, x2, y2, w, h):
  distances = []
  distances.append([distance(x1, y1, x2+w, y2+h), x2+w, y2+h])
  distances.append([distance(x1, y1, x2+w, y2), x2+w, y2])
  distances.append([distance(x1, y1, x2+w, y2-h), x2+w, y2-h])
  distances.append([distance(x1, y1, x2, y2+h), x2, y2+h])
  distances.append([distance(x1, y1, x2, y2), x2, y2])
  distances.append([distance(x1, y1, x2, y2-h), x2, y2-h])
  distances.append([distance(x1, y1, x2-w, y2+h), x2-w, y2+h])
  distances.append([distance(x1, y1, x2-w, y2), x2-w, y2])
  distances.append([distance(x1, y1, x2-w, y2-h), x2-w, y2-h])
  minimum = distances[0][0]
  index = 0
  for i in range(0, len(distances), 1):
    if(minimum > distances[i][0]):
      minimum = distances[i][0]
      index = i
  return [x1, y1, distances[index][1], distances[index][2]]

def relativeAngle(x1, y1, x2, y2):
  c = distance(x1, y1, x2, y2)
  if(c == 0.0):
    return 0
  a = abs(y1 - y2)
  quadrantAngle = math.asin(a/c) * 57.29577951308232087679815481410517033240547246
  if(x2 >= x1 and y2 >= y1):
    return quadrantAngle
  elif(x2 <= x1 and y2 >= y1):
    return 180 - quadrantAngle
  elif(x2 <= x1 and y2 <= y1):
    return 180 + quadrantAngle
  elif(x2 >= x1 and y2 <= y1):
    return 360 - quadrantAngle

def sign(num):
  if(num == 0):
    return 0
  elif(num < 0):
    return -1
  elif(num > 0):
    return 1

def changePositionX(angle, velocity):
  if(angle >= 90 and angle <= 270):
    return math.cos(angle%90/57.29577951308232087679815481410517033240547246) * velocity * -1
  else:
    return math.cos(angle%90/57.29577951308232087679815481410517033240547246) * velocity
  
  
def changePositionY(angle, velocity):
  if(angle >= 0 and angle <= 180):
    return math.sin(angle%90/57.29577951308232087679815481410517033240547246) * velocity
  else:
    return math.sin(angle%90/57.29577951308232087679815481410517033240547246) * velocity * -1
    
#------------------------------------------------------------------------------#
# Main Simulation Function                                                     #
#------------------------------------------------------------------------------#

particles = []
for i in range(0, 8, 1):
  createParticles(random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 360), particles)

history = []

for step in range(0, 100000, 1):
  show(particles, step)
  for particle in particles:
    history.append(particle.copy())
    R = 0
    L = 0
    for pair in particles:
      if(distance(particle[0], particle[1], pair[0], pair[1]) > 5):
        continue
      if(pair == particle):
        continue
      setPositions = shortDistanceCoords(particle[0], particle[1], pair[0], pair[1], 100, 100)
      primaryPoint = [setPositions[0], setPositions[1], particle[2]]
      secondaryPoint = [setPositions[2], setPositions[3], pair[2]]
      angle = relativeAngle(primaryPoint[0], primaryPoint[1], secondaryPoint[0], secondaryPoint[1])
      if(primaryPoint[2] < (primaryPoint[2] + 180)%360):
        if(angle > primaryPoint[2] and angle < (primaryPoint[2] + 180)%360):
          L += 1
        else:
          R += 1
      elif(primaryPoint[2] > (primaryPoint[2] + 180)%360):
        if(angle < primaryPoint[2] and angle > (primaryPoint[2] + 180)%360):
          R += 1
        else:
          L += 1
    changeAngle = 180 + 17 * (R + L) * sign(R-L)
    particle[2] = (particle[2] - changeAngle)%360
    particle[1] += changePositionY(particle[2], 0.67)
    particle[0] += changePositionX(particle[2], 0.67)
