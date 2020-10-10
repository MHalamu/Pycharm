from collections import OrderedDict


class CmaxCalculator(object):

    @staticmethod
    def put_jobs_to_machines(jobs_duration_list, no_of_machines):
        """Put all defined jobs to first free machine."""
        jobs_duration_iter = iter(jobs_duration_list)

        machines_dict = OrderedDict([("M%s" % i, []) for i in xrange(1, no_of_machines + 1)])

        while True:
            machine_with_least_time = min(machines_dict, key=lambda machine: sum(machines_dict[machine]))
            try:
                machines_dict[machine_with_least_time].append(jobs_duration_iter.next())
            except StopIteration:
                break

        return machines_dict

    @staticmethod
    def calculate_cmax(machines_dict):
        """Calculate Cmax out of all machines."""
        return sum(max(machines_dict.values(), key=lambda list_of_values: sum(list_of_values)))