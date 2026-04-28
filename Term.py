from MF import MF


class Term:
    """Лингвистическая переменная (тепло, молодой)"""
    def __init__(self, name:str):
        self.name = name

    def setMembershipFunction(self, MF: MF):
        self.MF = MF
        return self
    
    def ComputeTermValue(self, x: float):
        self.value = self.MF.GetDegreeOfMembership(x)

    def GetMembershipFunctionParams(self):
        params = [self.MF.params[paramName] for paramName in self.MF.params]
        return params
    
    