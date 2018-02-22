def InitializePopulation(nDISP, nNTypes, nPopulationSize, nTray):
	"""Create a random population.

	Parameters:
	nDISP -- total number of devices 
	nNTypes --  number of types of devices
	nnPopulationSize -- size of the population
	nTray -- number of trajectories of each size to solve

    """
	population = []

	for i in range(nPopulationSize):
		nSubTray = nTray
		genome = []

		for k  in range(nNTypes):
			nRandVector = GenerateRandVector(nTray, nDISP)
			for j in range(nDISP):
				genome[j][k] = nRandVector

		population.append(genome)

	return population