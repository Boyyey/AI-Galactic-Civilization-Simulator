import numpy as np
import random

class Star:
    """
    Represents a star in the galaxy.
    Attributes:
        id: Unique identifier
        position: 3D coordinates
        star_type: Spectral type (OBAFGKM)
        metallicity: Fraction of heavy elements
        age: Age in billion years
        luminosity: Star luminosity (solar units)
        planets: List of Planet objects
    """
    def __init__(self, id, position, star_type, metallicity, age):
        self.id = id
        self.position = position  # (x, y, z)
        self.star_type = star_type
        self.metallicity = metallicity
        self.age = age
        self.luminosity = self.estimate_luminosity()
        self.planets = []

    def estimate_luminosity(self):
        # Simple mapping by star type
        mapping = {'O': 100000, 'B': 20000, 'A': 80, 'F': 6, 'G': 1, 'K': 0.4, 'M': 0.04}
        return mapping.get(self.star_type, 1)

class Planet:
    """
    Represents a planet orbiting a star.
    Attributes:
        id: Unique identifier
        star: Parent Star object
        planet_type: rocky, gas_giant, etc.
        mass: In Earth masses
        temperature: In Kelvin
        resources: Available resources
        habitable_zone: Boolean if in habitable zone
        orbital_radius: Distance from star (AU)
        atmosphere: Type of atmosphere
        moons: Number of moons
        has_life: Boolean if life exists
        has_intelligent_life: Boolean if intelligent life exists
        civilization: Civilization object if present
    """
    ATMOSPHERES = ['none', 'thin', 'Earth-like', 'thick', 'toxic']
    def __init__(self, id, star, planet_type, mass, temperature, resources, habitable_zone):
        self.id = id
        self.star = star
        self.planet_type = planet_type
        self.mass = mass
        self.temperature = temperature
        self.resources = resources
        self.habitable_zone = habitable_zone
        self.orbital_radius = np.random.uniform(0.1, 30)  # AU
        self.atmosphere = random.choice(self.ATMOSPHERES)
        self.moons = np.random.poisson(1) if planet_type == 'rocky' else np.random.poisson(10)
        self.has_life = False
        self.has_intelligent_life = False
        self.civilization = None

class Galaxy:
    """
    Represents the galaxy, containing stars, planets, and civilizations.
    Handles procedural generation and seeding of life and civilizations.
    """
    STAR_TYPES = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    PLANET_TYPES = ['rocky', 'gas_giant', 'ice', 'ocean', 'desert']

    def __init__(self, n_stars=1000, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        self.stars = []
        self.planets = []
        self.civilizations = []
        self.generate_stars(n_stars)
        self.generate_planets()
        self.seed_life()

    def generate_stars(self, n_stars):
        for i in range(n_stars):
            position = np.random.uniform(-500, 500, 3)
            star_type = np.random.choice(self.STAR_TYPES, p=[0.01, 0.02, 0.06, 0.12, 0.2, 0.3, 0.29])
            metallicity = np.random.uniform(0.001, 0.03)
            age = np.random.uniform(0.1, 13.0)
            star = Star(i, position, star_type, metallicity, age)
            self.stars.append(star)

    def generate_planets(self):
        planet_id = 0
        for star in self.stars:
            n_planets = np.random.poisson(3)
            for _ in range(n_planets):
                planet_type = np.random.choice(self.PLANET_TYPES, p=[0.5, 0.2, 0.1, 0.1, 0.1])
                mass = np.random.uniform(0.1, 10)
                temperature = np.random.uniform(50, 500)
                resources = int(np.random.uniform(1e5, 1e8))
                habitable_zone = 200 < temperature < 350 and planet_type == 'rocky'
                planet = Planet(planet_id, star, planet_type, mass, temperature, resources, habitable_zone)
                star.planets.append(planet)
                self.planets.append(planet)
                planet_id += 1

    def seed_life(self):
        for planet in self.planets:
            if planet.habitable_zone and planet.atmosphere == 'Earth-like':
                p_life = 0.01 + 0.1 * planet.star.metallicity
                if planet.star.star_type in ['G', 'K', 'M']:
                    p_life += 0.05
                if np.random.rand() < p_life:
                    planet.has_life = True
                    p_intel = 0.01 + 0.05 * planet.star.metallicity
                    if np.random.rand() < p_intel:
                        planet.has_intelligent_life = True

    def get_nearby_planets(self, planet, max_distance=20):
        result = []
        for p in self.planets:
            if p is not planet and p.civilization is None:
                d = np.linalg.norm(planet.star.position - p.star.position)
                if d < max_distance:
                    result.append(p)
        return result 