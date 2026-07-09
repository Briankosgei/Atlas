class StructureClassifier:
    """
    Classifies swing highs and lows into:
    HH = Higher High
    HL = Higher Low
    LH = Lower High
    LL = Lower Low
    """

    def classify(self, swings):

        classified = []

        last_high = None
        last_low = None

        for swing in swings:

            if swing["type"] == "HIGH":

                if last_high is None:
                    label = "HIGH"

                elif swing["price"] > last_high:
                    label = "HH"

                else:
                    label = "LH"

                last_high = swing["price"]

            else:

                if last_low is None:
                    label = "LOW"

                elif swing["price"] > last_low:
                    label = "HL"

                else:
                    label = "LL"

                last_low = swing["price"]

            classified.append({
                **swing,
                "label": label
            })

        return classified