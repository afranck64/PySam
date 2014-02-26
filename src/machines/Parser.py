#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      said
#
# Created:     24.06.2012
# Copyright:   (c) Awounang Nekdem Franck
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from src.machines.errors import *
#from exceptions import SyntaxException

#import exceptions.SyntaxException as SyntaxException

class Type:
    INT = 0
    VAR = 1
    STR = 2
    MEM = 3
    CMD = 4
    def __init__(self, value, type=None):
        self.value = value


commands = ["load", "push", "pop", "store", "fuck", "continue"]
class Parser:
    def __init__(self):
        self.linenumbers = {}
        self.instructions = []
        self.labels = {}
        pass

    def parse(self, text):
        index = 0
        linenumber = 0
        self.fullcode = text.splitlines()
        for line in self.fullcode:
            linenumber += 1
            if not line:
                continue
            elif line[0] == "#":
                continue
            elif line[0] == "\"" or line[0].lstrip() == "\"":
                raise SyntaxException("Bad item found", waiting="command",
                                line="%s - at line : %s" % (line, linenumber))
            elif "\"" in line:
                lst = ""
                index = line.index("\"")
                print "wou", index
                start = line[:index]
                items = start.split()
                if not items:
                    continue
                if ":" in items[0]:
                    lbl, cmd = items[0].split(":")
                    self.labels[lbl] = index
                    items.pop(0)
                    if cmd:
                        items.insert(0, cmd)

                index += 1
                while (len(line)>index and line[index]!= "\""):
                    lst += line[index]
                    index += 1
                if len(line) == index:
                    raise ValueException("String not closed",
                            line=line + " at lineNr: " + str(linenumber))
                if items:
                    items.append(lst)
                items.extend(line[index+1:].split())
                for i, item in enumerate(items):
                    if item.isdigit():
                        #item[i] = int(item)
                        pass
            else:
                items = line.split()
                if not items:
                    continue
                elif "\"" in items[0]:
                    raise SyntaxException("Bad item found", waiting="command",
                                line="%s - at line : %s" % (line, linenumber))
                elif ":" in items[0]:
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
                self.instructions.append(items)
                self.linenumbers[index] = linenumber
                index += 1
                print self.instructions



def main():
    p = Parser()
    text = """
    val 1 2
    val 3 4
    push a
    push b
    """
    p.parse(text)

if __name__ == '__main__':
    p = Parser()
    text = """
    val 1 "anf"
    "sdf
    mama:
    val 3 4
    push a
    push b
    """
    p.parse(text)
    
