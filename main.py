from MF import MF
import numpy as np
from Rule import Rule
from Term import Term
from FuzzyVariable import FuzzyVariable
from RuleOperationType import RuleOperationType


outputRange  = np.linspace(0, 100, 100)

ruleOutputs  = []

crispInputs: dict[str, float] = {
    'temperature': 10,
    'humidity': 10
}

temperatureTerms: dict[str, Term] = {
    'low': Term('low').setMembershipFunction(MF(0, 10, 20)),
    'middle': Term('middle').setMembershipFunction(MF(20, 30, 40)),
    'high': Term('high').setMembershipFunction(MF(40, 50, 60))
}

humidityTerms: dict[str: Term] = {
    'low': Term('low').setMembershipFunction(MF(0, 10, 20)),
    'medium': Term('medium').setMembershipFunction(MF(20, 30, 40)),
    'high': Term('high').setMembershipFunction(MF(40, 50, 60)),
}

fuzzyVariables = {
    'temperature' : FuzzyVariable(temperatureTerms),
    'humidity': FuzzyVariable(humidityTerms)
}

for varName in fuzzyVariables:
    fuzzyVariables[varName].compute(crispInputs[varName])


outputVariable = FuzzyVariable({
    'low': Term('low').setMembershipFunction(MF(0, 20, 40)),
    'medium': Term('medium').setMembershipFunction(MF(30, 50, 70)),
    'high': Term('high').setMembershipFunction(MF(60, 80, 100))
})
outputVariable.setTermsDegrees(outputRange)

rules: list[Rule] = []

rules.append(
    Rule(RuleOperationType.intersection, ['temperature', 'humidity']).SetCoefficients([1, 1], 1).SetAntecendes(['low', 'low']).SetConsiquent('fan_speed', 'medium')
)
w = []
z = []
for rule in rules:
    w.append(np.prod([fuzzyVariables[ant].terms[rule.antecendes[ant]].value 
                      for ant in rule.antecendes]))
    
    z.append(sum(
        rule.Coefficients[ant] * crispInputs[ant]
        for ant in rule.antecendes) + rule.FreeCoefficient
    )

normalized_w = []
for a in w:
    normalized_w.append(a/sum(w))

output = sum(w * z for w, z in zip(normalized_w, z))

print(output)
