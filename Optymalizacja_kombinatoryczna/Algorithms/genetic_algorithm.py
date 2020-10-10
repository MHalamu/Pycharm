from Optymalizacja_kombinatoryczna.Algorithms.algorithm_interface import AbstractScheduleAlgorithm
from Optymalizacja_kombinatoryczna.Utilities.cmax_calculator import CmaxCalculator
from Optymalizacja_kombinatoryczna.Utilities.graph_printer import print_graph
from random import randint, shuffle
from copy import deepcopy
import sys
import time
import math


class Population(object):
    """Population object represents set of individuals.

    An individual is an object that represents all jobs for scheduling.
    """
    def __init__(self, size, jobs_duration_list, no_of_machines):
        self.size = size
        self.jobs_duration_list = jobs_duration_list
        self.individuals_list = []
        self.no_of_machines = no_of_machines

    def generate_random_individuals(self):
        """Generate random individuals based on provided list of jobs."""
        for individual_no in xrange(self.size):
            jobs_duration_list = deepcopy(self.jobs_duration_list)
            shuffle(jobs_duration_list)
            self.individuals_list.append(
                Individual(jobs_duration_list=jobs_duration_list,
                           no_of_machines=self.no_of_machines))

    def add_individual(self, individual):
        self.individuals_list.append(individual)

    def calculate_fitness(self):
        for individual in self.individuals_list:
            individual.calculate_fitness()

    def get_fittest(self):
        return sorted(self.individuals_list, key=lambda individual: individual.fitness_score)

    def get_shortest_durations(self):
        return sorted(self.individuals_list, key=lambda individual: individual.jobs_duration_list)

    def tune(self):
        for individual in self.individuals_list:
            individual.tune()

    def create_new_population(self, fittest_list, mutation_chance_range_prc, no_of_pairs_for_crossover=4):
        new_population = fittest_list[:no_of_pairs_for_crossover * 2]
        while len(new_population) < self.size:
            for parent_no in xrange(0, no_of_pairs_for_crossover*2, 2):
                offspring1 = fittest_list[parent_no].crossover(fittest_list[parent_no + 1])
                offspring1.mutate(mutation_chance_range_prc)
                offspring2 = fittest_list[parent_no + 1].crossover(fittest_list[parent_no])
                offspring2.mutate(mutation_chance_range_prc)

                new_population.append(offspring1)
                new_population.append(offspring2)

        while len(new_population) > self.size:
            new_population.pop()

        return new_population


class Individual(object):
    """Individual represents an object with chromosome."""

    def __init__(self, jobs_duration_list, no_of_machines):
        self.jobs_duration_list = jobs_duration_list
        self.fitness_score = sys.maxint
        self.no_of_machines = no_of_machines
        self.machine_dict = {}

    def get_longest_machine(self):
        return max(self.machine_dict, key=lambda machine: sum(self.machine_dict[machine]))

    def get_shortest_machine(self):
        return min(self.machine_dict, key=lambda machine: sum(self.machine_dict[machine]))

    def calculate_fitness(self):
        self.machine_dict = CmaxCalculator.put_jobs_to_machines(self.jobs_duration_list, self.no_of_machines)
        self.fitness_score = CmaxCalculator.calculate_cmax(self.machine_dict)

    def crossover(self, parent):
        """Perform LOX Crossover."""

        # Get random points between which data from parent will be passes to offspring.
        point1 = randint(0, len(self.jobs_duration_list) - 1)
        point2 = randint(point1, len(self.jobs_duration_list) - 1)

        offsprint_jobs_duration_list = self.jobs_duration_list[point1:point2 + 1]
        parent2_jobs_duration_list_copy = deepcopy(parent.jobs_duration_list)

        # In parent 2 remove jobs that were already transferred to offspring from parent1.
        [parent2_jobs_duration_list_copy.remove(duration) for duration in offsprint_jobs_duration_list]

        offsprint_jobs_duration_list = parent2_jobs_duration_list_copy[:point1] + offsprint_jobs_duration_list
        offsprint_jobs_duration_list = offsprint_jobs_duration_list + parent2_jobs_duration_list_copy[point1:]

        return Individual(offsprint_jobs_duration_list, self.no_of_machines)

    def mutate(self, prc_mutation):
        prc_mutation = randint(prc_mutation[0], prc_mutation[1])
        no_of_genes_for_mutation = int(math.ceil(len(self.jobs_duration_list) * (float(prc_mutation) / 100)))

        for _ in xrange(no_of_genes_for_mutation):
            # Switch genes between random indexes.
            self.jobs_duration_list.insert(
                randint(0, len(self.jobs_duration_list) - 1),
                self.jobs_duration_list.pop(randint(0, len(self.jobs_duration_list) - 1)))

    def _get_machine_with_lowest_taken_jobs(self, indiv, machines_with_taken_jobs):
        lowest = sys.maxint
        lowest_machine = ""
        for machine in indiv.machine_dict:
            result = sum(indiv.machine_dict[machine]) - sum(machines_with_taken_jobs[machine])
            if result < lowest:
                lowest = result
                lowest_machine = machine

        return lowest_machine

    def tune(self):
        machines_copy = deepcopy(self.machine_dict)
        while True:

            current_cmax = self.fitness_score
            longest_machine = self.get_longest_machine()
            shortest_machine = self.get_shortest_machine()

            shortest_job_longest_machine = min(machines_copy[longest_machine])

            machines_copy[longest_machine].remove(shortest_job_longest_machine)
            machines_copy[shortest_machine].append(shortest_job_longest_machine)

            new_cmax = CmaxCalculator.calculate_cmax(machines_copy)

            if new_cmax < current_cmax:
                self.machine_dict = deepcopy(machines_copy)
                self.fitness_score = new_cmax

                new_chromosome = []
                machines_with_taken_jobs = deepcopy(self.machine_dict)
                while True:
                    machine = self._get_machine_with_lowest_taken_jobs(self, machines_with_taken_jobs)
                    try:
                        new_chromosome.append(machines_with_taken_jobs[machine].pop(0))
                    except IndexError:
                        break

                self.jobs_duration_list = new_chromosome

            else:
               break


class GeneticAlgorythm(AbstractScheduleAlgorithm):

    def __init__(self, no_of_machines, jobs_duration_list):
        super(GeneticAlgorythm, self).__init__(no_of_machines, jobs_duration_list)
        self.population_size = 0
        self.stop_criteria_cycles = 0
        self.mutation_chance_range_prc = 0

    def configure(self, population_size, stop_criteria_cycles, mutation_chance_range_prc):
        self.population_size = population_size
        self.stop_criteria_cycles = stop_criteria_cycles
        self.mutation_chance_range_prc = mutation_chance_range_prc

    def schedule_jobs(self):
        population = Population(self.population_size, self.jobs_duration_list, self.no_of_machines)
        population.generate_random_individuals()
        no_of_cycles = 1
        self.cmax = sys.maxint
        no_of_cycles_without_change = 0
        start_time = time.time()

        while no_of_cycles_without_change < self.stop_criteria_cycles:

            population.calculate_fitness()
            population.tune()

            fittest_list = population.get_fittest()
            if fittest_list[0].fitness_score < self.cmax:
                self.cmax = fittest_list[0].fitness_score
                no_of_cycles_without_change = 0
                current_time = time.time()

                print "\nLoop %s" % no_of_cycles
                print "Best cmax: %s" % self.cmax
                print "Time since beginning of measurement: %ss" % (current_time - start_time)
                print_graph(fittest_list[0].machine_dict)

            new_population = population.create_new_population(fittest_list, self.mutation_chance_range_prc)
            population.individuals_list = new_population

            no_of_cycles_without_change += 1
            no_of_cycles += 1
