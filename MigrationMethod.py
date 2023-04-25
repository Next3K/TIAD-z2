import bisect
from abc import abstractmethod
from math import floor
from random import random
from typing import List

import numpy as np

from ParticleSwarm import ParticleSwarm
from SwarmRoundTable import SwarmRoundTable
from particle import Particle


class MigrationMethod:

    @abstractmethod
    def migrate(self, round_table: SwarmRoundTable):
        pass


class OsmosisMigration(MigrationMethod):

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def migrate(self, round_table: SwarmRoundTable):
        for i in range(round_table.size()):
            swarm_one = round_table.get_swarm(i)
            swarm_two = round_table.get_swarm(round_table.get_right_index(i))
            self.pair_migrate(swarm_one, swarm_two)

    def pair_migrate(self, swarm_one: ParticleSwarm, swarm_two: ParticleSwarm):

        assert len(swarm_two.particles) == len(swarm_one.particles)
        n = len(swarm_one.particles)

        score_one = swarm_one.particles[0].current_score
        score_two = swarm_two.particles[0].current_score
        diff = abs(score_one - score_two)
        smaller, bigger = (swarm_one.particles, swarm_two.particles) \
            if score_one < score_two else (swarm_two.particles, swarm_one.particles)
        if diff > self.threshold:
            migration_rate = diff / max(score_one, score_two)
            number_of_migrating: int = floor(migration_rate * n)

            # get particles to migrate
            bigger_to_migrate = bigger[:number_of_migrating]
            smaller_to_migrate = smaller[n - number_of_migrating:]

            bigger = bigger[number_of_migrating:]
            smaller = smaller[:n - number_of_migrating]

            # put weak particles into better swarm
            for big in bigger_to_migrate:
                bisect.insort(smaller, big)

            # put strong particles into weaker swarm
            for small in smaller_to_migrate:
                bisect.insort(bigger, small)


class EliteMigration(MigrationMethod):

    def __init__(self, param: float = 0.5):
        self.param = param

    def migrate(self, round_table: SwarmRoundTable):
        elite_particles: List[Particle] = []
        for particle_swarm in round_table.swarms:
            elite_particles.append(particle_swarm.particles[0])

        dim = len(elite_particles[0].position)
        for i in range(len(elite_particles)):
            mean_position = []
            for j in range(dim):
                mean_position.append(np.mean([p.position[j] for p in elite_particles if p != elite_particles[i]]))

            new_coords = []
            for dimension in range(dim):
                new_coords.append(mean_position[dim] * (1 + random.gauss(0.0, 1.0)))
            elite_particles[i].update_positions_with_coords(new_coords=new_coords)
