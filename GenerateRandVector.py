def GenerateRandVector(nSum, nLong):
	"""Create a random int vector of nLong items. 

	Parameters:
	nDISP -- total number of devices
	nNTypes --  number of types of devices
	nnPopulationSize -- size of the population
	nTray -- number of trajectories of each size to solve

	"""
	k = 0
	randVector = []

	for i in range(nLong):
		nAux = random.randrange(0, nSum)
		randVector.append(nAux)
		k += nAux

	k = k / nSum

	for i in range(nLong):
		nAux = randVector[j] / k
		randVector[i] = nAux
		nSum -= nAux

	randVector[0] += nSum

	return randVector