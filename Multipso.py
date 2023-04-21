from Algorithm import Algorithm
from ParticleSwarm import ParticleSwarm
from StopCriterion import StopCriterion
from functions import Equation


class Multipso(Algorithm):

    def find_solution(self, function: Equation) -> (float, [[float]]):
        iterations: int = 0
        while iterations < 300:
            iterations += 1

        return 0.5, [[0.4, 0.6, 0.3, 0.55]]

    def __init__(self,
                 stop_criterion: StopCriterion,
                 sub_swarms: int,
                 swarm_size: int,
                 algorithm_type: str,
                 ):
        super().__init__(stop_criterion)

        if algorithm_type not in {"elite", "osmosis"}:
            raise ValueError(f"Type of algorithm should be one of: \"elite\", \"osmosis\" but is f{algorithm_type}")

        self.type: str = algorithm_type
        self.sub_swarms: SwarmRoundTable = SwarmRoundTable(
            [ParticleSwarm(stop_criterion=stop_criterion,
                           swarm_size=swarm_size,
                           inertion=0.2,
                           social_constant=0.45,
                           cognitive_constant=0.35) for _ in range(sub_swarms)])


class SwarmRoundTable:

    def __init__(self, swarms: [ParticleSwarm]):
        self.swarms: [ParticleSwarm] = swarms

    def get_left(self, swarm: ParticleSwarm):
        index = self.swarms.index(swarm)
        return index - 1 if index - 1 >= 0 else 0

    def get_right(self, swarm: ParticleSwarm):
        index = self.swarms.index(swarm)
        return index + 1 if index + 1 <= len(self.swarms) - 1 else 0
