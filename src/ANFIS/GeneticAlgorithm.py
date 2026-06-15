import random
from ANFIS.ANFIS import ANFIS

class GeneticAlgorithm:
    def __init__(self, numEpochs: int, numSurv: int, accuracy: float, paramsCount: int, anfis: ANFIS):
        self.numEpochs = numEpochs
        self.numSurv = numSurv
        self.accuracy = accuracy
        self.paramsCount = paramsCount
        self.anfis = anfis
    
    def getSurvPopul(self, popul, val, reverse):
        newpopul = []
        sval = sorted(val, reverse=reverse)
        for i in range(self.numSurv):
            index = val.index(sval[i])
            newpopul.append(popul[index])
        return newpopul, sval
    
    def getParents(self, curr_popul, nsurv):
        indexp1 = random.randint(0, nsurv - 1)
        indexp2 = random.randint(0, nsurv - 1)
        botp1 = curr_popul[indexp1]
        botp2 = curr_popul[indexp2]

        return botp1, botp2

    def crossPointFrom2Parents(self, botp1, botp2, j):
        pindex = random.random()
        if pindex < 0.5:
            x = botp1[j]
        else:
            x = botp2[j]
        return x

    def mutate(self, bot: list[float], mutation_rate: float, mutation_strength: float = 0.3) -> list[float]:
        new_bot = bot.copy()
        
        for i in range(len(new_bot)):
            if random.random() < mutation_rate:
                mutation = random.gauss(0, mutation_strength * abs(new_bot[i]) + 0.1)
                new_bot[i] += mutation
                
        return new_bot

    def runAlgorithm(self, numBots: int, inputData: list[dict[str, float]], targetData: list[float], mutationRate: float):
        population = []
        countNewBots = numBots - self.numSurv

        for _ in range(numBots):
            bot = []
            for _ in range(self.paramsCount):
                bot.append(random.uniform(-100, 100))
            population.append(bot)

        for e in range(self.numEpochs):
            val = []
            for bot in population:
                self.anfis.setParameters(bot)
                error = 0
                for i, data in enumerate(inputData):
                    self.anfis.computeAllFuzzyVariables(data)
                    answer = self.anfis.forward(data)
                    error += (answer-targetData[i])**2
                val.append(error)
            newPopulation, sval = self.getSurvPopul(population, val, 0)
            
            best_error = min(val)
            print(f"Эпоха {e+1:3d} | Лучшая ошибка (SSE): {best_error:.4f}")

            if sval[0] < self.accuracy:
                return newPopulation[0]
            
            for _ in range(countNewBots):
                parent1, parent2 = self.getParents(newPopulation, self.numSurv)
                newBot = []
                for param in range(self.paramsCount):
                    newBot.append(self.crossPointFrom2Parents(parent1, parent2, param))
                newBot = self.mutate(newBot, mutationRate)
                    
                newPopulation.append(newBot)
            population = newPopulation
        
        return population[0]