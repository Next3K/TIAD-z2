from Algorithm import Algorithm
from Conductor import Conductor
from Multipso import Multipso
from ParticleSwarm import ParticleSwarm
import functions
from StopCriterion import StopCriterion
from functions import print_chart

if __name__ == '__main__':
    print('Program execution has started!')

    # choose functions
    functions = [functions.Sphere(),
                 functions.Ackley(),
                 functions.Easom(),
                 functions.Brown(),
                 functions.Griewank()]

    # stop criterion - iterations
    stop_criterion_iterations = StopCriterion("iterations")
    stop_criterion_delta = StopCriterion("delta")

    # Multi PSO parameters
    number_of_swarms: int = 5
    swarm_size: int = 100

    # PSO parameters
    inertion: float = 0.8
    social_constant: float = 1.2
    cognitive_constant: float = 1.2

    # setup algorithms
    algorithm_epso: Algorithm = Multipso(stop_criterion_iterations,
                                         sub_swarms=number_of_swarms,
                                         swarm_size=swarm_size,
                                         algorithm_type="elite")

    algorithm_opso: Algorithm = Multipso(stop_criterion_iterations,
                                         sub_swarms=number_of_swarms,
                                         swarm_size=swarm_size,
                                         algorithm_type="osmosis")

    # conduct experiments for all functions
    for function in functions:
        conductor_epso = Conductor(30, algorithm_epso, function)
        conductor_opso = Conductor(30, algorithm_opso, function)

        print(f"EPSO algorithm results for function {function.__class__}:")
        print(
            f"Best solution: {conductor_epso.best_solution},"
            f" avg solution: {conductor_epso.average_solution},"
            f" part success: {conductor_epso.part_successful},"
            f" standard deviation: {conductor_epso.standard_deviation}")

        print(f"OPSO algorithm results for function {function.__class__}:")
        print(
            f"Best solution: {conductor_opso.best_solution},"
            f" avg solution: {conductor_opso.average_solution},"
            f" part success: {conductor_opso.part_successful},"
            f" standard deviation: {conductor_opso.standard_deviation}")

        print_chart(conductor_opso.trace_list, "OPSO")
        print_chart(conductor_epso.trace_list, "EPSO")
