from Algorithm import Algorithm
from statistics import mean, stdev
import math

from Multipso import Multipso
from StopCriterion import StopCriterion
from functions import Equation


class Conductor:
    def __init__(self,
                 number_of_runs: int,
                 algorithm_type: str,
                 function: Equation,
                 stop_criterion: StopCriterion,
                 number_of_swarms: int,
                 swarm_size: int):

        self.solutions: [float] = []
        self.best_solution = math.inf
        self.trace_list: [[float]] = None
        self.number_of_runs: int = number_of_runs
        self.algorithm_type: str = algorithm_type
        self.function: Equation = function
        self.stop_criterion: StopCriterion = stop_criterion
        self.number_of_swarms: int = number_of_swarms
        self.swarm_size: int = swarm_size

        # conduct experiments
        for i in range(number_of_runs):
            algorithm = Multipso(stop_criterion=self.stop_criterion,
                                 sub_swarms=self.number_of_swarms,
                                 swarm_size=self.swarm_size,
                                 algorithm_type=self.algorithm_type,
                                 equation=self.function)
            solution, trace_list = algorithm.find_solution()
            print(f"conducted experiment for algo: {algorithm_type}")
            if solution is not None and solution is not -math.inf and solution is not math.inf:
                self.solutions.append(solution)
                if solution < self.best_solution:
                    self.best_solution = solution
                    self.trace_list = trace_list

        self.average_solution = mean(self.solutions)
        self.standard_deviation = stdev(self.solutions)
        self.part_successful = len(self.solutions) / number_of_runs
