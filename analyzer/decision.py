class DecisionEngine:

    def decide(self, confidence):

        if confidence >= 80:
            return "BUY / SELL"

        elif confidence >= 60:
            return "WATCH"

        return "NO TRADE"