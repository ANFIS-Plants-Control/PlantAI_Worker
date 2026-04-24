from typing import Dict
from MF import MF
from Rule import Rule
from Term import Term


class FuzzyVariable:
    """Лингвистическая переменная с набором функций принадлежности"""
    def __init__(self, terms: dict[str, Term]):
        self.terms = terms

    def compute(self, val: float):
        for t in self.terms:
            self.terms[t].ComputeTermValue(val)

    def setTermsDegrees(self, range):
        self.termsDegrees: dict[str, list[float]] = {}
        for t in self.terms:
            self.termsDegrees[t] = []
            for x in range:
                self.terms[t].ComputeTermValue(float(x))
                self.termsDegrees[t].append(self.terms[t].value)