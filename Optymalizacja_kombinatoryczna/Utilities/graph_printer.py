def print_graph(machines):

    sorted_names = sorted(machines.keys(), key=lambda name: int(name.strip("M")))
    for machine_name in sorted_names:
        report_for_machine_final = ""
        total_length = sum(machines[machine_name])
        for duration in machines[machine_name]:
            report_for_machine = "-" * duration
            report_for_machine_final += report_for_machine + "|"
        print machine_name + " |" + report_for_machine_final + "   %s j" % total_length
