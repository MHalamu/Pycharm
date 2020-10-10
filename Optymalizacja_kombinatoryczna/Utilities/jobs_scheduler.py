class JobsScheduler(object):
    def __init__(self, schedule_algorithm):
        self.schedule_algorithm = schedule_algorithm

    def schedule_jobs(self):
        self.schedule_algorithm.schedule_jobs()

    def get_cmax(self):
        return self.schedule_algorithm.get_cmax()

    def get_machines(self):
        return self.schedule_algorithm.machines_dict
