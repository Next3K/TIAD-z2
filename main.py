from Algorithm import Algorithm
from Conductor import Conductor
from ParticleSwarm import ParticleSwarm
import functions
from StopCriterion import StopCriterion
from functions import print_chart

if __name__ == '__main__':
    print('Program is starting!')

    # choose function
    function = functions.Sphere()

    # stop criterion - iterations
    stop_criterion_iterations = StopCriterion("iterations")
    stop_criterion_delta = StopCriterion("delta")

    # PSO parameters
    swarm_size: int = 100
    inertion: float = 0.8
    social_constant: float = 1.2
    cognitive_constant: float = 1.2

    # setup algorithm
    algorithm_pso: Algorithm = ParticleSwarm(stop_criterion_iterations,
                                             swarm_size,
                                             inertion,
                                             social_constant,
                                             cognitive_constant)

    count: int = 0

    conductor_pso = Conductor(30, algorithm_pso, function)
    print("PSO algorithm:")
    print(
        f"Best solution: {conductor_pso.best_solution},"
        f" avg solution: {conductor_pso.average_solution},"
        f" part success: {conductor_pso.part_successful},"
        f" standard deviation: {conductor_pso.standard_deviation}")

    print_chart(conductor_pso.trace_list, "PSO")

