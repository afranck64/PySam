#-------------------------------------------------------------------------------
# Name:        Machine
# Purpose:
#
# Author:      afranck64
#
# Created:     23.06.2012
# Copyright:   (c) Awounang Nekdem Franck
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import platform

def _print(*args, **kw):
    for i in args:
        print (i)
    for k,v in kw.items():
        print (k,v)


#from src.machines.errors import *
from errors import *

class Type:
    INT = 0
    VAR = 1
    STR = 2
    MEM = 3
    CMD = 4
    LBL = 5
    def __init__(self, value, type=None):
        self.value = value
        self.type = type
        
    def __str__(self):
        return str('"%s"' % (str(self.value)))
    
    def __repr__(self):
        return self.__str__()

class Machine():
    def __init__(self, text=None, dynamic=False, registers=0, **kw):
        if "input" in kw:
            self.input = kw["input"]
        else:
            self.input = input
        if "output" in kw:
            self.output = kw["output"]
        else:
            self.output = _print
        self.EXCLUDE = []
        self.memory = []
        self.registers = {}
        self.namespace = {}
        self.paused = False
        self.linenumbers = {}
        for i in range(registers):
            self.createVar("R"+str(i), 0)
        self.flags = {self.FLAG_POSITIV: False,
                      self.FLAG_NEGATIV: False,
                      self.FLAG_ZERO: False}
        self.map = {}
        for i in self.ARITHMETIC_OPS + self.DATA_OPS +\
                                    self.LOGICAL_OPS + self.IO_OPS:
            self.map[i] = i
        self.labels = {}
        self.instructions = []
        self.isDynamic = dynamic
        self.pc = 0
        self.isEnd = False
        self.fullcode = []

    def getMemory(self, index):
        return self.memory[index]

    def setMemory(self, index, value):
        self.memory[index] = value;

    def createVar(self, name, value=0):
        self.namespace[name] = len(self.memory)
        if self.isInteger(value):
            self.memory.append(self.getInteger(value))
        elif self.isIdentifier(value):
            self.memory.append(self.getValue(str(value)))
        else:
            raise ValueException()

    def isInteger(self, value=0):
        index = None
        if type(value) is int:
            return True
        name = str(value)
        if name.isdigit():
            return True
        try:
            index = int(name)
        except:
            try:
                index = int(name, 2)
            except:
                try:
                    index = int(name, 8)
                except:
                    try:
                        index = int(name, 16)
                    except:
                        pass
        if index is None:
            return False
        else:
            return True
    
    def isIdentifier(self, value):
        value = str(value)
        return len(value)>0 and value.isalnum() and not value[0].isdigit()# and value# in self.namespace

    def getInteger(self, value=0):
        value = str(value)
        if type(value) is int:
            return value
        name = str(value)
        if name.isdigit():
            return int(name)
        index = -1
        try:
            index = int(name)
        except:
            try:
                index = int(name, 2)
            except:
                try:
                    index = int(name, 8)
                except:
                    try:
                        index = int(name, 16)
                    except:
                        pass
        return index


    def getValue(self, name):
        index = -1
        if str(name).isalnum():
            if not name in self.namespace:
                raise NameException("Identifier not found", found=name,
                                    line=self.getLine())
            return self.memory[self.namespace[name]]
        elif self.isInteger(name):
            index = self.getInteger(name)
        if index>=len(self.memory) or 0>index:
            raise MemoryException("Invalid memory bloc", found=name,
                                   line=self.getLine())
        return self.memory[index]

    def setValue(self, name, value):
        index = -1
        if name in self.namespace:
            self.memory[self.namespace[name]] = value
            return
        elif str(name).isidentifier():
            if not name in self.namespace:
                raise NameException("Identifier not found", found=name,
                                    line=self.getLine())
            self.memory[self.namespace[name]] = value
        elif self.isInteger(name):
            index = self.getInteger(name)
        if index>=len(self.memory) or 0>index:
            raise MemoryException("Invalid memory bloc", found=index,
                                   line=self.getLine())

    def setFlags(self, value):
        self.flags[self.FLAG_NEGATIV] = (value < 0)
        self.flags[self.FLAG_ZERO] = (value == 0)
        self.flags[self.FLAG_POSITIV] = (0 < value)

    def parse(self, text):
        index = 0
        linenumber = 0
        self.fullcode = text.splitlines()
        for line in self.fullcode:
            linenumber += 1
            if not line:
                continue
            elif line and line[0] == "#":
                continue
            elif "\"" in line:
                lst = ""
                index = line.index("\"")
                start = line[:index]
                items = start.split()
                if not items:
                    continue
                if ":" in items[0]:
                    lbl, cmd = items[0].split(":")
                    self.labels[lbl] = index
                    items.pop(0)
                    if cmd:
                        items.insert(0, Type(cmd, Type.CMD))

                index += 1
                while (len(line)>index and line[index]!= "\""):
                    lst += line[index]
                    index += 1
                if len(line) == index:
                    raise ValueException("String not closed",
                            line=line + " at lineNr: " + str(linenumber))
                if items:
                    items.append(Type(lst, Type.STR))
                items.extend(line[index+1:].split())
                for i, item in enumerate(items):
                    pass#if item.isdigit():
                        #item[i] = int(item)
            else:
                items = line.split()
                if not items:
                    continue
                if ":" in items[0]:
                    lbl , cmd = items[0].split(":")
                    self.labels[lbl] = index
                    items.pop(0)
                    if cmd:
                        items.insert(0, cmd)
                for i, item in enumerate(items):
                    if item.isdigit():
                        #items[i] = int(item)
                        pass
            if items:
                items[0] = items[0].upper()
                allStr = True
                for item in items:
                    if not isinstance(item, (str, unicode)):
                        allStr = False
                        break
                if not allStr and items[0]!=self.OUTPUT_OP:
                    raise ValueException("String only allowed for output", line=line + " at lineNr: " + str(linenumber+1))
                self.instructions.append(items)
                self.linenumbers[index] = linenumber
                index += 1

    def loop(self):
        while not self.isEnd and not self.paused:
            self.fetch()


    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.loop()
    def fetch(self):
        cmd = self.instructions[self.pc][0]
        if cmd in self.EXCLUDE:
            self.isEnd = True
            raise CommandException("Command unavailable for this machine",
                                    found=cmd, line=self.getLine())

        if cmd in self.DATA_OPS:
            self.executeDataTransfert()
        elif cmd in self.ARITHMETIC_OPS:
            self.executeArithmetic()
        elif cmd in self.LOGICAL_OPS:
            self.executeLogical()
        elif cmd in self.IO_OPS:
            self.executeIO()
        else:
            self.isEnd = True
            raise CommandException("Unknown command",
                                    found=cmd, line=self.getLine())
        self.pc += 1
        if len(self.instructions) <= self.pc:
            self.isEnd = True

    def getLine(self):
        res = []
        line = self.instructions[self.pc]
        print "linenumbs : ", self.linenumbers
        print "lineNumb : ", self.getLineNumber()
        number = self.linenumbers[self.pc] + 1
        for i in line:
            res.append(str(i))
        res.append("- at line:")
        res.append(str(number))
        return " ".join(res)

    def getLineNumber(self):
        return self.linenumbers[self.pc] + 1

    def executeDataTransfert(self):
        instruction = self.instructions[self.pc]
        cmd = instruction[0]
        if cmd == self.map["VAL"]:
            if len(cmd)==3:
                self.namespace[instruction[1]] = len(self.memory)
                self.memory.append(self.getInteger(instruction[2]))
            else:
                raise CommandException("Unknown command",
                                        found=cmd, line=self.getLine())

    def executeArithmetic(self):
        pass

    def executeIO(self):
        instruction = self.instructions[self.pc]
        if not len(instruction)==2:
            raise ParameterException("Bad parameter number", waiting="2 args",
                                     line=self.getLine())
        cmd = instruction[0]
        dest = instruction[1]
        if cmd == self.map["INPUT"]:
            if not type(dest) is int and not self.isDynamic:
                if not dest in self.namespace:
                    raise ParameterException("Missing parameter",
                                             line=self.getLine())
            try:
                value = int(self.input())
            except:
                value = 0
            self.setValue(dest, value)
        elif cmd == self.map["OUTPUT"]:
            if dest in self.namespace:
                self.output(self.getValue(dest))
            else:
                self.output(dest)


    def executeLogical(self):
        instruction = self.instructions[self.pc]
        if not len(instruction)==2:
            raise ParameterException("Bad parameter number", waiting="2 args",
                                     line=self.getLine())
        cmd = instruction[0]
        dest = instruction[1]
        edited = False
        if not type(dest) is int:
            if not dest in self.labels:
                    raise ParameterException("Missing parameter",
                                             line=self.getLine())
            dest = self.labels[dest]
        if cmd == self.map["JEZ"]:
            if self.flags[self.FLAG_ZERO]:
                edited = True
                self.pc = dest
        elif cmd == self.map["JNE"]:
            if not self.flags[self.FLAG_ZERO]:
                edited = True
                self.pc = dest
        elif cmd == self.map["JLT"]:
            if self.flags[self.FLAG_NEGATIV]:
                edited = True
                self.pc = dest
        elif cmd == self.map["JGT"]:
            if self.flags[self.FLAG_POSITIV]:
                edited = True
                self.pc = dest
        elif cmd == self.map["JLE"]:
            if self.flags[self.FLAG_ZERO] or self.flags[self.FLAG_NEGATIV]:
                edited = True
                self.pc = dest
        elif cmd == self.map["JGE"]:
            if self.flags[self.FLAG_ZERO] or self.flags[self.FLAG_POSITIV]:
                edited = True
                self.pc = dest
        elif cmd == self.map["GOTO"]:
            edited = True
            self.pc = dest
        if edited:
            self.pc -= 1 #The fetcher will increment it.


    FLAG_ZERO = "zero"
    FLAG_POSITIV = "positiv"
    FLAG_NEGATIV = "negativ"
    DATA_OPS = ["VAL", "LOAD", "STORE", "PUSH", "POP", "SWAP", "MOV", "COPY"]
    ARITHMETIC_OPS = ["ADD", "SUB", "DIV", "MUL", "SQRT", "MOD", "ABS", "POW",
                      "NEG"]
    LOGICAL_OPS = ["JEZ", "JNE", "JLT", "JGT", "JLE", "JGE", "GOTO",]
    OUTPUT_OP = "OUTPUT"
    IO_OPS = ["INPUT", OUTPUT_OP]

if __name__ == "__main__":
    txt = """val X 32
    val z 65
    val k 1024
    val y 512
    output z
    output y
    continue:
    fuckyou:
    output "salut frangin"
    goto mama
    val y "toto"
    mama: output "salut man, comment tu vas?"
    error:
    """.upper()
    m = Machine()
    m.parse(txt)
    m.loop()