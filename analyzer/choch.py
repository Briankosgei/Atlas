class CHOCHDetector:
    """
    Detect Change of Character.
    """

    def detect(self, structure):

        if len(structure) < 3:

            return {
                "choch": False,
                "direction": None,
            }

        labels = [s["label"] for s in structure[-3:]]

        if "LL" in labels and "HH" in labels:

            return {
                "choch": True,
                "direction": "BUY",
            }

        if "HH" in labels and "LL" in labels:

            return {
                "choch": True,
                "direction": "SELL",
            }

        return {
            "choch": False,
            "direction": None,
        }