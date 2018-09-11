import sys, logging, time, os, random, platform, uuid, threading
from multiprocessing import Process, Queue, Pool, cpu_count, current_process, Manager, Semaphore
from time import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

#Example of method to launch a program execution into a GPU		
def gpu_consumer_task(q, r, semaphore, results_dict, sNode, nCore):
	ta = time()

	while len(q) > 0:
		name = current_process().name
                try:
			value = q.pop(0)
			
			if (value[1] <= 0):
				continue
			t1 = time()
			uid = r.get(True, 0.05)  
			logger.info("(%d)parallel consumer [%s] in %s getting value [%d] (ntray: %d, ttrat: %d) from queue..." % (uid, name, sNode, value[0], value[1], value[2]))
			srun = ...
			#Example: srun = "srun -N 1 -n 1 -p ibgpu -w %s --gres=gpu:1 ./micro -N %d -n %d -t %d -i %d" % (sNode, value[0], value[1], value[2], uid)
			os.system(srun)
			t2 = time()

			if results_dict.has_key(name):
				results_dict[name] = "%s-(N: %d ntray: %d ttray: %d)" % (results_dict[name], value[0], value[1], value[2]) 
			else:
				results_dict[name] = "(N: %d ntray: %d ttray: %d)" % (value[0], value[1], value[2])
			
        		tf = t2 - t1
			with open("tiempos_gpu.txt", mode='a') as file:
                		file.write('Time %s:  %s. Started: %s. NODE %s\n' % (name, tf, t1, sNode))

		except:
			logger.info("%s could not access to the queue at this moment: %s" % (name, sys.exc_info()) )

	tb = time()
	tf = tb - ta
	with open("final_gpu.txt", mode='a') as file:
        	file.write('Tiempo de %s:  %s. \n' % (name, tf))

#Example of method to launch a program execution into a CPU
def cpu_consumer_task(q, r, semaphore, results_dict, sNode, nCore):
	ta = time()

	while len(q) > 0:
		name = current_process().name
		try:
            value = q.pop()
					
			if (value[1] <= 0):
				continue
			
			uid = r.get(True, 0.05)	
			t1 = time()
			logger.info("(%d)sequential consumer [%s] in %s getting value [%d] (ntray: %d, ttrat: %d) from queue..." % (uid, name, sNode, value[0], value[1], value[2]))
			srun = ...
			#Example: srun = "srun -n 1 -w %s taskset -c %d ./microAux %d %d %d %d" % (sNode, nCore, value[0], value[1], value[2], uid)
			os.system(srun)
 			t2 = time()
			
			if results_dict.has_key(name):
					results_dict[name] = "%s-(N: %d ntray: %d ttray: %d)" % (results_dict[name], value[0], value[1], value[2])
			else:
					results_dict[name] = "(N: %d ntray: %d ttray: %d)" % (value[0], value[1], value[2])

			tf = t2 - t1
			with open("tiempos_cpu.txt", mode='a') as file:
					file.write('Time %s:  %s. Started: %s. NODE %s, CORE %d\n' % (name, tf, t1, sNode, nCore))
		except:
            logger.info("%s could not access to the queue at this moment: %s" % (name, sys.exc_info()) )
			
	tb = time()
	tf = tb - ta
	with open("final_cpu.txt", mode='a') as file:
		file.write('Tiempo de %s:  %s. \n' % (name, tf))

if __name__ == '__main__':
	data_index = Queue()
	results = Queue()
	semaphore = Semaphore(1)

	manager = Manager() 
	results_dict = manager.dict()

	#This example executes the result of the GA for a case study of 7 sizes: 216, 512, 1000, 2197, 4096, 8000 and 15625
	#In this example, the cluster has 4 machines, "bullxual01" to "bullxual04", each one with 16 cores and 2 GPU's
	#Take into account that two CPU-cores are needed to handle the tow GPUs in each machine, so only 14 CPU-cores are available
	
	#Number of trajectories, time steps and times for sizes 1 to 7 for GPU and CPU
	ntray = 500
	ttray = 500
	tiemposGPU = (167, 172, 182, 193, 226, 336, 540)
	tiemposCPU = (430, 700, 1500, 2900, 5172, 9558, 22253)
	
	#This list contains indexs. Each thread will use an unique index to save a file with an unique name
	nAux = 0
	for i in range(ntray): #Que haya de sobra
		data_index.put(nAux)
		nAux += 1

	#8 GPUs and 64-8 CPU-cores
	ngpus = 8
	ncpus = 56

	data_queue = []
	
	# This configuration is the result of the GA. To separate this example from the GA, it is given implicitly
	data_queue.append([[8000, 1, 500], [15625, 30, 500]])
	data_queue.append([[512, 1, 500], [8000, 10, 500], [15625, 24, 500]])
	data_queue.append([[4096, 1, 500], [8000, 2, 500], [15625, 29, 500]])
	data_queue.append([[8000, 12, 500], [15625, 23, 500]])
	data_queue.append([[8000, 1, 500], [15625, 30, 500]])
	data_queue.append([[8000, 1, 500], [15625, 30, 500]])
	data_queue.append([[4096, 1, 500], [8000, 2, 500], [15625, 29, 500]])
	data_queue.append([[8000, 1, 500], [15625, 30, 500]])
	
	data_queue.append([[216, 7, 500], [2197, 16, 500], [4096, 6, 500],[15625, 1, 500]])
	data_queue.append([[216, 1, 500], [1000, 2, 500], [2197, 2, 500], [4096, 7, 500], [8000, 5, 500]])
	data_queue.append([[512, 19, 500], [1000, 7, 500], [2197, 8, 500], [4096, 2, 500], [8000, 2, 500], [15625, 1, 500]])
	data_queue.append([[216, 4, 500], [512, 4, 500], [1000, 7, 500],  [4096, 4, 500], [8000, 6, 500]])
	data_queue.append([[512, 1, 500], [2197, 4, 500], [4096, 4, 500], [8000, 6, 500]])
	data_queue.append([[216, 1, 500], [2197, 3, 500], [4096, 3, 500], [8000, 4, 500], [15625, 1, 500]])
	data_queue.append([[512, 4, 500], [1000, 1, 500], [2197, 5, 500], [4096, 3, 500], [8000, 6, 500]])
	data_queue.append([[216, 9, 500], [512, 1, 500], [1000, 2, 500], [2197, 2, 500], [4096, 5, 500], [8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[216, 6, 500], [512, 3, 500], [1000, 2, 500], [2197, 6, 500], [4096, 3, 500], [8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[216, 3, 500], [512, 6, 500], [1000, 7, 500], [2197, 7, 500], [4096, 10, 500], [8000, 2, 500]])
	data_queue.append([[216, 15, 500], [512, 3, 500], [1000, 10, 500], [2197, 8, 500],[8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[512, 4, 500],  [4096, 8, 500], [8000, 5, 500]])
	data_queue.append([[512, 10, 500], [1000, 5, 500], [2197, 10, 500],[8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[216, 1, 500], [512, 13, 500], [1000, 14, 500],  [4096, 5, 500], [8000, 2, 500], [15625, 1, 500]])
	data_queue.append([[216, 3, 500], [512, 13, 500], [1000, 7, 500], [2197, 2, 500], [4096, 3, 500], [8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[216, 8, 500], [512, 1, 500], [1000, 10, 500], [2197, 7, 500], [4096, 1, 500], [8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[216, 8, 500], [512, 10, 500], [1000, 3, 500], [2197, 5, 500], [4096, 4, 500], [8000, 5, 500]])
	data_queue.append([[512, 2, 500], [1000, 12, 500], [2197, 6, 500], [4096, 10, 500], [8000, 2, 500]])
	data_queue.append([[216, 16, 500], [1000, 6, 500], [2197, 1, 500], [4096, 6, 500], [8000, 5, 500]])
	data_queue.append([[512, 9, 500], [2197, 1, 500], [4096, 7, 500], [8000, 5, 500]])
	data_queue.append([[216, 7, 500], [512, 1, 500], [1000, 3, 500],  [4096, 5, 500], [8000, 6, 500]])
	data_queue.append([[216, 6, 500], [512, 11, 500], [1000, 3, 500], [2197, 1, 500], [4096, 2, 500], [8000, 4, 500], [15625, 1, 500]])
	data_queue.append([[216, 4, 500], [512, 3, 500],  [4096, 4, 500], [8000, 4, 500], [15625, 1, 500]])
	data_queue.append([[216, 2, 500], [1000, 7, 500], [2197, 2, 500], [4096, 2, 500], [8000, 4, 500], [15625, 1, 500]])
	data_queue.append([[216, 3, 500], [512, 1, 500], [1000, 1, 500], [2197, 2, 500], [4096, 7, 500], [8000, 5, 500]])
	data_queue.append([[216, 6, 500],  [4096, 1, 500], [8000, 8, 500]])
	data_queue.append([[216, 13, 500], [1000, 11, 500], [2197, 21, 500], [4096, 5, 500], [8000, 1, 500]])
	data_queue.append([[216, 5, 500], [1000, 2, 500], [2197, 8, 500],[8000, 4, 500], [15625, 1, 500]])
	data_queue.append([[216, 9, 500], [512, 4, 500], [2197, 7, 500], [4096, 9, 500], [8000, 3, 500]])
	data_queue.append([[216, 2, 500], [512, 1, 500], [1000, 3, 500], [2197, 7, 500], [4096, 9, 500], [8000, 3, 500]])
	data_queue.append([[216, 1, 500], [512, 6, 500], [1000, 1, 500],  [4096, 6, 500], [8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[216, 1, 500], [512, 2, 500], [1000, 3, 500], [2197, 4, 500], [4096, 8, 500], [8000, 4, 500]])
	data_queue.append([[512, 1, 500],  [4096, 2, 500], [8000, 5, 500], [15625, 1, 500]])
	data_queue.append([[216, 12, 500], [512, 5, 500], [1000, 7, 500], [2197, 8, 500], [4096, 14, 500]])
	data_queue.append([[216, 3, 500], [512, 1, 500], [1000, 2, 500],  [4096, 3, 500], [8000, 7, 500]])
	data_queue.append([[216, 2, 500], [512, 1, 500], [2197, 3, 500], [4096, 2, 500], [8000, 7, 500]])
	data_queue.append([[216, 10, 500], [512, 3, 500], [1000, 11, 500], [2197, 1, 500], [4096, 1, 500], [8000, 4, 500], [15625, 1, 500]])
	data_queue.append([[216, 15, 500], [512, 22, 500], [1000, 10, 500], [2197, 10, 500], [4096, 1, 500], [8000, 4, 500]])
	data_queue.append([[512, 27, 500], [1000, 6, 500], [2197, 12, 500], [4096, 1, 500], [8000, 4, 500]])
	data_queue.append([[512, 7, 500], [1000, 4, 500], [2197, 1, 500], [4096, 4, 500], [8000, 6, 500]])
	data_queue.append([[512, 6, 500], [1000, 3, 500], [2197, 5, 500],[8000, 7, 500]])
	data_queue.append([[216, 9, 500], [512, 5, 500], [1000, 16, 500], [2197, 3, 500], [4096, 6, 500], [8000, 1, 500], [15625, 1, 500]])
	data_queue.append([[216, 2, 500], [1000, 7, 500], [2197, 6, 500], [4096, 4, 500], [8000, 5, 500]])
	data_queue.append([[216, 3, 500], [512, 4, 500], [1000, 9, 500], [2197, 1, 500], [4096, 4, 500], [8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[2197, 24, 500], [4096, 4, 500], [8000, 2, 500]])
	data_queue.append([[512, 1, 500], [2197, 4, 500], [4096, 4, 500], [8000, 6, 500]])
	data_queue.append([[216, 2, 500], [512, 4, 500], [1000, 2, 500], [2197, 2, 500], [4096, 5, 500], [8000, 3, 500], [15625, 1, 500]])
	data_queue.append([[216, 4, 500], [512, 7, 500], [1000, 1, 500],  [4096, 1, 500], [8000, 5, 500], [15625, 1, 500]])
	data_queue.append([[216, 8, 500], [1000, 4, 500], [2197, 8, 500], [4096, 1, 500], [8000, 6, 500]])
	data_queue.append([[1000, 8, 500],  [4096, 2, 500], [8000, 7, 500]])
	data_queue.append([[216, 4, 500], [512, 3, 500], [1000, 6, 500], [2197, 4, 500], [4096, 8, 500], [8000, 1, 500], [15625, 1, 500]])
	data_queue.append([[216, 3, 500], [512, 3, 500], [2197, 6, 500], [4096, 17, 500]])
	data_queue.append([[512, 2, 500], [1000, 4, 500],  [4096, 5, 500], [8000, 6, 500]])
	data_queue.append([[216, 3, 500], [512, 13, 500], [1000, 10, 500], [2197, 2, 500],[8000, 4, 500], [15625, 1, 500]])
	data_queue.append([[216, 29, 500],  [4096, 8, 500], [8000, 2, 500], [15625, 1, 500]])
	data_queue.append([[512, 2, 500], [1000, 11, 500], [2197, 5, 500], [4096, 2, 500], [8000, 3, 500], [15625, 1, 500]])

	
	tiempo_inicial = time()
	consumer_list = []
	nTimesPerBull = ncpus / 4 #4 machines in this example
	
	logger.info(data_queue)
	#This part is also given implicitly, but should be customized 
	consumer10 = Process(target=gpu_consumer_task, args=(data_queue[0], data_index, semaphore, results_dict, "bullxual01", 0))
	consumer10.start()
	consumer_list.append(consumer10)
	
	consumer20 = Process(target=gpu_consumer_task, args=(data_queue[2], data_index, semaphore, results_dict, "bullxual02", 0))
	consumer20.start()
	consumer_list.append(consumer20)
			
	consumer30 = Process(target=gpu_consumer_task, args=(data_queue[4], data_index, semaphore, results_dict, "bullxual03", 0))
	consumer30.start()
	consumer_list.append(consumer30)

	consumer40 = Process(target=gpu_consumer_task, args=(data_queue[6], data_index, semaphore, results_dict, "bullxual04", 0))
	consumer40.start()
	consumer_list.append(consumer40)
	
	consumer11 = Process(target=consumer_task, args=(data_queue[1], data_index, semaphore, results_dict, "bullxual01", 1))
	consumer11.start()
	consumer_list.append(consumer11)

	consumer21 = Process(target=consumer_task, args=(data_queue[3], data_index, semaphore, results_dict, "bullxual02", 1))
	consumer21.start()
	consumer_list.append(consumer21)

	consumer31 = Process(target=consumer_task, args=(data_queue[5], data_index, semaphore, results_dict, "bullxual03", 1))
	consumer31.start()
	consumer_list.append(consumer31)

	consumer41 = Process(target=consumer_task, args=(data_queue[7], data_index, semaphore, results_dict, "bullxual04", 1))
	consumer41.start()
	consumer_list.append(consumer41)

	for j in range(nTimesPerBull):
		consumerS1 = Process(target=cpu_consumer_task, args=(data_queue[8 + j*4], data_index, semaphore, results_dict, "bullxual01", 15 - j))
		consumerS1.start()
		consumer_list.append(consumerS1)

		consumerS2 = Process(target=cpu_consumer_task, args=(data_queue[9 + j*4], data_index, semaphore, results_dict, "bullxual02", 15 - j))
		consumerS2.start()
		consumer_list.append(consumerS2)

		consumerS3 = Process(target=cpu_consumer_task, args=(data_queue[10 + j*4], data_index, semaphore, results_dict, "bullxual03", 15 - j))
		consumerS3.start()
		consumer_list.append(consumerS3)

		consumerS4 = Process(target=cpu_consumer_task, args=(data_queue[11 + j*4], data_index, semaphore, results_dict, "bullxual04", 15 - j))
		consumerS4.start()
		consumer_list.append(consumerS4)

	[consumer.join() for consumer in consumer_list]

	tiempo_final = time()
	tiempo_ejecucion = tiempo_final - tiempo_inicial
	logger.info(results_dict)
	
	print 'Final time: ',tiempo_ejecucion
	with open("final.txt", mode='a') as file:
    		file.write('Final time:  %s.\n' % (tiempo_ejecucion,))
