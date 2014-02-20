#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      said
#
# Created:     23.06.2012
# Copyright:   (c) afranck64 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from machines import *

def getMachine(text='', file=None, **kw):
    if file:
        with open(file) as f:
            text = f.read()
    ens = text.split("\n", 1)
    line = ens[0]
    typ = line.split()[0].upper()
    if typ == "MACHINE0":
        machine = StackMachine.StackMachine(**kw)
    elif typ == "MACHINE1":
        machine = AccuMachine.AccuMachine(**kw)
    elif typ == "MACHINE2":
        machine = TwoAddressMachine.TwoAddressMachine(**kw)
    elif typ == "MACHINE3":
        machine = ThreeAddressMachine.ThreeAddressMachine(**kw)
    else:
        raise Machine.MachineException("Unknown machine", found=typ,
                                    line=line + "- at lineNr. 1")
    machine.parse(ens[1])
    print (machine.output)
    return machine

if __name__ == "__main__":
    m = getMachine('machine0\n"output fuck you"')
    m.loop()