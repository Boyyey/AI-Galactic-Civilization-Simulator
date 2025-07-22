import numpy as np
import random


def random_name(prefix="CIV"):
    """Generate a random name with a prefix."""
    return f"{prefix}-{random.randint(1000, 9999)}"


def distance(pos1, pos2):
    """Calculate Euclidean distance between two 3D points."""
    return np.linalg.norm(np.array(pos1) - np.array(pos2))


def log_event(history, event):
    """Append an event to a civilization's history."""
    history.append(event)


def weighted_choice(choices, weights):
    """Randomly select an item from choices with given weights."""
    total = sum(weights)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(choices, weights):
        if upto + w >= r:
            return c
        upto += w
    return choices[-1]


def random_government():
    """Return a random government type."""
    return random.choice(['democracy', 'monarchy', 'theocracy', 'republic', 'dictatorship', 'anarchy'])


def random_economy():
    """Return a random economic system."""
    return random.choice(['capitalist', 'socialist', 'mixed', 'planned'])


def random_religion():
    """Return a random religion/philosophy."""
    return random.choice(['none', 'polytheism', 'monotheism', 'animism', 'philosophy'])


def random_language():
    """Return a random language."""
    return random.choice(['Galactic Basic', 'Proto', 'Lingua', 'Xeno', 'Synth'])


def format_event_log(log):
    """Format a list of event log strings for display."""
    return '\n'.join(f"- {event}" for event in log) 