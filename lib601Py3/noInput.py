# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/noInput.py
from . import sig
from . import simulate

def testSignal(simTime = 3.0):
    nsteps = int(simTime / simulate.Tsim)
    print(__name__, 'nsteps ', nsteps)
    return (nsteps, sig.ListSignal(nsteps * [{}]))


nsteps, sigIn = testSignal()

def runTest(lines, parent = None, nsteps = 70):
    simulate.runCircuit(lines, sigIn, parent, nsteps)