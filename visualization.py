import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import numpy as np


def plot_galaxy_3d(galaxy):
    """
    Plots a 3D map of the galaxy with stars and civilizations.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    xs, ys, zs = [], [], []
    for star in galaxy.stars:
        xs.append(star.position[0])
        ys.append(star.position[1])
        zs.append(star.position[2])
    ax.scatter(xs, ys, zs, s=2, c='yellow', alpha=0.5, label='Stars')
    for civ in galaxy.civilizations:
        if civ.status == 'alive':
            x = civ.home_planet.star.position[0]
            y = civ.home_planet.star.position[1]
            z = civ.home_planet.star.position[2]
            ax.scatter([x], [y], [z], s=40, c='red', marker='^', label='Civilization')
    ax.set_xlabel('X (ly)')
    ax.set_ylabel('Y (ly)')
    ax.set_zlabel('Z (ly)')
    plt.title('Galaxy Map')
    plt.show()


def plot_civilization_stats(stats_history):
    """
    Plots the number of alive civilizations and total population over time.
    """
    df = pd.DataFrame(stats_history)
    plt.figure()
    plt.plot(df['alive_civs'], label='Alive Civilizations')
    plt.plot(df['total_population'], label='Total Population')
    if 'avg_tech' in df:
        plt.plot(df['avg_tech'], label='Average Tech Level')
    plt.xlabel('Time (x1000 years)')
    plt.legend()
    plt.title('Civilization Stats Over Time')
    plt.show()


def plot_trade_network(galaxy):
    """
    Plots a network graph of trade or diplomatic relations between civilizations.
    Shows edge weights for trade volume or diplomatic status.
    """
    G = nx.Graph()
    for civ in galaxy.civilizations:
        if civ.status == 'alive':
            G.add_node(civ.id)
    # Example: add edges for trade and diplomacy
    for i, civ1 in enumerate(galaxy.civilizations):
        for j, civ2 in enumerate(galaxy.civilizations):
            if i < j and civ1.status == 'alive' and civ2.status == 'alive':
                # Placeholder: random trade volume and diplomacy
                trade_volume = np.random.randint(0, 1000)
                diplomacy = np.random.randint(-10, 10)
                if trade_volume > 500:
                    G.add_edge(civ1.id, civ2.id, weight=trade_volume, color='green')
                elif diplomacy < -5:
                    G.add_edge(civ1.id, civ2.id, weight=abs(diplomacy)*10, color='red')
    pos = nx.spring_layout(G)
    edges = G.edges()
    colors = [G[u][v]['color'] if 'color' in G[u][v] else 'gray' for u,v in edges]
    weights = [G[u][v]['weight']/100 for u,v in edges]
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='red', edge_color=colors, width=weights)
    plt.title('Trade/Diplomacy Network')
    plt.show()


def plot_civilization_history(civilization):
    """
    Plots the history/timeline of a single civilization.
    """
    events = civilization.history
    if not events:
        print(f"Civilization {civilization.id} has no history events.")
        return
    plt.figure(figsize=(8, 2))
    plt.title(f"Civilization {civilization.id} History")
    plt.plot(range(len(events)), [1]*len(events), 'ro')
    for i, event in enumerate(events):
        plt.text(i, 1.02, event, rotation=45, ha='right', va='bottom', fontsize=8)
    plt.yticks([])
    plt.xlabel('Event #')
    plt.show()


def plot_resource_heatmap(galaxy):
    """
    Plots a heatmap of resource distribution across the galaxy.
    """
    xs, ys, resources = [], [], []
    for planet in galaxy.planets:
        xs.append(planet.star.position[0])
        ys.append(planet.star.position[1])
        resources.append(planet.resources)
    plt.figure(figsize=(10, 8))
    plt.hexbin(xs, ys, C=resources, gridsize=50, cmap='YlOrRd', bins='log')
    plt.colorbar(label='Resource Abundance (log scale)')
    plt.xlabel('X (ly)')
    plt.ylabel('Y (ly)')
    plt.title('Resource Distribution Heatmap')
    plt.show()


def plot_tech_tree(civ):
    """
    Visualizes the tech tree for a given civilization.
    """
    techs = getattr(civ, 'techs', [])
    all_techs = [
        'Agriculture', 'Metallurgy', 'Spaceflight', 'Fusion Power',
        'AI', 'FTL Communication', 'Terraforming', 'Dyson Spheres'
    ]
    y = [1 if t in techs else 0 for t in all_techs]
    plt.figure(figsize=(10, 2))
    plt.bar(all_techs, y, color=['green' if v else 'gray' for v in y])
    plt.title(f"Tech Tree for Civilization {civ.id}")
    plt.ylim(0, 1.2)
    plt.ylabel('Researched')
    plt.show()

# Add more visualization functions as needed for deeper analysis. 