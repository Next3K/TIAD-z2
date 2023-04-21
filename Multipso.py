import math
from typing import List

from Algorithm import Algorithm
from ParticleSwarm import ParticleSwarm
from StopCriterion import StopCriterion
from functions import Equation


class Multipso(Algorithm):

    def find_solution(self, function: Equation) -> (float, [[float]]):
        iteration: int = 0
        global_solution: float = math.inf
        trace: [[float]] = []
        while not self.stop_criterion.should_stop(iteration=iteration, solution=global_solution):
            # add scores to the trace
            trace.append(self.swarms.get_all_scores())
            global_solution = min(global_solution, min(self.swarms.get_all_scores()))

            # perform iteration
            self.swarms.next_iteration()

            # particle migration
            for i in range(self.swarms.size()):
                swarm_one = self.swarms.get_swarm(i)
                swarm_two = self.swarms.get_swarm(self.swarms.get_right_index(i))
                self.migrate(swarm_one, swarm_two)

            # update iteration count and global solution
            iteration += 1

        return global_solution, trace

    def __init__(self,
                 stop_criterion: StopCriterion,
                 sub_swarms: int,
                 swarm_size: int,
                 algorithm_type: str,
                 ):
        super().__init__(stop_criterion)

        if algorithm_type not in {"elite", "osmosis"}:
            raise ValueError(f"Type of algorithm should be one of: \"elite\", \"osmosis\" but is f{algorithm_type}")

        self.algorithm_type: str = algorithm_type
        self.swarms: SwarmRoundTable = SwarmRoundTable(
            [ParticleSwarm(stop_criterion=stop_criterion,
                           swarm_size=swarm_size,
                           inertion=0.2,
                           social_constant=0.45,
                           cognitive_constant=0.35) for _ in range(sub_swarms)])

    def migrate(self, swarm_one: ParticleSwarm, swarm_two: ParticleSwarm):
        if self.algorithm_type == "elite":
            # particle exchange using elite method
            # do binary insertion since list is sorted
            pass
        elif self.algorithm_type == "osmosis":
            score_one = swarm_one.particles[0].current_score
            score_two = swarm_two.particles[0].current_score
            diff = abs(score_one - score_two)
            if diff > 0.5:

                # particle exchange using osmosis method
                # do binary insertion since list is sorted
                migration_rate: float = 0.4
            pass
        else:
            raise ValueError("wrong choice error")


class SwarmRoundTable:

    def __init__(self, swarms: List[ParticleSwarm]):
        self.swarms: List[ParticleSwarm] = swarms

    def get_left_index(self, swarm_index: int) -> int:
        return swarm_index - 1 if swarm_index - 1 >= 0 else 0

    def get_right_index(self, swarm_index: int) -> int:
        return swarm_index + 1 if swarm_index + 1 <= len(self.swarms) - 1 else 0

    def get_swarm(self, index: int):
        return self.swarms[index]

    def size(self) -> int:
        return len(self.swarms)

    def get_all_scores(self):
        scores: [float] = []
        for swarm in self.swarms:
            scores.extend([particle.current_score for particle in swarm.particles])
        return scores

    def next_iteration(self):
        for swarm in self.swarms:
            swarm.run_iteration()

