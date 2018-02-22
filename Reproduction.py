def Reproduction(nDISP, nNTypes, nPopulationSize, population, nGenomeA, nGenomeB):
	"""Obtain a new pair of individuals from another two individuals.

	The reproducition consist in the change of columns between the two fathers.

	Parameters:
	nDISP -- total number of devices
	nNTypes --  number of types of devices
	nnPopulationSize -- size of the population
	population -- the population to evaluate
	nGenomeA -- one father
	nGenomeB -- another father

    """
	fatherA = population[nGenomeA][:];
	fatherB = population[nGenomeB][:];

	sonA = []
	sonB = []
	for i in range(nDISP): 
		A = [0]*nNTypes
		B = [0]*nNTypes

		sonA.append(A)
		sonB.append(B)

	nDiv = random.randrange(1, nNTypes - 1)

	for i in range(nDiv):
		for j in range(nDISP):
			sonA[j][i] = fatherA[j,i]
			sonB[j][i] = fatherB[j,i]

	for i in range(nDiv, nNTypes):
		for j in range(nDISP):
                        sonA[j][i] = fatherA[j,i]
                        sonB[j][i] = fatherB[j,i]

        population.append(sonA)
        population.append(sonB)