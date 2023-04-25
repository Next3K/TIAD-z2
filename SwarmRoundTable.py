from typing import List

from ParticleSwarm import ParticleSwarm


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
