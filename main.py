from MF import MF
import numpy as np
from Rule import Rule
from Term import Term
from pprint import pprint
from FuzzyVariable import FuzzyVariable
from RuleOperationType import RuleOperationType


output_variable_degrees = []
output_range  = np.linspace(0, 100, 100)

rule_outputs  = []

crisp_inputs: dict[str, float] = {
    'temperature': 10,
    'humidity': 10
}

temperature_terms: dict[str, Term] = {
    'low': Term('low').setMembershipFunction(MF(0, 10, 20)),
    'middle': Term('middle').setMembershipFunction(MF(20, 30, 40)),
    'high': Term('high').setMembershipFunction(MF(40, 50, 60))
}

humidity_terms: dict[str: Term] = {
    'low': Term('low').setMembershipFunction(MF(0, 10, 20)),
    'medium': Term('medium').setMembershipFunction(MF(20, 30, 40)),
    'high': Term('high').setMembershipFunction(MF(40, 50, 60)),
}

fuzzy_variables = {
    'temperature' : FuzzyVariable(temperature_terms),
    'humidity': FuzzyVariable(humidity_terms)
}

for var_name in fuzzy_variables:
    fuzzy_variables[var_name].compute(crisp_inputs[var_name])


output_variable = FuzzyVariable({
    'low': Term('low').setMembershipFunction(MF(0, 20, 40)),
    'medium': Term('medium').setMembershipFunction(MF(30, 50, 70)),
    'high': Term('high').setMembershipFunction(MF(60, 80, 100))
})
output_variable.setTermsDegrees(output_range)

rules: list[Rule] = []
rules.append(
    Rule(RuleOperationType.intersection).SetRule(['temperature', 'humidity'], ['low', 'low'], 'fan_speed', 'medium')
)

for rule in rules:
    alpha = min([fuzzy_variables[ant].terms[rule.antecendes[ant]].value for ant in rule.antecendes])
    
    clipped_output = [
        min(alpha, mu) for mu in output_variable.termsDegrees[rule.consequent_term_name]
    ]

    rule_outputs.append(clipped_output)

aggregated_output  = np.maximum.reduce(rule_outputs)

if np.sum(aggregated_output) == 0:
    result = 0
else:
    result = sum(output_range  * aggregated_output)/sum(aggregated_output)

print(result)