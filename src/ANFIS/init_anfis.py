from ANFIS import ANFIS
from GeneticAlgorithm import GeneticAlgorithm
from MF import MF
from Term import Term
from ANFIS.ANFIS import ANFIS
from ANFIS.GeneticAlgorithm import GeneticAlgorithm
from ANFIS.MF import MF
from ANFIS.Term import Term
import logging
import numpy as np
from math import sqrt

logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    filemode='w',
    format='%(message)s'
)

anfis = ANFIS(['temperature', 'humidity'])

temperatureTermNames = ['low', 'middle', 'high']
temperatureTerms: dict[str, Term] = {
    temperatureTermNames[0]: Term('low').setMembershipFunction(MF(10, 6)),
    temperatureTermNames[1]: Term('middle').setMembershipFunction(MF(25, 6)),
    temperatureTermNames[2]: Term('high').setMembershipFunction(MF(40, 6))
}
humidityTermNames = ['low', 'middle', 'high']
humidityTerms: dict[str: Term] = {
    humidityTermNames[0]: Term('low').setMembershipFunction(MF(10, 5)),
    humidityTermNames[1]: Term('middle').setMembershipFunction(MF(25, 5)),
    humidityTermNames[2]: Term('high').setMembershipFunction(MF(40, 5))
}
anfis.addFuzzyVariableFromTerms('temperature', temperatureTerms)
anfis.addFuzzyVariableFromTerms('humidity', humidityTerms)

anfis.addRule(['low', 'low'], [0.5, 0.5], 10)
anfis.addRule(['middle', 'low'], [1, 1], 1)
anfis.addRule(['high', 'low'], [1.5, 1.5], 30)
anfis.addRule(['low', 'middle'], [2, 2], 60)

trainingCrispInputs: list[dict[str, float]] = [
    {
        'temperature': 10,
        'humidity': 20
    },
    {
        'temperature': 15,
        'humidity': 20
    },
    {
        'temperature': 30,
        'humidity': 80
    },
    {
        'temperature': 20,
        'humidity': 40
    },
]
targets = [80, 70, 10, 60]

for i in trainingCrispInputs:
    anfis.computeAllFuzzyVariables(i)
    output, _ = anfis.forward(i)
    print(output)

ga = GeneticAlgorithm(1000, 10, 0.001, len(anfis.getParameters()), anfis)
newParams = ga.runAlgorithm(100, trainingCrispInputs, targets, 0.2)
print(newParams)
anfis.setParameters(newParams)
for i in trainingCrispInputs:
    anfis.computeAllFuzzyVariables(i)
    output, _ = anfis.forward(i)
    print(output)
