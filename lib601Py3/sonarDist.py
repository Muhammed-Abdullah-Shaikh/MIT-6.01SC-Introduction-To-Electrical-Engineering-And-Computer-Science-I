# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/sonarDist.py
"""
Useful constants and utilities for dealing with sonar readings in soar.
"""
import math
from . import util
sonarPoses = [util.Pose(0.08, 0.134, math.pi / 2),
 util.Pose(0.122, 0.118, 5 * math.pi / 18),
 util.Pose(0.156, 0.077, math.pi / 6),
 util.Pose(0.174, 0.0266, math.pi / 18),
 util.Pose(0.174, -0.0266, -math.pi / 18),
 util.Pose(0.156, -0.077, -math.pi / 6),
 util.Pose(0.122, -0.118, -5 * math.pi / 18),
 util.Pose(0.08, -0.134, -math.pi / 2)]
sonarMax = 1.5

def getDistanceRight(sonarValues):
    """
    @param sonarValues: list of 8 sonar readings
    @return: the perpendicular distance to a surface on the right of
    the robot, assuming there is a linear surface.
    """
    return getDistanceRightAndAngle(sonarValues)[0]


def getDistanceRightAndAngle(sonarValues):
    """
    @param sonarValues: list of 8 sonar readings
    @return: (d, a) where, d is the perpendicular distance to a
    surface on the right of the robot, assuming there is a linear
    surface;  and a is the angle to that surface.
    
    Change to use C{sonarHit}, or at least point and pose transforms.
    """
    hits = []
    for spose, d in zip(sonarPoses, sonarValues):
        if d < sonarMax:
            hits.append((spose.x + d * math.cos(spose.theta), spose.y + d * math.sin(spose.theta)))
        else:
            hits.append(None)

    return distAndAngle(hits[6], hits[7])


def sonarHit(distance, sonarPose, robotPose):
    """
    @param distance: distance along ray that the sonar hit something
    @param sonarPose: C{util.Pose} of the sonar on the robot
    @param robotPose: C{util.Pose} of the robot in the global frame
    @return: C{util.Point} representing position of the sonar hit in the
    global frame.  
    """
    return robotPose.transformPoint(sonarPose.transformPoint(util.Point(distance, 0)))


def distAndAngle(h0, h1):
    if h0 and h1:
        linex, liney, lined = line(h0, h1)
        return (abs(lined), math.pi / 2 - math.atan2(liney, linex))
    elif h0:
        hx, hy = h0
        return (math.sqrt(hx * hx + hy * hy), None)
    elif h1:
        hx, hy = h1
        return (math.sqrt(hx * hx + hy * hy), None)
    else:
        return (sonarMax, None)
        return None


def line(h0, h1):
    h0x, h0y = h0
    h1x, h1y = h1
    dx = h1x - h0x
    dy = h1y - h0y
    mag = math.sqrt(dx * dx + dy * dy)
    nx = dy / mag
    ny = -dx / mag
    d = nx * h0x + ny * h0y
    return (nx, ny, d)