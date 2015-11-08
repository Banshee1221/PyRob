import ast
import bge
import mover
import picker
import outWriter


class tester:
    """The main class for the game logic.

    :attribute objList: Stores a list of game objects form Blender.
    :type objList: list
    :attribute scene: Stores the scene object of the current Blender level.
    :type objList: KX_Scene
    :attribute codeList: Stores all the code that a player submits per level.
    :type objList: dict
    :attribute levelScore: Keeps track of user score per level.
    :type objList: int
    :attribute staticPosX: Static X world position for player avatar default.
    :type objList: float
    :attribute staticPosY: Static Y world position for player avatar default.
    :type objList: float
    :attribute staticPosZ: Static Z world position for player avatar default.
    :type objList: float
    :attribute actions: Array for storing list of actions to be performed on user submission.
    :type objList: list
    :attribute actionsLen: Keeps track of total action list length for submission.
    :type objList: int
    :attribute step: Progression of current submission.
    :type objList: int
    :attribute winObj: String name of the Blender object that the player needs to reach.
    :type objList: str
    :attribute val: Bool to ensure player is on an object.
    :type objList: bool
    :attribute obj_name: Static string that stores the name of the player object.
    :type objList: str
    :attribute text: Stores the text (code) that a user submits to be evaluated.
    :type objList: str
    :attribute m: Initialise the mover class.
    :type objList: mover.mover
    :attribute p: Initialise the picker class.
    :type objList: picker.pickup
    :attribute running: Keeps track of whether the player code is interpreted and executing.
    :type objList: bool

    """

    objList = None
    scene = None
    codeList = {'tut1': [], 'tut2': [], 'tut3': [], 'pre_loops': [], 'loops': []}
    levelScore = 0
    staticPosX = -9.5
    staticPosY = -9.5
    staticPosZ = 1.06
    actions = []
    actionsLen = 0
    step = 1
    winObj = ""
    val = False

    def __init__(self):
        self.scene = bge.logic.getCurrentScene()
        self.objList = self.scene.objects
        obj_name = 'Cube'
        self.Cube = self.objList[obj_name]
        self.text = ''
        self.m = mover.mover()
        self.p = picker.pickup()
        self.running = False

    def setText(self, stri):
        """Sets the string variable to the text submitted by the user.

        :param stri: String code block provided by the user.
        :type stri: str

        """
        self.text = stri

    def run(self):
        """The main operation. This function takes the user provided code, attempts to build an array of commands to
        execute and execute them.

        :returns: Strings for specific types of errors, -2 if the player collided with the winning object, 0 if moves are complete, a float for the moves progressed.

        """

        # If the winObj name is not yet set, look for it in the scene and set it.
        if self.winObj is "":
            for i in self.objList:
                if "win" in str(i):
                    self.winObj = self.objList[str(i)]

        # If the user provided a source code string, operate on it.
        if self.text != '':
            self.codeList[str(self.scene)].append(self.text)
            outWriter.dictFormatter(self.codeList)

            # Do a check to see if while loops exist in the string.
            tmp = while_check(str(self.text))
            if tmp == -1:
                return "Incorrect command used somewhere. Syntax Error."

            # Replace the original provided string with the modified or non-modified text from the while loop checker.
            self.text = tmp
            print(str(self.text))
            print(self.compile_check(str(self.text)))
            print(valid_check(str(self.text)))
            print(self.codeList)

            # Attempt to compile and execute the source code provided by the player. Sets the steps to be one in
            # preparation for the execution on the scene and reset the user text.
            try:
                codeobj = compile(str(self.text), '<string>', 'exec')
                eval(codeobj, globals(), locals())
                self.actionsLen = len(self.actions)
                self.step = 1
                self.text = ''
                print(self.actions)
            except Exception as e:
                self.text = ''
                return str(e)

        # While there are actions left in the action array, perform the various tasks the user has specified.
        if len(self.actions) > 0:
            currItem = self.actions[0]

            # If the action is a move action, do a raycast test. If pass: move the player avatar and dequeue, else
            # delete array and return error string. If object is winObj, return -2 for win.
            if list(currItem.items())[0][0] == 'move':
                checker = self.m.moveUnitOne(self.Cube, list(currItem.items())[0][1], self.winObj)
                if checker == -1:
                    self.step += 1
                    del self.actions[:]
                    return "Runtime error on move command. Probably into a wall!"

                elif checker == 1:
                    self.step += 1
                    del self.actions[0]
                    self.val = False

                elif checker == 2:
                    self.step += 1
                    del self.actions[0]
                    self.val = False
                    return -2

            # If the action is a check action, do a raycast to the ground to determine if there is an object on the
            # floor. If not, fail and return string, else set val to True.
            if list(currItem.items())[0][0] == 'check':
                checker_pick = self.p.confirmObject(self.Cube)
                if checker_pick == -1:
                    self.step += 1
                    del self.actions[:]
                    return "The object you are checking for does not exist."
                else:
                    print("at check")
                    self.step += 1
                    del self.actions[0]
                    self.val = True

            # If the action is a pickup action, do a raycast and if the object is found return the score to blender_test
            # If the object does not exist then fail, if not checked then fail.
            if list(currItem.items())[0][0] == 'pickup':
                checker_pick = self.p.evaluate(self.Cube)
                # print(self.val, checker_pick)
                if checker_pick[1] == -1:
                    print("here")
                    self.step += 1
                    del self.actions[0]
                    return "You are not on top of an object, so you can't pick it up."
                if not self.val and checker_pick[1] != -1:
                    self.step += 1
                    del self.actions[:]
                    return "You did not do a check for object existence."
                else:
                    self.step += 1
                    self.levelScore += checker_pick[1]
                    del self.actions[0]
                    checker_pick[0].endObject()
                    return ("score", self.levelScore)

        # If there are no actions left return 0
        if len(self.actions) == 0:
            return 0

        # Return the float of what's left in the steps for the progress bar.
        return self.step / self.actionsLen

    def compile_check(self, code):
        """Performs a check to ensure that the code provided by the user is correct.

        :param code: Source code string block.
        :type code: str        
        :returns: bool -- True is successfully compiled, False otherwise.

        """
        try:
            compile(code, '<string>', 'exec')
        except Exception as e:
            print(
                "Error executing code!\n=====================\nLine:\t{0}\nSnip:\t{1}\nIssue:\t{2}".format(e.lineno,
                                                                                                           e.text,
                                                                                                           e))
            return False

        return True

    def resetPos(self):
        """Set the player avatar to default world position."""
        self.m.setMoving(False)
        self.Cube.worldPosition = [self.staticPosX, self.staticPosY, self.staticPosZ]

    @classmethod
    def move(cls, dir):
        """Adds a move instruction to the action list in the direction specified.

        :param dir: String for the direction the avatar should move.
        :type dir: str

        """
        cls.actions.append({'move': dir})

    @classmethod
    def pick(cls):
        """Adds a pickup instruction to the action list."""
        cls.actions.append({'pickup': 1})

    @classmethod
    def checker(cls):
        """Adds a checker instruction to the action list."""
        cls.actions.append({'check': 1})

    @classmethod
    def clearArrayOnSceneChange(cls):
        """Clears the actions array in preperation for a new Blender scene to be loaded."""
        cls.actions = []
        cls.actionsLen = 0

    def resetScore(self):
        """Set the user score to zero."""
        self.levelScore = 0


def moveUp():
    """Calls the move classmethod from the tester class for the direction North."""
    tester.move("n")


def moveDown():
    """Calls the move classmethod from the tester class for the direction South."""
    tester.move("s")


def moveRight():
    """Calls the move classmethod from the tester class for the direction East."""
    tester.move("e")


def moveLeft():
    """Calls the move classmethod from the tester class for the direction West."""
    tester.move("w")


def pickup():
    """Calls the pick classmethod from the tester class."""
    tester.pick()


def object():
    """Placeholder function to always return False.

    :returns: Always false.

    """
    return False


def ground():
    """Calls the checker classmethod from the tester class.

    :returns: Always false.

    """
    tester.checker()
    return False


def valid_check(code):
    """Performs a check to ensure that the code provided by the user is syntactically correct.

    :param code: Source code string block.
    :type code: str
    :returns: True is successfully compiled, False otherwise.

    """
    try:
        node = ast.parse(code)
        # print(ast.dump(node))
    except SyntaxError:
        return False
    return True


def while_check(code):
    """Prevents player from using indefinite while loops by breaking loop after pre-defined amount of iterations.

    :param code: Source code string block.
    :type code: str
    :returns: The modified user source code string block.

    """
    tab = False
    pass1 = False
    tmpArr = code.split('\n')
    lineCount = 0
    wordList = ["_tmpWhileTrackCounter = 0", "_tmpWhileTrackCounter += 1", "if _tmpWhileTrackCounter >= 21:", "break"]

    # Check each word in the submitted code for a "while", otherwise determine if user is using tabs or spaces. Insert
    # if statement to break while loop according to user indentation.
    for all in tmpArr:
        if pass1:
            lineCount += 1
            pass
        elif "while" in all:
            if "\t" in all or "\t" in tmpArr[lineCount + 1]:
                tab = True
            spacing = len(all) - len(all.lstrip())
            spacing1 = len(tmpArr[lineCount + 1]) - len(tmpArr[lineCount + 1].lstrip())
            if tab:
                tmpArr.insert(lineCount, wordList[0].rjust(len(wordList[0]) + spacing, "\t"))
                tmpArr.insert(lineCount + 2, wordList[1].rjust(len(wordList[1]) + spacing1, "\t"))
                tmpArr.insert(lineCount + 3, wordList[2].rjust(len(wordList[2]) + spacing1, "\t"))
                tmpArr.insert(lineCount + 4, wordList[3].rjust(len(wordList[3]) + spacing1 + 1, "\t"))
                pass1 = True
            else:
                tmpArr.insert(lineCount, wordList[0].rjust(len(wordList[0]) + spacing))
                tmpArr.insert(lineCount + 2, wordList[1].rjust(len(wordList[1]) + spacing1))
                tmpArr.insert(lineCount + 3, wordList[2].rjust(len(wordList[2]) + spacing1))
                tmpArr.insert(lineCount + 4, wordList[3].rjust(len(wordList[3]) + spacing1 + 4))
                pass1 = True
        lineCount += 1

    retVal = '\n'.join([str(x) for x in tmpArr])
    return retVal


def if_handler(code):
    """Prevents player from using indefinite while loops by breaking loop after pre-defined amount of iterations.

    :param code: Source code string block.
    :type code: str
    :returns: The modified user source code string block is successful or -1 if failure.

    """
    print("if handler")
    tmpArr = code.split('\n')
    lineCount = 0
    for all in tmpArr:
        lineCount += 1
        if "if" in all:
            if all.lstrip() != "if object() is on ground():":
                print("error!!!!")
                return -1
            else:
                tmpArr[lineCount - 1] = str.replace(tmpArr[lineCount - 1], "is on", "==")
                break

    retVal = '\n'.join([str(x) for x in tmpArr])
    return retVal
