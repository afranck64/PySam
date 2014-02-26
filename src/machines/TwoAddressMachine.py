#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      said
#
# Created:     23.06.2012
# Copyright:   (c) Awounang Nekdem Franck
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from errors import *
from Machine import Machine

class TwoAddressMachine(Machine):
    def __init__(self, text=None, dynamic=False, **kw):
        Machine.__init__(self, text, dynamic, **kw)
        self.EXCLUDE = ["PUSH", "POP"]

    def excecuteDataTransfert(self):
        instruction = self.instructions[self.pc]
        cmd = instruction[0]
        if len(instruction) == 3:
            arg1, arg2 = instruction[1], instruction[2]
            if cmd == self.map["VAL"]:
                self.createVar(instruction[1], instruction[2])
            elif cmd == self.map["SWAP"]:
                tmp = self.getValue(arg1)
                self.setValue(arg1, self.getValue(arg2))
                self.setValue(arg2, tmp)
            elif cmd == self.map["COPY"]:
                self.setValue(arg1, self.getValue(arg2))

    def executeArithmetic(self):
        instruction = self.instructions[self.pc]
        cmd = instruction[0]
        if len(instruction) == 1:
            raise ParameterException("Not enough parameters",
                                     line=self.getLine())
        elif len(instruction) == 2:
            arg1 = instruction[1]
            if cmd == self.map["NEG"]:
                self.setValue(arg1, -self.getValue(arg1))
            elif cmd == self.map["ABS"]:
                self.setValue(arg1, abs(self.getValue(arg1)))
            elif cmd == self.map["SQRT"]:
                self.setValue(arg1, self.getValue(arg1)**0.5)
            self.setFlags(self.getValue(arg1))
        elif len(instruction) == 3:
            arg1, arg2 = instruction[1], instruction[2]
            if cmd == self.map["NEG"]:
                self.setValue(arg1, -self.getValue(arg2))
            elif cmd == self.map["ABS"]:
                self.setValue(arg1, abs(self.getValue(arg2)))
            elif cmd == self.map["SQRT"]:
                self.setValue(arg1, self.getValue(arg2)**0.5)
            if cmd == self.map["ADD"]:
                self.setValue(arg1, self.getValue(arg1)+self.getValue(arg2))
            elif cmd == self.map["SUB"]:
                self.setValue(arg1, self.getValue(arg1)-self.getValue(arg2))
            elif cmd == self.map["MUL"]:
                self.setValue(arg1, self.getValue(arg1)*self.getValue(arg2))
            elif cmd == self.map["DIV"]:
                self.setValue(arg1, self.getValue(arg1)/self.getValue(arg2))
            elif cmd == self.map["MOD"]:
                self.setValue(arg1, self.getValue(arg1)%self.getValue(arg2))
            elif cmd == self.map["POW"]:
                self.setValue(arg1, self.getValue(arg1)**self.getValue(arg2))
            self.setFlags(self.getValue(arg1))
        else:
            raise ParameterException("Too many parameters",
                                    line=self.getLine())

if __name__ == "__main__":
    txt = """val x 32
    val y 15
    add x y
    output blalbalba
    output hello
    output nano
    close: output x
    enddor:output y"""
    m = TwoAddressMachine()
    m.parse(txt)
    m.loop()