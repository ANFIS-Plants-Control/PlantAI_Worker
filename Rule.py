from RuleOperationType import RuleOperationType


class Rule:
    def __init__(self, operationType: RuleOperationType, InputVariableNames: list[str]):
        self.operationType = operationType
        self.InputVariableNames = InputVariableNames

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