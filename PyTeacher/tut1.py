import bge


class tut1:
    """Hotfix code for testing.

    :attribute winCond: Determine if the player wins.

    """
    winCond = False

    def __init__(self, winCon):
        self.winCond = winCon

    def check(self):
        """

        :return: None

        """
        if self.winCond:
            bge.logic.getCurrentScene().replace('loops1.blend')