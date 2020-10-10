from Algorithms.spt_algorithm import SptAlgorithm
from Algorithms.lpt_algorithm import LptAlgorithm
from Algorithms.genetic_algorithm import GeneticAlgorythm
from Utilities.jobs_scheduler import JobsScheduler
from Utilities.graph_printer import print_graph
from Utilities.instance_provider import open_instance_file
import time


# Genetic Algorithm stop criteria.
# After that many loops without Cmax change, algorithm will stop.
GA_MAX_CYCLES = 2000

GA_POPULATION_SIZE = 200
GA_MUTATION_CHANCE_RANGE = (0, 10)

# Instance from file
jobs_duration_list, no_of_machines = open_instance_file('m20.txt')

# Random instance
# jobs_duration_list, no_of_machines = get_random_instance(
#     job_times_range=[10, 40],
#     no_of_jobs_range=[30, 50],
#     no_of_machines_range=[5, 10])

print "Number of machines: %s" % no_of_machines
print "Number of jobs: %s" % len(jobs_duration_list)
print "Jobs duration list: %s" % jobs_duration_list


# --------------------------- SPT -----------------------------------------
timestamp_list = [time.time()]
spt_alg_scheduler = JobsScheduler(
    schedule_algorithm=SptAlgorithm(jobs_duration_list=jobs_duration_list,
                                    no_of_machines=no_of_machines))

spt_alg_scheduler.schedule_jobs()
timestamp_list.append(time.time())
print "\n\nSPT"
print "Cmax: %s" % spt_alg_scheduler.get_cmax()
print "Calculation time: %ss" % (timestamp_list[1] - timestamp_list[0])

print_graph(spt_alg_scheduler.get_machines())
# -------------------------------------------------------------------------

# ---------------------------- LPT ----------------------------------------
timestamp_list = [time.time()]
lpt_alg_scheduler = JobsScheduler(
    schedule_algorithm=LptAlgorithm(jobs_duration_list=jobs_duration_list,
                                    no_of_machines=no_of_machines))

lpt_alg_scheduler.schedule_jobs()
timestamp_list.append(time.time())
print "\n\nLPT"
print "Cmax: %s" % lpt_alg_scheduler.get_cmax()
print "Calculation time: %ss" % (timestamp_list[1] - timestamp_list[0])

print_graph(lpt_alg_scheduler.get_machines())
# -------------------------------------------------------------------------

# ----------------------- Genetic algorithm -------------------------------
genetic_alg_scheduler = JobsScheduler(
    schedule_algorithm=GeneticAlgorythm(jobs_duration_list=jobs_duration_list,
                                        no_of_machines=no_of_machines))
genetic_alg_scheduler.schedule_algorithm.configure(
    population_size=GA_POPULATION_SIZE,
    stop_criteria_cycles=GA_MAX_CYCLES,
    mutation_chance_range_prc=GA_MUTATION_CHANCE_RANGE)

print "\n\nGenetic algorithm"
genetic_alg_scheduler.schedule_jobs()
print "\n\nBest Cmax: %s" % genetic_alg_scheduler.get_cmax()
# -------------------------------------------------------------------------
