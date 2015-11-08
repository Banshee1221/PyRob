import time
import bge
import mathutils


class mover:
    """Handles the movement of the player avatar on the Blender scene.

    :attribute moving: Keeps track of whether the player avatar is moving or not.
    :type moving: bool      
    :attribute endTime: Tracks the time that the player avatar moves.
    :type moving: float
    :attribute startTime: When the player avatar starts moving.
    :type moving: float
    :attribute endPos: Position in world space where the player avatar stops.
    :type moving: list
    :attribute startPos: Position in world space before the player avatar starts moving.
    :type moving: list

    """

    def __init__(self):
        # pass
        self.moving = False
        self.endTime = 0
        self.startTime = 0
        self.endPos = []
        self.startPos = []

    def moveUnitOne(self, obj, dir, winObj):
        """Function to manage the movement of the player avatar and check collisions.

        :param obj: The Blender game object of the player avatar.
        :type obj: KX_GameObject
        :param dir: The string which indicates the direction that the avatar will move.
        :type dir: str
        :param winObj: The Blender game object of the object that needs to be conected with in order for the player to win.
        :type winObj: KX_GameObject

        :returns: -1 if the player avatar object fails a raycast test, 2 if the player object raycasts and moves towards the winning object, the time delta of the movement.

        """

        win = False
        fail = False
        x = 0
        y = 0

        if dir is "n":
            rayTest = obj.rayCastTo([obj.localPosition.x, obj.localPosition.y + 0.501, obj.localPosition.z], 0)
            if (rayTest) is winObj:
                win = True
            elif (rayTest) is not None:
                fail = True
            y = 1
        elif dir is "s":
            rayTest = obj.rayCastTo([obj.localPosition.x, obj.localPosition.y - 0.501, obj.localPosition.z], 0)
            if (rayTest) is winObj:
                win = True
            elif (rayTest) is not None:
                fail = True
            y = -1
        elif dir is "e":
            rayTest = obj.rayCastTo([obj.localPosition.x + 0.501, obj.localPosition.y, obj.localPosition.z], 0)
            if (rayTest) is winObj:
                win = True
            elif (rayTest) is not None:
                fail = True
            x = 1
        elif dir is "w":
            rayTest = obj.rayCastTo([obj.localPosition.x - 0.501, obj.localPosition.y, obj.localPosition.z], 0)
            if (rayTest) is winObj:
                win = True
            elif (rayTest) is not None:
                fail = True
            x = -1

        if fail:
            print(rayTest)
            percent = 0
            return -1

        if (self.moving == False):
            self.startTime = time.time()
            self.endTime = self.startTime + 0.25
            self.moving = True
            self.endPos = [obj.position.x + x, obj.position.y + y, obj.position.z]
            self.startPos = [obj.position.x, obj.position.y, obj.position.z]

        percent = (time.time() - self.startTime) * 4
        if (percent < 1):
            # print(percent)
            obj.worldPosition = lerp(self.startPos, self.endPos, percent)
        else:
            percent = 1
            obj.worldPosition = lerp(self.startPos, self.endPos, percent)
            self.moving = False

        if win:
            percent = 0
            obj.worldPosition = winObj.worldPosition
            return 2

        return percent

    """
    def moveUnit(self, obj, dir, steps):

        x = 0
        y = 0

        if dir is "n":
            y = steps
        elif dir is "s":
            y = -steps
        elif dir is "e":
            x = steps
        elif dir is "w":
            x = -steps

            # obj.setLinearVelocity([y, x, 0], True)
        obj.worldPosition = [obj.position.x + x, obj.position.y + y, obj.position.z]
    """


def lerp(startPos, endPos, percent):
    """Lerp function to move the player avatar object along with the main game loop.

    :param startPos: The position of the player avatar object before the move.
    :type startPos: list
    :param endPos: The position that the player avatar object needs to move towards.
    :type endPos: list
    :param percent: The time delta as calculated in moveUnitOne.
    :type percent: float

    :returns: The position of the game object.

    """
    x = startPos[0] + percent * (endPos[0] - startPos[0])
    y = startPos[1] + percent * (endPos[1] - startPos[1])
    return ([x, y, startPos[2]])
