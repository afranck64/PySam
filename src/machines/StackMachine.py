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

#from exceptions import *
from Machine import *

class StackMachine(Machine):
    def __init__(self, text=None, dynamic=False, **kw):
        Machine.__init__(self, text, dynamic, **kw)
        self.EXCLUDES = ["LOAD", "STORE", "SWAP", "MOV", "COPY"]
        self.stack = []

    def executeArithmetic(self):
        instruction = self.instructions[self.pc]
        print (self.stack, self.memory)
        if not len(instruction) == 1:
            raise ParameterException("Two many parameter", line=self.getLine())
        cmd = instruction[0]
        if self.stack:
            x = self.stack.pop()
            if cmd == self.map["SQRT"]:
                if x < 0:
                    raise ArithmeticException("Square root of negativ number",
                                                line=getLine())
                self.stack.append(x**0.5)
            elif cmd == self.map["NEG"]:
                self.stack.append(-x)
            elif cmd == self.map["ABS"]:
                self.stack.append(abs(x))
            elif 0 < len(self.stack) :
                y = self.stack.pop()
                if cmd == self.map["ADD"]:
                    self.stack.append(y + x)
                elif cmd == self.map["SUB"]:
                    self.stack.append(y - x)
                elif cmd == self.map["MUL"]:
                    self.stack.append(y * x)
                elif cmd == self.map["DIV"]:
                    if x==0:
                        raise ArithemeticException("Division by zero",
                                                   line=self.getLine())
                    self.stack.append(y / x)
                elif cmd == self.map["MOD"]:
                    if x==0:
                        raise ArithemeticException("Division by zero",
                                                   line=self.getLine())
                    self.stack.append(y % x)
                else:
                    raise CommandException("Unknown Command",
                                          line=self.getLine())
            self.setFlags(self.stack[-1])
        else:
            raise ParameterException("Not enough parameter in stack",
                                     line=self.getLine())

    def executeDataTransfert(self):
        instruction = self.instructions[self.pc]
        cmd = instruction[0]
        if len(instruction)==3 and  cmd == self.map["VAL"]:
            self.createVar(instruction[1], instruction[2])
        elif len(instruction) == 2:
            if cmd == self.map["PUSH"]:
                self.stack.append(self.getValue(instruction[1]))
            elif cmd == self.map["POP"]:
                if not self.stack:
                    raise ParameterException("Not enough parameter in stack",
                                             line=self.getLine())
                if instruction[1] in self.namespace:
                    self.memory[self.namespace[instruction[1]]] = self.stack.pop()
                elif self.isDynamic and str(instruction[1]).isidentifier():
                    self.createVar(instruction[1])
                    self.memory[self.namespace[instruction[1]]] = self.stack.pop()
                else:
                    if self.isInteger(instruction[1]):
                        self.setValue(instruction[1], self.stack.pop())
                    else:
                        raise NameException("Identifier not found",
                                    found=instruction[1], line=self.getLine())
            else:
                    raise CommandException("Unknown Command",
                                          line=self.getLine())
        else:
            raise ParameterException("Two many parameters",
                                     line=self.getLine())

if __name__ == "__main__":
    txt = """val x 2
val y 3
val toto 5
val papa 6
val c 9
retour: val a 2
encore: val b 4
push a
push b
push toto
add
add
pop papa
output papa
output "FUCK spece de connar!!! YOU"
""".upper()
    m = StackMachine()
    m.parse(txt)
    m.loop()