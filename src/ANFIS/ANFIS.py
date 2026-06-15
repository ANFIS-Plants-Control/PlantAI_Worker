from ANFIS.FuzzyVariable import FuzzyVariable
from ANFIS.Rule import Rule
from ANFIS.RuleOperationType import RuleOperationType
from ANFIS.Term import Term
import numpy as np


class ANFIS:
    def __init__(self, inputNames:list[str]):
        self.inputNames = inputNames
        self.fuzzyVariables: dict[str, FuzzyVariable] = {}
        self.rules: list[Rule] = []

    def addFuzzyVariableFromTerms(self, name, terms:dict[str, Term]):
        self.fuzzyVariables[name] = FuzzyVariable(terms)

    def addRule(self, antecendes:list[str], coeffs:list[float], freeCoeff:float):
        self.rules.append(
            Rule(RuleOperationType.intersection, self.inputNames).SetCoefficients(coeffs, freeCoeff).SetAntecendes(antecendes)
        )

    def computeAllFuzzyVariables(self, values: dict[str, float]):
        for fv in self.fuzzyVariables:
            self.fuzzyVariables[fv].compute(values[fv])

    def getParameters(self):
        params = []
        for name in self.inputNames:
            for termName in self.fuzzyVariables[name].terms:
                for mfParam in self.fuzzyVariables[name].terms[termName].GetMembershipFunctionParams():
                    params.append(mfParam)
        for rule in self.rules:
            for c in rule.Coefficients:
                params.append(rule.Coefficients[c])
            params.append(rule.FreeCoefficient)
        return params

    def setParameters(self, params: list[float]):
        iterator = 0
        for name in self.inputNames:
            for termName in self.fuzzyVariables[name].terms:
                for mfParam in self.fuzzyVariables[name].terms[termName].MF.params:
                    self.fuzzyVariables[name].terms[termName].MF.params[mfParam] = params[iterator]
                    iterator += 1
        for rule in self.rules:
            for c in rule.Coefficients:
                rule.Coefficients[c] = params[iterator]
                iterator+=1
            rule.FreeCoefficient = params[iterator]
            iterator+=1

    def forward(self, inputData:dict[str, float]):
        w = []
        z = []
        for rule in self.rules:
            w.append(np.prod([self.fuzzyVariables[ant].terms[rule.antecendes[ant]].value 
                            for ant in rule.antecendes]))
            
            rule.Output = sum(
                rule.Coefficients[ant] * inputData[ant]
                for ant in rule.antecendes) + rule.FreeCoefficient
            z.append(rule.Output)

        normalized_w: list[float] = []
        if(sum(w) == 0):
            return sum(z)/len(z), []
        for a in w:
            normalized_w.append(a/sum(w))

        output = sum(w * z for w, z in zip(normalized_w, z))
        return output, normalized_w