
class JPEG1:
    """
    JPEG1 linear predictor.
    """
    @staticmethod
    def predict(a, b, c):
        return a

class JPEG2:
    """
    JPEG2 linear predictor.
    """
    @staticmethod
    def predict(a, b, c):
        return b

class JPEG3:
    """
    JPEG3 linear predictor.
    """
    @staticmethod
    def predict(a, b, c):
        return c

class JPEG4:
    """
    JPEG4 linear predictor.
    """
    @staticmethod
    def predict(a, b, c):
        return a + b - c

class JPEG5:
    """
    JPEG5 linear predictor.
    """
    @staticmethod
    def predict(a, b, c):
        return a + ((b - c) // 2)  # TODO: ver se tem de ser inteiro

class JPEG6():
    """
    JPEG6 linear predictor.
    """
    @staticmethod
    def predict(a, b, c):
        return b + ((a - b) // 2)

class JPEG7:
    """
    JPEG7 linear predictor.
    """
    @staticmethod
    def predict(a, b, c):
        return (a + b) // 2
