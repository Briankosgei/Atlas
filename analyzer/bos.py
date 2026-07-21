class BOSDetector:
    """
    Detect Break of Structure.
    """

    def detect(self, structure):

        if len(structure) < 2:

            return {
                "bos": False,
                "direction": None,
            }

        last = structure[-1]

        if last["label"] == "HH":

            return {
                "bos": True,
                "direction": "BUY",
            }

        if last["label"] == "LL":

            return {
                "bos": True,
                "direction": "SELL",
            }

        return {
            "bos": False,
            "direction": None,
        }