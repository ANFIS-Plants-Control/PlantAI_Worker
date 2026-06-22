import random

from src.ANFIS.ANFIS import ANFIS


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
        print('start training')
        population = []
        countNewBots = numBots - self.numSurv

        for _ in range(numBots):
            bot = []
            for _ in range(self.paramsCount):
                bot.append(random.uniform(-100, 100))
            population.append(bot)
        

        for e in range(self.numEpochs):
            print(e)
            val = []
            popul_l = len(population)
            for (i, bot) in enumerate(population):
                print(f'population number {i}/{popul_l}')
                self.anfis.setParameters(bot)
                error = 0
                for i, data in enumerate(inputData):
                    self.anfis.computeAllFuzzyVariables(data)
                    answer, _ = self.anfis.forward(data)
                    error += (answer - targetData[i]) ** 2
                val.append(error)

            newPopulation, sval = self.getSurvPopul(population, val, 0)
            best_error = min(val)
            avg_error = sum(val) / len(val)
            self._print_training_status(e + 1, best_error, avg_error)

            if sval[0] < self.accuracy:
                print()
                return newPopulation[0]

            for i in range(countNewBots):
                parent1, parent2 = self.getParents(newPopulation, self.numSurv)
                newBot = []
                for param in range(self.paramsCount):
                    newBot.append(self.crossPointFrom2Parents(parent1, parent2, param))
                newBot = self.mutate(newBot, mutationRate)

                newPopulation.append(newBot)
            population = newPopulation

        print()
        return population[0]

    def _print_training_status(self, epoch: int, best_error: float, avg_error: float):
        progress = epoch / self.numEpochs
        bar_width = 30
        filled = int(bar_width * progress)
        bar = "=" * filled + "." * (bar_width - filled)

        print(
            f"\rEpoch {epoch:3d}/{self.numEpochs} "
            f"[{bar}] "
            f"{progress * 100:6.2f}% "
            f"loss={best_error:.6f} "
            f"avg_loss={avg_error:.6f}",
            end="",
            flush=True,
        )
