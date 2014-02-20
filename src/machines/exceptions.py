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

class PySamException(Exception):
    def __init__(self, msg=None, *args, **kw):
        lst = list(args)
        lst.extend(kw.items())
        self.__dict__.update(kw)
        res = ["ERROR:", msg]
        for item in args:
            res.append(str(item))
        for key, item in kw.items():
            if key=="found":
                item = "- %s -" % (item)
            elif key=="line":
                item = "\n\t%s" % (item)
            elif key == "waiting":
                item = "\t waiting: %s\n" %(item)
            res.append(str(item))
        Exception.__init__(self, " ".join(res))

class ParameterException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)

class MemoryException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)

class SyntaxException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)

class CommandException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)

class ArithmeticException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)

class NameException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)

class ValueException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)

class MachineException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)

class SyntaxException(PySamException):
    def __init__(self, msg=None, *args, **kw):
        PySamException.__init__(self, msg, *args, **kw)