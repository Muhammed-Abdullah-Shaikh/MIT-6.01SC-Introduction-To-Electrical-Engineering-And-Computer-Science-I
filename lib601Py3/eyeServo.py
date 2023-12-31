# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/eyeServo.py
import math
from . import sig
from . import simulate

def testSignal(dist = 1.0, simTime = 3.0):
    nsteps = int(simTime / simulate.Tsim)
    print(__name__, 'nsteps ', nsteps)
    ninter = nsteps / 4
    return (nsteps, sig.ListSignal(ninter * [{'lightAngle': 1.57,
       'lightDist': dist}] + ninter * [{'lightAngle': 3.14,
       'lightDist': dist}] + ninter * [{'lightAngle': 1.57,
       'lightDist': dist}] + ninter * [{'lightAngle': 3.14,
       'lightDist': dist}]))


nsteps, sigIn = testSignal(dist=1.0)

def runTest(lines, parent = None, nsteps = nsteps):
    simulate.runCircuit(lines, sigIn, parent, nsteps)


def simpleSignal(dist = 1.0, simTime = 3.0):
    nsteps = int(simTime / simulate.Tsim)
    return (nsteps, sig.ListSignal(nsteps * [{'lightAngle': 1.57,
       'lightDist': dist}]))


def simpleSignal2(dist = 1.0, simTime = 3.0):
    nsteps = int(simTime / simulate.Tsim)
    return (nsteps, sig.ListSignal(nsteps * [{'lightAngle': 3 * math.pi / 4,
       'lightDist': dist}]))