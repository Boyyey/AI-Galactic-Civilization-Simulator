import numpy as np
import random
from galaxy import Galaxy
from agents import Civilization
from utils import distance

class TechTree:
    """
    Represents a simple technology tree for civilizations.
    """
    def __init__(self):
        self.technologies = [
            'Agriculture', 'Metallurgy', 'Spaceflight', 'Fusion Power',
            'AI', 'FTL Communication', 'Terraforming', 'Dyson Spheres'
        ]
        self.prereqs = {
            'Metallurgy': ['Agriculture'],
            'Spaceflight': ['Metallurgy'],
            'Fusion Power': ['Spaceflight'],
            'AI': ['Fusion Power'],
            'FTL Communication': ['AI'],
            'Terraforming': ['Fusion Power'],
            'Dyson Spheres': ['Fusion Power', 'AI']
        }

    def available(self, civ):
        """Return list of technologies available to research."""
        owned = set(civ.techs)
        return [tech for tech in self.technologies if tech not in owned and all(p in owned for p in self.prereqs.get(tech, []))]

class TradeRoute:
    """
    Represents a trade route between two civilizations.
    """
    def __init__(self, civ1, civ2, resource_type, volume):
        self.civ1 = civ1
        self.civ2 = civ2
        self.resource_type = resource_type
        self.volume = volume
        self.active = True

class Diplomacy:
    """
    Handles diplomatic relations between civilizations.
    """
    def __init__(self, civs):
        self.relations = {(a.id, b.id): 0 for a in civs for b in civs if a.id != b.id}
        # 0 = neutral, positive = friendly, negative = hostile

    def update(self, civ1, civ2, delta):
        key = (civ1.id, civ2.id)
        if key in self.relations:
            self.relations[key] += delta

    def get(self, civ1, civ2):
        return self.relations.get((civ1.id, civ2.id), 0)

class War:
    """
    Handles war between civilizations.
    """
    def __init__(self):
        self.active_wars = []  # List of (civ1, civ2)

    def declare(self, civ1, civ2):
        self.active_wars.append((civ1, civ2))
        civ1.history.append(f"Declared war on Civ {civ2.id}")
        civ2.history.append(f"Was attacked by Civ {civ1.id}")

    def resolve(self, civ1, civ2):
        # Simple resolution: higher tech or population wins
        winner = civ1 if civ1.tech_level + civ1.population > civ2.tech_level + civ2.population else civ2
        loser = civ2 if winner is civ1 else civ1
        loser.collapse('defeated in war')
        winner.history.append(f"Defeated Civ {loser.id} in war")
        self.active_wars.remove((civ1, civ2))

class CommunicationLag:
    """
    Models communication lag between civilizations (in years).
    """
    def __init__(self, galaxy, c=1):
        self.galaxy = galaxy
        self.c = c  # speed of light in ly/year

    def lag(self, civ1, civ2):
        pos1 = civ1.home_planet.star.position
        pos2 = civ2.home_planet.star.position
        return distance(pos1, pos2) / self.c

class Simulation:
    """
    Manages the simulation of the galaxy and civilizations.
    Handles seeding, time steps, and statistics.
    Now includes tech tree, trade, diplomacy, war, and communication lag.
    """
    def __init__(self, n_stars=1000, n_civs=10, seed=42):
        self.galaxy = Galaxy(n_stars=n_stars, seed=seed)
        self.n_civs = n_civs
        self.seed = seed
        self.stats_history = []
        self.tech_tree = TechTree()
        self.trade_routes = []
        self.diplomacy = Diplomacy(self.galaxy.civilizations)
        self.war = War()
        self.comms = CommunicationLag(self.galaxy)
        self.seed_civilizations()

    def seed_civilizations(self):
        civ_id = 0
        candidates = [p for p in self.galaxy.planets if p.has_intelligent_life]
        random.shuffle(candidates)
        for planet in candidates[:self.n_civs]:
            traits = {
                'aggression': np.random.uniform(0, 1),
                'curiosity': np.random.uniform(0, 1),
                'risk_tolerance': np.random.uniform(0, 1)
            }
            civ = Civilization(civ_id, planet, traits)
            civ.techs = ['Agriculture']
            planet.civilization = civ
            self.galaxy.civilizations.append(civ)
            civ_id += 1

    def step(self):
        # Each civilization grows, expands, or collapses
        for civ in self.galaxy.civilizations:
            if civ.status == 'alive':
                civ.grow()
                civ.expand(self.galaxy)
                self.handle_tech(civ)
                self.handle_trade(civ)
                self.handle_diplomacy(civ)
                self.handle_war(civ)
        self.stats_history.append(self.stats())

    def handle_tech(self, civ):
        # Research available tech if possible
        available = self.tech_tree.available(civ)
        if available and random.random() < 0.2:
            tech = random.choice(available)
            civ.techs.append(tech)
            civ.tech_level += 1
            civ.history.append(f"Researched {tech}")

    def handle_trade(self, civ):
        # Simple: trade with a random neighbor if friendly
        for other in self.galaxy.civilizations:
            if other is not civ and other.status == 'alive':
                if self.diplomacy.get(civ, other) > 0 and self.comms.lag(civ, other) < 50:
                    if random.random() < 0.05:
                        route = TradeRoute(civ, other, 'resources', random.randint(100, 1000))
                        self.trade_routes.append(route)
                        civ.history.append(f"Started trade with Civ {other.id}")
                        other.history.append(f"Started trade with Civ {civ.id}")

    def handle_diplomacy(self, civ):
        # Randomly improve or worsen relations
        for other in self.galaxy.civilizations:
            if other is not civ and other.status == 'alive':
                delta = random.choice([-1, 0, 1])
                self.diplomacy.update(civ, other, delta)

    def handle_war(self, civ):
        # If relations are very bad, declare war
        for other in self.galaxy.civilizations:
            if other is not civ and other.status == 'alive':
                if self.diplomacy.get(civ, other) < -5 and (civ, other) not in self.war.active_wars:
                    self.war.declare(civ, other)
                # Resolve war if active
                if (civ, other) in self.war.active_wars:
                    if random.random() < 0.1:
                        self.war.resolve(civ, other)

    def run(self, steps=100):
        for t in range(steps):
            self.step()
        return self.stats_history

    def stats(self):
        alive = sum(1 for c in self.galaxy.civilizations if c.status == 'alive')
        total_pop = sum(c.population for c in self.galaxy.civilizations if c.status == 'alive')
        avg_tech = np.mean([c.tech_level for c in self.galaxy.civilizations if c.status == 'alive']) if alive else 0
        return {'alive_civs': alive, 'total_population': total_pop, 'avg_tech': avg_tech} 