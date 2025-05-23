import math

from Algorithm import Algorithm
from ParticleSwarm import ParticleSwarm, ParticleSwarmElite
from StopCriterion import StopCriterion
from SwarmRoundTable import SwarmRoundTable
from functions import Equation
from MigrationMethod import MigrationMethod, OsmosisMigration, EliteMigration


class Multipso(Algorithm):

    def find_solution(self) -> (float, [[float]]):
        iteration: int = 0
        global_solution: float = math.inf
        trace: [[float]] = []
        while not self.stop_criterion.should_stop(iteration=iteration, solution=global_solution):
            # perform iteration
            self.swarms.next_iteration()

            # add scores to the trace
            trace.append(self.swarms.get_all_scores())
            global_solution = min(global_solution, min(self.swarms.get_all_scores()))

            # particle migration
            self.migration_method.migrate(self.swarms)

            # update iteration count and global solution
            iteration += 1

        return global_solution, trace

    def __init__(self,
                 stop_criterion: StopCriterion,
                 equation: Equation,
                 sub_swarms: int,
                 swarm_size: int,
                 algorithm_type: str,
                 ):
        super().__init__(stop_criterion)

        if algorithm_type not in {"elite", "osmosis"}:
            raise ValueError(f"Type of algorithm should be one of: \"elite\", \"osmosis\" but is f{algorithm_type}")

        self.migration_method: MigrationMethod = OsmosisMigration() \
            if algorithm_type == "osmosis" else EliteMigration()

        if algorithm_type == "osmosis":
            self.swarms: SwarmRoundTable = SwarmRoundTable(
                [ParticleSwarm(stop_criterion=stop_criterion,
                               equation=equation,
                               swarm_size=swarm_size,
                               inertion=0.2,
                               social_constant=0.45,
                               cognitive_constant=0.35) for _ in range(sub_swarms)])
        elif algorithm_type == "elite":
            self.swarms: SwarmRoundTable = SwarmRoundTable(
                [ParticleSwarmElite(stop_criterion=stop_criterion,
                                    equation=equation,
                                    swarm_size=swarm_size,
                                    inertion=0.2,
                                    social_constant=0.45,
                                    cognitive_constant=0.35) for _ in range(sub_swarms)])
        else:
            raise ValueError("Bad choice")
