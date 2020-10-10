from abc import ABCMeta, abstractmethod
from copy import deepcopy


class AbstractScheduleAlgorithm(object):
    __metaclass__ = ABCMeta

    def __init__(self, no_of_machines, jobs_duration_list):
        self.jobs_duration_list = deepcopy(jobs_duration_list)
        self.no_of_machines = no_of_machines
        self.cmax = 0
        self.machines_dict = {}

    @abstractmethod
    def schedule_jobs(self):
        pass

    def get_cmax(self):
        return self.cmax