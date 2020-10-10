from random import randint


def open_instance_file(path_to_instance):
    with open('instances/' + path_to_instance) as f:
        data_from_file = [int(data) for data in f.read().splitlines()]
        no_of_machines = data_from_file[0]
        jobs_duration_list = data_from_file[2:]

    return jobs_duration_list, no_of_machines


def get_random_instance(job_times_range, no_of_machines_range, no_of_jobs_range):

    no_of_machines = randint(no_of_machines_range[0], no_of_machines_range[1])
    no_of_jobs = randint(no_of_jobs_range[0], no_of_jobs_range[1])

    list_of_jobs = []
    for job in xrange(no_of_jobs):
        list_of_jobs.append(randint(job_times_range[0], job_times_range[1]))

    return list_of_jobs, no_of_machines
