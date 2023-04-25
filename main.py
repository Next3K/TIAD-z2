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
    dimensions: [int] = [20, 50]

    # PSO parameters
    inertion: float = 0.8
    social_constant: float = 1.2
    cognitive_constant: float = 1.2

    # conduct experiments for all functions
    for function in functions:
        for number_of_dimensions in dimensions:

            # set proper number od dimensions
            function.dimensions = number_of_dimensions

            conductor_opso = Conductor(8,
                                       algorithm_type="osmosis",
                                       function=function,
                                       stop_criterion=stop_criterion_iterations,
                                       number_of_swarms=number_of_swarms,
                                       swarm_size=swarm_size)

            conductor_epso = Conductor(8,
                                       algorithm_type="elite",
                                       function=function,
                                       stop_criterion=stop_criterion_iterations,
                                       number_of_swarms=number_of_swarms,
                                       swarm_size=swarm_size)


            print(f"EPSO algorithm results for function {function.__class__} (dimensions: {number_of_dimensions}):")
            print(
                f"Best solution: {conductor_epso.best_solution},"
                f" avg solution: {conductor_epso.average_solution},"
                f" part success: {conductor_epso.part_successful},"
                f" standard deviation: {conductor_epso.standard_deviation}")

            print(f"OPSO algorithm results for function {function.__class__} (dimensions: {number_of_dimensions}):")
            print(
                f"Best solution: {conductor_opso.best_solution},"
                f" avg solution: {conductor_opso.average_solution},"
                f" part success: {conductor_opso.part_successful},"
                f" standard deviation: {conductor_opso.standard_deviation}")

            print_chart(conductor_opso.trace_list, "OPSO")
            print_chart(conductor_epso.trace_list, "EPSO")
