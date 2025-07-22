import random

class CosmicEvent:
    """
    Base class for cosmic events (supernova, gamma-ray burst, asteroid impact, black hole, etc).
    """
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect  # Function to apply effect

    def trigger(self, galaxy):
        self.effect(galaxy)

class CivilizationEvent:
    """
    Base class for civilization events (revolt, boom, crash, golden age, plague).
    """
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect  # Function to apply effect

    def trigger(self, civilization):
        self.effect(civilization)

class EventManager:
    """
    Manages random events in the simulation.
    Handles both cosmic and civilization events, with detailed logging.
    """
    def __init__(self, galaxy):
        self.galaxy = galaxy
        self.events = []
        self.log = []

    def maybe_trigger_cosmic_event(self):
        # Supernova
        if random.random() < 0.01:
            star = random.choice(self.galaxy.stars)
            for planet in star.planets:
                planet.has_life = False
                planet.has_intelligent_life = False
                planet.civilization = None
            msg = f"Supernova at star {star.id}! All planets sterilized."
            print(msg)
            self.log.append(msg)
        # Asteroid impact
        if random.random() < 0.01:
            planet = random.choice(self.galaxy.planets)
            planet.has_life = False
            planet.has_intelligent_life = False
            if planet.civilization:
                planet.civilization.collapse('asteroid impact')
            msg = f"Asteroid impact on planet {planet.id}!"
            print(msg)
            self.log.append(msg)
        # Black hole event
        if random.random() < 0.005:
            star = random.choice(self.galaxy.stars)
            for planet in star.planets:
                planet.has_life = False
                planet.has_intelligent_life = False
                planet.civilization = None
            msg = f"Black hole devoured star {star.id}!"
            print(msg)
            self.log.append(msg)

    def maybe_trigger_civilization_event(self):
        for civ in self.galaxy.civilizations:
            if civ.status == 'alive':
                # Revolt
                if random.random() < 0.02:
                    civ.collapse('internal revolt')
                    msg = f"Civilization {civ.id} collapsed due to revolt!"
                    print(msg)
                    self.log.append(msg)
                # Golden age
                if random.random() < 0.01:
                    civ.growth_rate *= 1.5
                    civ.history.append('Golden Age! Growth rate increased.')
                    msg = f"Civilization {civ.id} entered a Golden Age!"
                    print(msg)
                    self.log.append(msg)
                # Plague
                if random.random() < 0.01:
                    civ.population = int(civ.population * 0.7)
                    civ.history.append('Plague! Population reduced.')
                    msg = f"Civilization {civ.id} hit by a plague! Population reduced."
                    print(msg)
                    self.log.append(msg)
                # Resource boom
                if random.random() < 0.01:
                    civ.resources += int(civ.resources * 0.5)
                    civ.history.append('Resource boom! Resources increased.')
                    msg = f"Civilization {civ.id} experienced a resource boom!"
                    print(msg)
                    self.log.append(msg)
                # Resource crash
                if random.random() < 0.01:
                    civ.resources = int(civ.resources * 0.5)
                    civ.history.append('Resource crash! Resources halved.')
                    msg = f"Civilization {civ.id} suffered a resource crash!"
                    print(msg)
                    self.log.append(msg) 