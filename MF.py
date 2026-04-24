class MF:
    def __init__(self, left_side, middle_side, right_side):
        self.left_side = left_side
        self.middle_side = middle_side
        self.right_side = right_side

    def GetDegreeOfMembership(self, val):
        result = max(
            min(
                ((val-self.left_side)/(self.middle_side - self.left_side)),
                ((self.right_side - val)/(self.right_side - self.middle_side))
            ), 0)

        return result