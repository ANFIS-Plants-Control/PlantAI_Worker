
class Rule:
    def __init__(self, InputVariableNames: list[str]):
        self.InputVariableNames = InputVariableNames
        self.Output: float = 0.0

    def SetCoefficients(self, VariableCoefficients: list[float], FreeCoefficient: float):
        self.Coefficients = {
            name: value
            for name, value in zip(self.InputVariableNames, VariableCoefficients)
        }
        self.FreeCoefficient = FreeCoefficient
        return self
    
    def SetAntecendes(self, InputTermNames: list[str]):
        self.antecendes = {
            inputName: termName
            for inputName, termName in zip(self.InputVariableNames, InputTermNames)
        }
        return self
    
    def SetConsiquent(self, OutputVariableName: str, OutputTermName: str):
        self.consiquentVariableName = OutputVariableName
        self.consiquentTermName = OutputTermName
        return self
    
    def GetCoefficients(self):
        coeffs = [self.Coefficients[cn] for cn in self.Coefficients]
        return coeffs