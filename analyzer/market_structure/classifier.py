class StructureClassifier:
    """
    AtlasTrader Market Structure Classifier

    Converts raw swing points into market structure.

    Labels:
        HH = Higher High
        HL = Higher Low
        LH = Lower High
        LL = Lower Low

    Also classifies:

        • Strong / Weak swings
        • Internal / External structure

    Returns a standardized structure used by:
        - Trend Engine
        - BOS Detector
        - CHoCH Detector
        - Liquidity Detector
        - Confidence Engine
    """

    def __init__(self, external_threshold=0.005):
        """
        external_threshold

        Percentage move required to classify
        a swing as External Structure.

        Default:
            0.5%
        """

        self.external_threshold = external_threshold

    ###############################################################

    def _structure_type(
        self,
        current_price,
        previous_price,
    ):
        """
        Determines whether a swing is
        Internal or External.
        """

        if previous_price is None:
            return "UNKNOWN"

        movement = abs(
            current_price - previous_price
        ) / previous_price

        if movement >= self.external_threshold:
            return "EXTERNAL"

        return "INTERNAL"

    ###############################################################

    def _strength(
        self,
        current_price,
        previous_price,
    ):
        """
        Determines Strong / Weak swing.
        """

        if previous_price is None:
            return "UNKNOWN"

        movement = abs(
            current_price - previous_price
        ) / previous_price

        if movement >= self.external_threshold:
            return "STRONG"

        return "WEAK"

    ###############################################################

    def classify(self, swings):

        if not swings:
            return []

        classified = []

        last_high = None
        last_low = None

        ###########################################################

        for swing in swings:

            swing_type = swing.get("type")
            price = swing.get("price")

            #######################################################
            # HIGH
            #######################################################

            if swing_type == "HIGH":

                if last_high is None:

                    label = "HIGH"

                elif price > last_high:

                    label = "HH"

                elif price < last_high:

                    label = "LH"

                else:

                    label = "EH"      # Equal High

                strength = self._strength(
                    price,
                    last_high,
                )

                structure = self._structure_type(
                    price,
                    last_high,
                )

                last_high = price

            #######################################################
            # LOW
            #######################################################

            elif swing_type == "LOW":

                if last_low is None:

                    label = "LOW"

                elif price > last_low:

                    label = "HL"

                elif price < last_low:

                    label = "LL"

                else:

                    label = "EL"      # Equal Low

                strength = self._strength(
                    price,
                    last_low,
                )

                structure = self._structure_type(
                    price,
                    last_low,
                )

                last_low = price

            #######################################################
            # UNKNOWN
            #######################################################

            else:

                label = "UNKNOWN"
                strength = "UNKNOWN"
                structure = "UNKNOWN"

            #######################################################
            # Store
            #######################################################

            classified.append({

                **swing,

                "label": label,

                "strength": strength,

                "structure": structure,

            })

        ###########################################################
        # Summary Statistics
        ###########################################################

        bullish = sum(
            1 for s in classified
            if s["label"] in ("HH", "HL")
        )

        bearish = sum(
            1 for s in classified
            if s["label"] in ("LH", "LL")
        )

        external = sum(
            1 for s in classified
            if s["structure"] == "EXTERNAL"
        )

        internal = sum(
            1 for s in classified
            if s["structure"] == "INTERNAL"
        )

        ###########################################################
        # Attach summary to every swing
        ###########################################################

        for item in classified:

            item["summary"] = {

                "bullish_swings": bullish,

                "bearish_swings": bearish,

                "external_swings": external,

                "internal_swings": internal,

                "total_swings": len(classified),

            }

        return classified