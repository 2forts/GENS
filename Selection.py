#Auxiliary structure used to sort populations
class FitnessInfo:
    def __init__(self, nIndex, nMaxTime):
        self.nIndex = nIndex
        self.nMaxTime = nMaxTime

def Selection(nPopulationSize, population, fitness):
 	"""Selects the nPopulationSize best individuals of a population and creates a new one with them.

	Parameters:
	nnPopulationSize -- size of the population
	population -- a list with individuals
	fitness -- a list with the puntuation of each individual of the population
	"""
	_allFitnessInfo = []
	nAuxTimes = [] 

	for i in range(len(fitness)):
		aux = FitnessInfo(i, fitness)
		_allFitnessInfo.append(aux)

	#Sort by fitness
	sorted(_allFitnessInfo, key=lambda Fitness: Fitness.nMaxTime)

	#Copy only the best individuals
	newPopulation = []
	while len(newPopulation) < nPopulationSize:
		nIndex = _allFitnessInfo[i].nIndex
		newPopulation.append(population[nIndex])

	population = newPopulation
	return population


