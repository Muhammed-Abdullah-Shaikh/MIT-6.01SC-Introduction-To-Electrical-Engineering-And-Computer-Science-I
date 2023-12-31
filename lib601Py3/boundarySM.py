# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/boundarySM.py
"""
Very simple behavior for following the boundary of an obstacle in the
world, with the robot's 'right hand' on the wall. 
"""
from . import sm
from soar.io import io
sideClearDist = 0.3
clearDist = 0.25
forwardSpeed = 0.25
rotationalSpeed = 0.25
stop = io.Action(0, 0)
go = io.Action(forwardSpeed, 0)
left = io.Action(0, rotationalSpeed)
right = io.Action(sideClearDist * rotationalSpeed, -rotationalSpeed)

def clearTest(selectedSensors, threshold):
    return min(selectedSensors) > threshold


def frontClear(sensors):
    return clearTest(frontSonars(sensors), clearDist)


def leftClear(sensors):
    return clearTest(leftSonars(sensors), sideClearDist)


def rightClear(sensors):
    return clearTest(rightSonars(sensors), sideClearDist)


def frontSonars(sensors):
    return sensors.sonars[2:6]


def front6Sonars(sensors):
    return sensors.sonars[1:7]


def leftSonars(sensors):
    return sensors.sonars[0:3]


def rightSonars(sensors):
    return sensors.sonars[5:8]


def rightmostSonar(sensors):
    return sensors.sonars[7:8]


def wallInFront(sensors):
    return not clearTest(front6Sonars(sensors), clearDist)


def wallOnRight(sensors):
    return not clearTest(rightmostSonar(sensors), sideClearDist)


def pickAction(state):
    if state == 'turningLeft':
        return left
    elif state == 'turningRight':
        return right
    elif state == 'stop':
        return stop
    else:
        return go


class BoundaryFollowerSM4(sm.SM):
    """State machine with instances of C{io.SensorInput} as input and
    C{io.Action} as output.  Follows a boundary with the robot's
    'right hand' on the wall.  Has four internal states:
    'turningLeft', 'turningRight', 'movingForward', and 'following'
    """
    startState = 'movingForward'

    def getNextValues(self, state, inp):
        if state == 'turningLeft':
            if wallInFront(inp):
                nextState = 'turningLeft'
            elif wallOnRight(inp):
                nextState = 'following'
            else:
                nextState = 'turningLeft'
        elif state == 'turningRight':
            if wallOnRight(inp):
                nextState = 'following'
            else:
                nextState = 'turningRight'
        elif state == 'movingForward':
            if wallInFront(inp):
                nextState = 'turningLeft'
            else:
                nextState = 'movingForward'
        elif wallInFront(inp):
            nextState = 'turningLeft'
        elif wallOnRight(inp):
            nextState = 'following'
        else:
            nextState = 'turningRight'
        return (nextState, pickAction(nextState))


class BoundaryFollowerSM2(sm.SM):
    """State machine with instances of C{io.SensorInput} as input and
    C{io.Action} as output.  Follows a boundary with the robot's
    'right hand' on the wall.  Has two internal states:  'seek' and
    'following'. 
    """
    startState = 'seek'

    def getNextValues(self, state, inp):
        if state == 'seek':
            if wallInFront(inp):
                return ('following', left)
            elif wallOnRight(inp):
                return ('following', go)
            else:
                return ('seek', go)
        else:
            if wallInFront(inp):
                return ('following', left)
            if wallOnRight(inp):
                return ('following', go)
            return ('following', right)