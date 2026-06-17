from openpyxl import load_workbook
from src.ANFIS.ANFIS import ANFIS
from src.ANFIS.GeneticAlgorithm import GeneticAlgorithm

class Gym:
    def __init__(self, anfis: ANFIS):
        self.anfis = anfis

    def train(self):
        book = load_workbook("./static/MarkeredData.xlsx")
        ws = book.active

        ga = GeneticAlgorithm(100, 10, 0.001, len(self.anfis.getParameters()), self.anfis)
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            trainingParams: list[dict[str, float]] = []
            targets: list[float] = []

            for i in range(10):
                co2 = float(row[0])
                hum = float(row[1])
                temp = float(row[2])
                target = float(row[4])
                trainingParams.append([{'temperature':temp}, {'humidity', hum}, {'co2': co2}])
                targets.append(target)
            
            newParams = ga.runAlgorithm(100, trainingParams, targets, 0.2)
            self.anfis.setParameters(newParams)
    
        return self.anfis