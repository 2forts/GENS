def Mutation(nGPUS, nCPUS, nNTypes, nTray, nPopulationSize, population, nGenome, tcuda, tcpu, probability):
	"""Applies a mutation to the individuals with some probabbility.

	The probability is checked in each individual.

	Parameters:
	nGPUS -- number of GPU devices
	nCPUS -- number of CPU cores
	nNTypes --  number of types of devices
	nTray -- number of trajectories of each size to solve
	nnPopulationSize -- size of the population
	population -- a list with individuals
	nGenome -- the index (in  population) of the individual which be afected by the mutation
	tcuda -- times for the GPU devices for each size
	tcpu -- times for the CPU cores for each size
	probability -- the probability of apply the mutation

	"""
	nDISP = nGPUS + nCPUS
	father = population[nGenome]

	times = [0] * nDISP
	for i in range(nDISP):
		time = 0
		for j in range(nNTypes):
			if i < nGPUS:
				time = time + father[i][j] * tcuda[j]
			else:
				time = time + father[i][j] * tcpu[j]

		times[i] = time

	for i in range(nDISP):
 		for j in range(nDISP):
			if i != j:
				ind1 = [0] * nNTypes
				ind2 = [0] * nNTypes

				for k in range(nNTypes):
					ind1[k] = father[i][k]
					ind2[k] = father[j][k]

				for k in range(nNTypes):
					valid = random.randrange(0, 10)
					if valid >= probability:
						aux = ind1[k]
						ind1[k] = ind2[k]
						ind2[k] = aux

						#Random mutation
						mut = random.randrange(0, ind1[k])
						if (ind2[k] + mut)<nTray:
							ind1[k] -= mut
							ind2[k] += mut

				timei = 0
				timej = 0
				for k in range(nNTypes):
					if i < nGPUS:
						timei += ind1[k] * tcuda[k]
					else:
						timei += ind1[k] * tcpu[k]

					if j < nGPUS:
                                		timej += ind2[k] * tcuda[k]
                            		else:
                                		timej += ind2[k] * tcpu[k]

				if max(timei, timej) < max(times[i], times[j]):
					for w in range(nNTypes):
						father[i][w] = ind1[w]
						father[j][w] = ind2[w]

					times[i] = timei
					times[j] = timej

	population[nGenome] = father