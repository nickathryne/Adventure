# File: AdvRoom.py

"""
This module is responsible for modeling a single room in Adventure.
"""

###########################################################################
# Your job in this milestone is to fill in the definitions of the         #
# methods listed in this file, along with any helper methods you need.    #
# The public methods shown in this file are the ones you need for         #
# Milestone #1.  You will need to add other public methods for later      #
# milestones, as described in the handout.  For Milestone #7, you will    #
# need to move the getNextRoom method into the AdvGame class and replace  #
# it with a getPassages method that returns the dictionary of passages.   #
###########################################################################

# Constants

MARKER = "-----"

class AdvRoom:

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""
        self._name = name
        self._shortdesc = shortdesc
        self._longdesc = longdesc
        self._passages = passages
        self.setVisited(False)
        self._objects = set()

    def getName(self):
        """Returns the name of this room."""
        return self._name

    def getShortDescription(self):
        """Returns a one-line short description of this room."""
        return self._shortdesc

    def getLongDescription(self):
        """Returns the list of lines describing this room."""
        return self._longdesc

    def getPassages(self):
        """Returns the names of the possible destination rooms."""
        return self._passages

    def setVisited(self, flag):
        '''Sets if the room has been visited before.'''
        self._visited = flag

    def hasBeenVisited(self):
        '''Returns whether the room has been visited before.'''
        return self._visited

    def addObject(self, object):
        ''''''
        self._objects.add(object)

    def removeObject(self, object):
        ''''''
        self._objects.remove(object)

    def containsObject(self, object):
        ''''''
        return object in self._objects

    def getContents(self):
        ''''''
        return self._objects

    @staticmethod
    def readRoom(f):
        """Reads a room from the data file."""
        name = f.readline().rstrip()
        if name == '':
            return None
        shortdesc = f.readline().rstrip()
        longdesc = []
        while True:
            line = f.readline().rstrip()
            if line == MARKER: break
            longdesc.append(line)
        passages = []
        while True:
            line = f.readline().rstrip()
            if line == '': break
            colon = line.find(':')
            lock = line.find('/')
            if colon == -1:
                raise ValueError('Missing colon in ' + line)
            if lock == -1:
                requires = None
                next = line[colon + 1:].strip()
            else:
                next = line[colon + 1:lock].strip()
                requires = line[lock + 1:].strip()
            response = line[:colon].strip().upper()
            passages.append((response, next, requires))
        return AdvRoom(name, shortdesc, longdesc, passages)
