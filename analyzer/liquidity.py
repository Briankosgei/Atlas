class LiquidityDetector:
    """
    AtlasTrader Liquidity Engine

    Detects:

        • Buy Side Liquidity (BSL)
        • Sell Side Liquidity (SSL)
        • Equal Highs
        • Equal Lows
        • Liquidity Sweeps
        • Fake Sweeps
        • Sweep Strength
        • Internal / External Sweeps

    Returns standardized output for:

        • Signal Engine
        • Confidence Engine
        • Trade Planner
        • BOS
        • CHoCH
    """

    def __init__(
        self,
        lookback=20,
        equal_tolerance=0.0005,
    ):

        self.lookback = lookback
        self.equal_tolerance = equal_tolerance

    ##############################################################

    def _equal(self, a, b):

        return abs(a - b) <= self.equal_tolerance

    ##############################################################

    def detect(
        self,
        candles,
        structure,
    ):

        if (
            candles is None
            or structure is None
            or len(candles) < 3
            or len(structure) < 2
        ):

            return {

                "sweep": False,

                "direction": None,

                "level": None,

                "strength": 0,

                "confidence": 0,

                "type": None,

                "fake": False,

                "reason": "Insufficient data",
            }

        ##########################################################

        last = candles[-1]

        recent = structure[-self.lookback:]

        highs = [
            s for s in recent
            if s.get("type") == "HIGH"
        ]

        lows = [
            s for s in recent
            if s.get("type") == "LOW"
        ]

        ##########################################################
        # Equal High Detection
        ##########################################################

        equal_high = False

        if len(highs) >= 2:

            equal_high = self._equal(
                highs[-1]["price"],
                highs[-2]["price"],
            )

        ##########################################################
        # Equal Low Detection
        ##########################################################

        equal_low = False

        if len(lows) >= 2:

            equal_low = self._equal(
                lows[-1]["price"],
                lows[-2]["price"],
            )

        ##########################################################
        # BUY SIDE LIQUIDITY
        ##########################################################

        if highs:

            level = highs[-1]["price"]

            if (
                last["high"] > level
                and last["close"] < level
            ):

                strength = last["high"] - level

                confidence = 70

                if equal_high:
                    confidence += 15

                structure_type = highs[-1].get(
                    "structure",
                    "UNKNOWN",
                )

                if structure_type == "EXTERNAL":
                    confidence += 15

                return {

                    "sweep": True,

                    "direction": "BUY",

                    "level": level,

                    "strength": round(strength, 5),

                    "confidence": min(
                        confidence,
                        100,
                    ),

                    "type": "BUY_SIDE_LIQUIDITY",

                    "fake": False,

                    "equal_high": equal_high,

                    "equal_low": False,

                    "structure": structure_type,

                    "reason": (
                        "Buy-side liquidity sweep confirmed"
                    ),
                }

        ##########################################################
        # SELL SIDE LIQUIDITY
        ##########################################################

        if lows:

            level = lows[-1]["price"]

            if (
                last["low"] < level
                and last["close"] > level
            ):

                strength = level - last["low"]

                confidence = 70

                if equal_low:
                    confidence += 15

                structure_type = lows[-1].get(
                    "structure",
                    "UNKNOWN",
                )

                if structure_type == "EXTERNAL":
                    confidence += 15

                return {

                    "sweep": True,

                    "direction": "SELL",

                    "level": level,

                    "strength": round(strength, 5),

                    "confidence": min(
                        confidence,
                        100,
                    ),

                    "type": "SELL_SIDE_LIQUIDITY",

                    "fake": False,

                    "equal_high": False,

                    "equal_low": equal_low,

                    "structure": structure_type,

                    "reason": (
                        "Sell-side liquidity sweep confirmed"
                    ),
                }

        ##########################################################
        # Fake Break Detection
        ##########################################################

        if highs:

            level = highs[-1]["price"]

            if last["high"] > level and last["close"] > level:

                return {

                    "sweep": False,

                    "direction": None,

                    "level": level,

                    "strength": 0,

                    "confidence": 30,

                    "type": "BREAKOUT",

                    "fake": True,

                    "equal_high": equal_high,

                    "equal_low": equal_low,

                    "structure": highs[-1].get(
                        "structure",
                        "UNKNOWN",
                    ),

                    "reason": (
                        "Bullish breakout, not liquidity sweep"
                    ),
                }

        if lows:

            level = lows[-1]["price"]

            if last["low"] < level and last["close"] < level:

                return {

                    "sweep": False,

                    "direction": None,

                    "level": level,

                    "strength": 0,

                    "confidence": 30,

                    "type": "BREAKDOWN",

                    "fake": True,

                    "equal_high": equal_high,

                    "equal_low": equal_low,

                    "structure": lows[-1].get(
                        "structure",
                        "UNKNOWN",
                    ),

                    "reason": (
                        "Bearish breakout, not liquidity sweep"
                    ),
                }

        ##########################################################

        return {

            "sweep": False,

            "direction": None,

            "level": None,

            "strength": 0,

            "confidence": 0,

            "type": None,

            "fake": False,

            "equal_high": equal_high,

            "equal_low": equal_low,

            "structure": None,

            "reason": "No liquidity event detected",
        }