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
#!/usr/bin/env python


from Machine import *

class AccuMachine(Machine):
    def __init__(self, text=None, dynamic=False, **kw):
        Machine.__init__(self, text, dynamic, **kw)
        self.EXCLUDE = ["PUSH", "POP"]
        self.accu = 0

    def executeArithmetic(self):
        instruction = self.instructions[self.pc]
        cmd = instruction[0]
        if len(instruction) == 1:
            if cmd == self.map["SQRT"]:
                self.accu = self.accu**0.5
            elif cmd == self.map["NEG"]:
                self.accu = -self.accu
            elif cmd == self.map["ABS"]:
                self.accu = abs(self.accu)
            else:
                raise CommandException("Unknown command",
                                       found=cmd, line=self.getLine())
        elif len(instruction) == 2:
            arg = self.getValue(instruction[1])
            if cmd == self.map["ADD"]:
                self.accu += arg
            elif cmd == self.map["SUB"]:
                self.accu -= arg
            elif cmd == self.map["MUL"]:
                self.accu *= arg
            elif cmd == self.map["DIV"]:
                if arg==0:
                    raise ArithemeticException("Division by zero",
                                                line=self.getLine())
                self.accu /= arg
            elif cmd == self.map["MOD"]:
                if arg==0:
                    raise ArithemeticException("Division by zero",
                                                line=self.getLine())
                self.accu %= arg
            elif cmd == self.map["POW"]:
                self.accu **= arg
        else:
            raise ParameterException("Too many parameter",
                                    line=self.getLine())
        self.setFlags(self.accu)

    def executeDataTransfert(self):
        instruction = self.instructions[self.pc]
        cmd = instruction[0]
        if len(instruction) == 2:
            arg = instruction[1]
            if cmd == self.map["LOAD"]:
                self.accu = self.getValue(arg)
            elif cmd == self.map["STORE"]:
                self.setValue(arg, self.accu)
            else:
                raise CommandException("Unknown command",
                                        found=cmd, line=self.getLine())
        elif len(instruction) == 3:
            if cmd == self.map["VAL"]:
                self.createVar(instruction[1], instruction[2])
            else:
                raise CommandException("Unknown command",
                                        found=cmd, line=self.getLine())
        else:
            raise ParameterException("Too many parameter",
                                    line=self.getLine())


if __name__ == "__main__":
    txt = """val          x 23
    load x
    SQRT
    jez end
    store x
    output x
    end:output    stoppppppp
    """.upper()
    m = AccuMachine(registers=32)
    m.parse(txt)
    m.loop()