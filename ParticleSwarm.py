import math
import random
from typing import List

from Algorithm import Algorithm
from StopCriterion import StopCriterion
from functions import Equation
from particle import Particle


class ParticleSwarm:

    def __init__(self,
                 stop_criterion: StopCriterion,
                 swarm_size: int = 80,
                 inertion: float = 0.2,
                 social_constant: float = 0.45,
                 cognitive_constant: float = 0.35):

        super().__init__(stop_criterion)
        self.swarm_size = swarm_size
        self.inertion = inertion
        self.social_constant = social_constant
        self.cognitive_constant = cognitive_constant

        # setup for current experiment
        self.global_solution = None
        self.particles: List[Particle] = []
        self.current_iteration = 0
        self.equation = None

    def set_function_to_optimize(self, equation: Equation):
        # self.global_solution = math.inf
        self.equation = equation
        self.particles: [Particle] = [Particle(equation.min, equation.max, equation.dimensions)
                                      for _ in range(self.swarm_size)]

    # return sorted particles and their scores
    def run_iteration(self):

        # calculate scores
        for particle in self.particles:
            calculated_score = self.equation.calculate(particle.position)
            particle.update_score(calculated_score)

        # sort particles by their score
        self.particles.sort(key=lambda x: x.current_score)

        current_best_position = self.particles[0].position

        # update particle velocities
        for particle in self.particles:
            for dim in range(len(particle.position)):
                inertion_component = self.inertion * particle.velocity[dim]
                cognitive_component = self.cognitive_constant * random.uniform(0, 1) * (
                        particle.particle_best_positions[dim] - particle.position[dim])
                social_component = self.social_constant * random.uniform(0, 1) * (
                        current_best_position[dim] - particle.position[dim])
                particle.velocity[dim] = inertion_component + cognitive_component + social_component

        # update particle positions
        for particle in self.particles:
            particle.update_positions()

        # increase current iteration
        self.current_iteration += 1
