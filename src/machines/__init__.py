#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      said
#
# Created:     23.06.2012
# Copyright:   (c) said 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env
import sys
print (sys.path)
from machines.exceptions import *
import machines.Machine as Machine
import machines.ThreeAddressMachine as ThreeAddressMachine
import machines.AccuMachine as AccuMachine
import machines.StackMachine as StackMachine
import machines.TwoAddressMachine as TwoAddressMachine
import machines.Loader as Loader