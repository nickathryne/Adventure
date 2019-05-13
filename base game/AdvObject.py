# File: AdvObject.js

"""
This module defines a class that models an object in Adventure.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# You won't need to work with this file until Milestone #4.  In my        #
# solution, none of the milestones required any public methods beyond     #
# the ones defined in this starter file.                                  #
###########################################################################

class AdvObject:

    def __init__(self, name, description, location):
        """Creates an AdvObject from the specified properties."""
        self._name = name
        self._description = description
        self._location = location

    def __str__(self):
        """Converts an AdvObject to a string."""
        return self._name

    def getName(self):
        """Returns the name of this object."""
        return self._name

    def getDescription(self):
        """Returns the description of this object."""
        return self._description

    def getInitialLocation(self):
        """Returns the initial location of this object."""
        return self._location

    @staticmethod
    def readObject(f):
        """Reads and returns the next object from the file."""
        name = f.readline().rstrip()
        if name == '':
            return None
        description = f.readline().rstrip()
        location = ''
        while True:
            line = f.readline().rstrip()
            if line == '': break
            location += line
        return AdvObject(name, description, location)