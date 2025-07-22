import random

class Civilization:
    """
    Represents a spacefaring civilization agent.
    Attributes:
        id: Unique identifier
        home_planet: Planet object
        planets: List of colonized Planet objects
        population: Current population
        growth_rate: Population growth rate
        tech_level: Current technology level
        resources: Total resources
        traits: Dict of cultural traits
        government: Type of government
        language: Main language
        religion: Main religion
        economy: Economic system
        status: 'alive' or 'collapsed'
        history: List of events
    """
    GOVERNMENTS = ['democracy', 'monarchy', 'theocracy', 'republic', 'dictatorship', 'anarchy']
    ECONOMIES = ['capitalist', 'socialist', 'mixed', 'planned']
    RELIGIONS = ['none', 'polytheism', 'monotheism', 'animism', 'philosophy']
    LANGUAGES = ['Galactic Basic', 'Proto', 'Lingua', 'Xeno', 'Synth']

    def __init__(self, id, home_planet, traits):
        self.id = id
        self.home_planet = home_planet
        self.planets = [home_planet]
        self.population = random.randint(1_000_000, 10_000_000)
        self.growth_rate = random.uniform(0.01, 0.05)
        self.tech_level = 1
        self.resources = home_planet.resources
        self.traits = traits  # aggression, curiosity, risk_tolerance
        self.government = random.choice(self.GOVERNMENTS)
        self.language = random.choice(self.LANGUAGES)
        self.religion = random.choice(self.RELIGIONS)
        self.economy = random.choice(self.ECONOMIES)
        self.status = 'alive'
        self.history = []

    def grow(self):
        """Simulate population growth and resource consumption."""
        if self.status == 'alive':
            self.population = int(self.population * (1 + self.growth_rate))
            self.resources -= int(self.population * 0.001)
            if self.resources < 0:
                self.collapse('resource depletion')

    def collapse(self, reason):
        """Collapse the civilization for a given reason."""
        self.status = 'collapsed'
        self.history.append(f'Collapsed due to {reason}')

    def expand(self, galaxy):
        """Attempt to colonize a nearby planet with life."""
        if self.status != 'alive':
            return
        for planet in galaxy.get_nearby_planets(self.home_planet, max_distance=20):
            if planet.civilization is None and planet.has_life:
                planet.civilization = self
                self.planets.append(planet)
                self.resources += planet.resources
                self.history.append(f'Colonized planet {planet.id}')
                break

    def reform_government(self, new_gov):
        """Change the government type."""
        self.government = new_gov
        self.history.append(f'Reformed government to {new_gov}')

    def cultural_change(self, trait, delta):
        """Change a cultural trait by delta."""
        if trait in self.traits:
            self.traits[trait] = min(max(self.traits[trait] + delta, 0), 1)
            self.history.append(f'Cultural trait {trait} changed by {delta}')

    def revolution(self):
        """Simulate a revolution: randomize government, economy, and possibly religion."""
        old_gov = self.government
        old_econ = self.economy
        self.government = random.choice(self.GOVERNMENTS)
        self.economy = random.choice(self.ECONOMIES)
        if random.random() < 0.5:
            self.religion = random.choice(self.RELIGIONS)
        self.history.append(f'Revolution! Gov: {old_gov}->{self.government}, Econ: {old_econ}->{self.economy}') 