def Fitness(nGPU, nDISP, nNTypes, population, timesGPU, timesCPU):
	"""Returns the UB parameter of all individuals for a certain population.

	UB is the difference between the slower device and the faster one.

	Parameters:
	nGPU -- the number of GPUs
	nDISP -- total number of devices
	nNTypes -- number of types of devices
	population -- the population to evaluate
	timeGPU -- list with the times of each size involved for the GPU
	timesCPU -- list with the times of each size involved for the CPU cores

	"""
	maxtime = [0] * len(population)
	mintime = [0] * len(population)
	UB = [0] * len(population)

	for i in range(len(population)):
		son = x[i][:]

		for j in range(nDISP):
                	nTime = 0

		    	for k in range(nNTypes):
                        	if j < nGPU:
                            		nTime += timesGPU[k] * son[j, k]
                        	else:
                            		nTime += timesCPU[k] * son[j, k]

                    	if j == 0:
                        	mintime[i] = nTime
                    	elif nTime < mintime[i]:
                        	mintime[i] = nTime

                    	if nTime > maxtime[i]:
                        	maxtime[i] = nTime

                UB[i] = maxtime[i] - mintime[i];

	return UB;