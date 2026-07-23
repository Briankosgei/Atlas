class SignalGrade:
    """
    AtlasTrader Signal Grade

    Converts a confidence score (0-100)
    into a standardized trading grade.

    Returns:
        grade
        quality
        confidence
    """

    ##########################################################

    def grade(self, confidence):

        ######################################################
        # Validate Input
        ######################################################

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.0

        confidence = max(0.0, min(confidence, 100.0))

        ######################################################
        # Grade Mapping
        ######################################################

        if confidence >= 95:
            grade = "A+"
            quality = "Excellent"

        elif confidence >= 90:
            grade = "A"
            quality = "Very High"

        elif confidence >= 80:
            grade = "B+"
            quality = "High"

        elif confidence >= 70:
            grade = "B"
            quality = "Good"

        elif confidence >= 60:
            grade = "C"
            quality = "Average"

        elif confidence >= 50:
            grade = "D"
            quality = "Weak"

        else:
            grade = "F"
            quality = "Poor"

        ######################################################
        # Return
        ######################################################

        return {
            "grade": grade,
            "quality": quality,
            "confidence": round(confidence, 2),
        }