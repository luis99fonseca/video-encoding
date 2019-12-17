# linear predictors
class JPEG1:
    @staticmethod
    def predict(a, b, c):
        return a


class JPEG2:
    @staticmethod
    def predict(a, b, c):
        return b


class JPEG3:
    @staticmethod
    def predict(a, b, c):
        return c


class JPEG4:
    @staticmethod
    def predict(a, b, c):
        return a + b - c


class JPEG5:
    @staticmethod
    def predict(a, b, c):
        return a + ((b - c) // 2)  # TODO: ver se tem de ser inteiro


class JPEG6():
    @staticmethod
    def predict(a, b, c):
        return b + ((a - b) // 2)


class JPEG7:
    @staticmethod
    def predict(a, b, c):
        return (a + b) // 2

