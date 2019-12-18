"""
JPEG1 linear predictor.
"""
class JPEG1:
    @staticmethod
    def predict(a, b, c):
        return a

"""
JPEG2 linear predictor.
"""
class JPEG2:
    @staticmethod
    def predict(a, b, c):
        return b

"""
JPEG3 linear predictor.
"""
class JPEG3:
    @staticmethod
    def predict(a, b, c):
        return c

"""
JPEG4 linear predictor.
"""
class JPEG4:
    @staticmethod
    def predict(a, b, c):
        return a + b - c

"""
JPEG5 linear predictor.
"""
class JPEG5:
    @staticmethod
    def predict(a, b, c):
        return a + ((b - c) // 2)  # TODO: ver se tem de ser inteiro

"""
JPEG6 linear predictor.
"""
class JPEG6():
    @staticmethod
    def predict(a, b, c):
        return b + ((a - b) // 2)

"""
JPEG7 linear predictor.
"""
class JPEG7:
    @staticmethod
    def predict(a, b, c):
        return (a + b) // 2
