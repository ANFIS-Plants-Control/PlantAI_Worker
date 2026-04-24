from RuleOperationType import RuleOperationType


class Rule:
    def __init__(self, operationType: RuleOperationType):
        self.operationType = operationType
        self.antecendes = {}
        self.consiquentVariableName = ''
        self.consiquentTermName = ''
    
    def SetRule(self, inputVariableNames: list[str], inputTermNames: list[str], outputVariableName: str, outputTermName: str):
        if len(inputVariableNames) != len(inputTermNames):
            raise ValueError("Количество входных переменных должно совпадать с количеством термов")

        self.antecendes = {
            variableName: termName
            for(variableName, termName) in zip(inputVariableNames, inputTermNames)
        }
        
        self.consiquentVariableName = outputVariableName
        self.consiquentTermName = outputTermName

        return self