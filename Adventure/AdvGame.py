# File: AdvGame.py

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# Unless you are implementing extensions, you won't need to add new       #
# public methods (i.e., methods called from other modules), but the       #
# amount of code you need to add is large enough that decomposing it      #
# into helper methods will be essential.                                  #
###########################################################################

from AdvRoom import AdvRoom
from AdvObject import AdvObject
from tokenscanner import TokenScanner

ACTION_WORDS = ['LOOK', 'HELP', 'INVENTORY', 'TAKE', 'DROP']
DIRECTION_WORDS = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'UP', 'DOWN', 'IN', 'OUT']
PUZZLE_WORDS = ['PLUGH', 'XYZZY', 'UMBRELLA', 'WAVE', 'JUMP', 'FIRE', 'CLUE', 'WATER', 'SWIM']

class AdvGame:

    def __init__(self, prefix):
        """Reads the game data from files with the specified prefix."""
        with open(prefix + 'Rooms.txt') as f:
            self._rooms = {}
            while True:
                room = AdvRoom.readRoom(f)
                if room is None: break
                if len(self._rooms) == 0:
                    self._rooms['START'] = room
                name = room.getName()
                self._rooms[name] = room

        try:
            with open(prefix + 'Objects.txt') as f:
                self._objects = {}
                while True:
                    object = AdvObject.readObject(f)
                    if object is None: break
                    name = object.getName()
                    self._objects[name] = object
        except:
            self._objects = {}
        try:
            with open(prefix + 'Synonyms.txt') as f:
                self._synonyms = {}
                sep = '='
                for line in f:
                    index = line.find(sep)
                    key = line[:index].strip()
                    value = line[index + len(sep):].strip()
                    self._synonyms[key] = value
        except:
            self._synonyms = {} 
        try:
            with open(prefix + 'PermObjects.txt') as f:
                self._permanent = {}
                sep = '='
                for line in f:
                    index = line.find(sep)
                    key = line[:index].strip()
                    value = line[index + len(sep):].strip()
                    self._permanent[key] = value
        except:
            self._permanent = {} 
                    

    def getRoom(self, name):
        """Returns the AdvRoom object with the specified name."""
        return self._rooms[name]
        

    def run(self):
        """Plays the adventure game stored in this object."""
        self.initializeObjects(self._rooms, self._objects)
        current = 'START'
        new_room = True
        while current != 'EXIT':
            room = self.getRoom(current)
            if (any('FORCED' in passages for passages in room.getPassages()) or
                any('RETURN' in passages for passages in room.getPassages())):
                printLongDesc(room)
                room.setVisited(True)
                current = self.getNextRoom(room, None, prev)
            else:
                if new_room:
                    if room.hasBeenVisited():
                        printShortDesc(room)
                    else:
                        printLongDesc(room)
                        room.setVisited(True)
                response = input('>').strip().upper()
                tokens = listTokens(response)
                if 'QUIT' in tokens: break
                elif self.scanFor(tokens, ACTION_WORDS) is not None:
                    item = self.scanFor(tokens, self._objects)
                    if item is None:
                        item = self.scanFor(tokens, self._permanent)
                    if self.scanFor(tokens, ['ALL']) is not None:
                        item = self.scanFor(tokens, ['ALL'])
                    self.preformAction(self.scanFor(tokens, ACTION_WORDS), item, room)
                    new_room = False
                else:
                    new_room = True
                    next = self.getNextRoom(room, self.scanFor(tokens, DIRECTION_WORDS + PUZZLE_WORDS))
                    if next is None:
                        print("I don't understand that response.")
                    else:
                            prev = current
                            current = next


    def initializeObjects(self, rooms, objects):
        self._player = set()
        for name, object in objects.items():
            room = rooms.get(object.getInitialLocation())
            if room is not None:
                room.addObject(object)
            else:
                self._player.add(object)

    def preformAction(self, action, item_word, room):
        if action == ACTION_WORDS[0]:
            printLongDesc(room)
        elif action == ACTION_WORDS[1]:
            for line in HELP_TEXT:
                print(line)
        elif action == ACTION_WORDS[2]:
            if len(self._player) != 0:
                print('You are carrying:')
                for item in self._player:
                    print(item.getDescription())
            else:
                print('You are empty-handed.')
        elif action == ACTION_WORDS[3]:
            if item_word in self._objects and self._objects[item_word] in room.getContents():
                self._player.add(self._objects[item_word])
                room.removeObject(self._objects[item_word])
                print('Taken.')
            elif item_word in self._permanent and self._permanent[item_word] == room.getName():
                print("You can't take that.")
            elif item_word == 'ALL':
                if len(room.getContents()) != 0:
                    self._player = room.getContents() | self._player
                    room.getContents().clear()
                    print('Taken.')
                else:
                    print("There's nothing here to take.")
            else:
                print('I do not see that item')
        else:
            if item_word in self._objects and self._objects[item_word] in self._player:
                self._player.remove(self._objects[item_word])
                room.addObject(self._objects[item_word])
                print('Dropped.')
            elif item_word == 'ALL':
                if len(self._player) != 0:
                    contains = []
                    for obj in self._player:
                        contains.append(obj)
                    for obj in contains:
                        self._player.remove(obj)
                        room.addObject(obj)
                    print('Dropped.')
                else:
                    print('You are empty-handed.')
            else:
                print('You are not carrying that.')

    def getNextRoom(self, room, verb, prev_room = None):
        for direction, location, key in room.getPassages():
            if direction == verb:
                if key is not None and self._objects[key] in self._player:
                    return location
                elif key is None:
                    return location
            elif direction == '*':
                return location
            elif direction == 'FORCED':
                if key is not None and self._objects[key] in self._player:
                    return location
                elif key is None:
                    return location
            elif direction == 'RETURN':
                return prev_room

    def scanFor(self, scanner, options):
        for w in scanner:
            if w in options:
                return w
            elif w in self._synonyms and self._synonyms[w] in options:
                return self._synonyms[w]
        return None
                    
def printLongDesc(room):
    for line in room.getLongDescription():
        print(line)
    for obj in room.getContents():
        print('There is ' + obj.getDescription() + ' here.')

def printShortDesc(room):
    print(room.getShortDescription())
    for obj in room.getContents():
        print('There is ' + obj.getDescription() + ' here.')

def listTokens(s):
    scanner = TokenScanner(s)
    scanner.ignoreWhitespace()
    tokens = []
    while scanner.hasMoreTokens():
        token = scanner.nextToken().upper()
        if token.isalpha():
            tokens.append(token)
    return tokens

# Constants

HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    'Keep a look out for secret treasure as well. Those who have searched',
    'the cave previously are said to have left notes behind for those that',
    'come after them. Rumor has it that should you find the hidden treasure',
    'you would amass an even greater fortune when you leave, but I have never',
    'seen this done before. No one has been able to slove all of the clues.',
    '',
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are, say LOOK.  If you",
    "want to end your adventure, say QUIT."
]

