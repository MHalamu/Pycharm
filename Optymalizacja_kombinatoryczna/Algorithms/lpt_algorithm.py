from Optymalizacja_kombinatoryczna.Utilities.cmax_calculator import CmaxCalculator
from Optymalizacja_kombinatoryczna.Algorithms.algorithm_interface import AbstractScheduleAlgorithm


class LptAlgorithm(AbstractScheduleAlgorithm):

    def __init__(self, no_of_machines, jobs_duration_list):
        super(LptAlgorithm, self).__init__(no_of_machines, jobs_duration_list)

    def schedule_jobs(self):
        self.jobs_duration_list.sort(reverse=True)
        self.machines_dict = CmaxCalculator.put_jobs_to_machines(self.jobs_duration_list, self.no_of_machines)
        self.cmax = CmaxCalculator.calculate_cmax(self.machines_dict)
