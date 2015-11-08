class pickup:
    """Formats the provided dictionary and writes it to file.

    :attribute scores: List of scores attached to the various game objects.
    :type scores: dict

    """

    scores = {'pickup': 50}

    def __init__(self):
        pass

    def confirmObject(self, player):
        """RayCasts to ensure that the player avatar is above an object that is allowed to be picked up.

        :param player: The game object of the player avatar.
        :type player: KX_GameObject

        :returns: 1 if success, -1 otherwise.

        """
        rayTest = player.rayCastTo([player.localPosition.x, player.localPosition.y, player.localPosition.z - 1.0], 0)
        print(rayTest)
        if str(rayTest) == "pickup":
            return 1
        return -1

    def evaluate(self, player):
        """RayCasts to ensure that the player avatar is above an object that is allowed to be picked up and gives the player score.

        :param player: The game object of the player avatar.
        :type player: KX_GameObject

        :returns: A tuple containing the object as well as the score attached to the object if success , a tuple containing the string 'fail' and -1 otherwise.

        """
        rayTest = player.rayCastTo([player.localPosition.x, player.localPosition.y, player.localPosition.z - 1.0], 0)

        try:
            return (rayTest, self.scores[str(rayTest)])
        except:
            return ("fail", -1)