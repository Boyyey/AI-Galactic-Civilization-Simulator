import random
import numpy as np

class CivilizationAI:
    """
    Handles adaptive behavior and learning for civilizations.
    Includes stubs for RL, evolutionary algorithms, and trait mutation.
    """
    def __init__(self, civilization):
        self.civilization = civilization
        self.memory = []  # Stores past actions and outcomes
        self.strategy = 'expand'  # Default strategy

    def choose_strategy(self, context):
        """
        Decide on expansion, diplomacy, or war based on context.
        Uses a weighted random choice based on civilization traits and past outcomes.
        """
        aggression = self.civilization.traits.get('aggression', 0.5)
        curiosity = self.civilization.traits.get('curiosity', 0.5)
        risk = self.civilization.traits.get('risk_tolerance', 0.5)
        weights = [aggression, curiosity, risk, 1 - aggression]
        strategies = ['war', 'expand', 'trade', 'isolate']
        chosen = random.choices(strategies, weights=weights, k=1)[0]
        self.strategy = chosen
        self.memory.append((context, chosen))
        return chosen

    def mutate_traits(self):
        """
        Mutate civilization traits for evolutionary simulation.
        Traits can drift slightly or mutate more strongly if the civilization is in crisis.
        """
        for trait in self.civilization.traits:
            mutation_strength = 0.05
            if self.civilization.status == 'collapsed':
                mutation_strength = 0.2
            if random.random() < 0.1:
                self.civilization.traits[trait] += random.uniform(-mutation_strength, mutation_strength)
                self.civilization.traits[trait] = min(max(self.civilization.traits[trait], 0), 1)

    def learn_from_outcome(self, outcome):
        """
        Update strategy based on simulation outcome (stub).
        Could use Q-learning or evolutionary fitness in future.
        """
        self.memory.append(('outcome', outcome))
        # Placeholder: if outcome is bad, shift away from last strategy
        if outcome == 'collapse' and self.memory:
            last_context, last_strategy = self.memory[-2] if len(self.memory) > 1 else (None, None)
            if last_strategy == 'war':
                self.civilization.traits['aggression'] = max(0, self.civilization.traits['aggression'] - 0.1)
            elif last_strategy == 'expand':
                self.civilization.traits['curiosity'] = max(0, self.civilization.traits['curiosity'] - 0.1)

    def evolutionary_algorithm(self, population):
        """
        Evolve a population of civilizations using selection, crossover, and mutation.
        Placeholder for future expansion.
        """
        # Select top civilizations by population
        sorted_pop = sorted(population, key=lambda c: c.population, reverse=True)
        survivors = sorted_pop[:max(1, len(population)//2)]
        # Crossover traits
        children = []
        for _ in range(len(population) - len(survivors)):
            parents = random.sample(survivors, 2)
            child_traits = {k: random.choice([parents[0].traits[k], parents[1].traits[k]]) for k in parents[0].traits}
            child = type(parents[0])(len(population)+len(children), parents[0].home_planet, child_traits)
            children.append(child)
        # Mutate children
        for child in children:
            for trait in child.traits:
                if random.random() < 0.2:
                    child.traits[trait] += random.uniform(-0.1, 0.1)
                    child.traits[trait] = min(max(child.traits[trait], 0), 1)
        return survivors + children

    def q_learning_update(self, state, action, reward, next_state):
        """
        Placeholder for Q-learning update. In a real implementation, would update Q-table or neural net.
        """
        pass

    def policy(self, state):
        """
        Placeholder for policy function. Would select action based on learned Q-values or policy network.
        """
        return self.choose_strategy(state)

# Example usage:
# ai = CivilizationAI(civ)
# action = ai.choose_strategy(context)
# ai.learn_from_outcome('collapse') 