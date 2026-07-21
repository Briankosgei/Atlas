class SignalGrade:

    def grade(
        self,
        confidence,
    ):

        if confidence >= 95:

            return {

                "grade": "A+",

                "quality": "Excellent"

            }

        elif confidence >= 90:

            return {

                "grade": "A",

                "quality": "High"

            }

        elif confidence >= 80:

            return {

                "grade": "B",

                "quality": "Good"

            }

        elif confidence >= 70:

            return {

                "grade": "C",

                "quality": "Average"

            }

        return {

            "grade": "D",

            "quality": "Poor"

        }