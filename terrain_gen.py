import maya.cmds as cmds
import noise.diamondSquare as ds
import noise.simplex as simplex

reload(ds)
reload(simplex)

def simplexNoise(x, y, scale, mag, exp):
    return (simplex.raw_noise_2d(x/scale, y/scale) * mag)**exp

def sampleTerrain(x, y):
    #softNoise = heightMapSoft.sample(x, y)
    hardNoise = heightMapHard.sample(x, y)
    
    #noise = ds.cosineInterp(softNoise, hardNoise, 1)
    
    return (x, hardNoise, y)

width = 64
height = 64
resX = 32
resY = 32
featureSize = 64
scale = 8

updateStep = 12

try:
    cmds.delete('pPlane*')
except ValueError:
    pass

print "Generating heightmap..."    
pixelMapHard = ds.generate(resX, resY, 16, 2)

print "Interpolating heightmap..."

scaleX = width / float(resX)
scaleY = height / float(resY)
pixelMapHard.scaleNearestNeighbour(scaleX, scaleY)

heightMapHard = pixelMapHard.getInterpPixels(ds.linearInterp, 0,4 )

print scaleX, scaleY

#heightMapHard.scaleNearestNeighbour(scaleX, scaleY)

cmds.progressWindow(isInterruptable=True)

width = pixelMapHard.width
height = pixelMapHard.height


totalPixels = width * height
shouldUpdate = False

print "Generating terrain..."

planeName = cmds.polyPlane(w = width, h = height, sx = width, sy = height)[0]
cmds.polySoftEdge(planeName, a=0)

for y in xrange(0, height):
    for x in xrange(0, width):
        point = sampleTerrain(x, y)
        
        #name = cmds.polyCube(ch=False)[0]
        #cmds.move(point[0], point[1], point[2], name, ws=True)
        #cmds.move(-64, '%s.f[3]' % name, x=False, y=True, z=False, ws=True)
        
        i = x+(y*width)
        
        cmds.select('%s.f[%d]' % (planeName, i))
        cmds.move(0, point[1], 0, ws=True, r=True)

        progress = ((i)*(1.0/totalPixels))*100
        
        if(cmds.progressWindow(query=True, isCancelled=True)):
            cmds.delete('pPlane*')
            break
        else:
            cmds.progressWindow(progress = progress, edit=True)

    if(cmds.progressWindow(query=True, isCancelled=True)):
        break
    if(y % updateStep == 0):
        cmds.refresh()
        shouldUpdate = False
            
cmds.progressWindow(endProgress=True)
        