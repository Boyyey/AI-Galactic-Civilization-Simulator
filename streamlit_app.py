import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly
import matplotlib.pyplot as plt
from datetime import datetime
from simulation import Simulation, TechTree
from visualization import plot_galaxy_3d, plot_civilization_stats, plot_trade_network, plot_civilization_history, plot_resource_heatmap, plot_tech_tree
from events import EventManager
from utils import format_event_log

# Set page configuration
st.set_page_config(
    page_title="🌌 Galactic Civilization Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f5f7fa;
    }
    .stProgress > div > div > div > div {
        background-color: #4e89e5;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🌌 AI Galactic Civilization Simulator Dashboard")
st.markdown("""
Explore the rise and fall of civilizations across a procedurally generated galaxy. 
Adjust parameters, run simulations, and analyze the results through interactive visualizations.
""")

# Sidebar controls
with st.sidebar:
    st.header("🎮 Simulation Controls")
    
    # Scenario selection with descriptions
    scenario_descriptions = {
        "Default": "Balanced parameters for a standard simulation",
        "Crowded Galaxy": "Many civilizations in a dense galaxy, high competition",
        "Sparse Life": "Few civilizations with vast distances between them",
        "Warzone": "High aggression and competition for resources",
        "Peaceful Era": "Cooperative civilizations with low aggression"
    }
    
    scenario = st.selectbox(
        "🌐 Scenario Preset",
        list(scenario_descriptions.keys()),
        format_func=lambda x: f"{x}: {scenario_descriptions[x]}",
        help="Predefined simulation scenarios with different parameters"
    )
    
    st.markdown("---")
    
    # Galaxy parameters
    st.subheader("🌌 Galaxy Parameters")
    n_stars = st.slider(
        "Number of Stars", 
        100, 5000, 1000, step=100,
        help="Total number of stars in the galaxy"
    )
    
    # Civilization parameters
    st.subheader("👥 Civilization Parameters")
    n_civs = st.slider(
        "Number of Civilizations", 
        1, 50, 10, step=1,
        help="Initial number of civilizations"
    )
    
    # Simulation parameters
    st.subheader("⏱ Simulation Parameters")
    steps = st.slider(
        "Simulation Steps (x1000 years)", 
        10, 500, 100, step=10,
        help="Duration of the simulation in thousands of years"
    )
    
    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        seed = st.number_input(
            "Random Seed", 
            min_value=0, max_value=999999, value=42,
            help="Seed for random number generation"
        )
        events_enabled = st.checkbox(
            "Enable Random Events", 
            value=True,
            help="Enable cosmic events and random occurrences"
        )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("🚀 Run Simulation", use_container_width=True, type="primary")
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            if 'sim' in st.session_state:
                del st.session_state['sim']
            if 'event_manager' in st.session_state:
                del st.session_state['event_manager']
            if 'stats_history' in st.session_state:
                del st.session_state['stats_history']
            st.rerun()
    
    # Simulation info
    if 'sim' in st.session_state and st.session_state['sim']:
        st.markdown("---")
        st.markdown("### Simulation Info")
        st.caption(f"Status: {'✅ Complete' if 'end_time' in st.session_state else '⏳ Running'}")
        if 'start_time' in st.session_state:
            duration = (datetime.now() - st.session_state['start_time']).seconds
            st.caption(f"Duration: {duration} seconds")

if 'sim' not in st.session_state or st.sidebar.button("Reset Simulation"):
    st.session_state['sim'] = None
    st.session_state['event_manager'] = None
    st.session_state['stats_history'] = None

if run_button:
    try:
        # Initialize session state for new simulation
        st.session_state['sim'] = None
        st.session_state['event_manager'] = None
        st.session_state['stats_history'] = None
        st.session_state['start_time'] = datetime.now()
        
        # Clear any previous output
        st.empty()
        
        # Create a status container and progress bar
        status_container = st.empty()
        progress_bar = st.progress(0)
        status_text = status_container.info("Initializing simulation...")
        
        # Scenario presets
        if scenario == "Crowded Galaxy":
            n_stars, n_civs = 2000, 40
        elif scenario == "Sparse Life":
            n_stars, n_civs = 2000, 2
        elif scenario == "Warzone":
            n_stars, n_civs = 1000, 20
        elif scenario == "Peaceful Era":
            n_stars, n_civs = 1000, 10
        
        # Initialize simulation
        status_text.info("Generating galaxy...")
        sim = Simulation(n_stars=n_stars, n_civs=n_civs, seed=seed)
        event_manager = EventManager(sim.galaxy)
        stats_history = []
        
        # Run simulation steps
        status_text.info("Running simulation...")
        for t in range(steps):
            # Update progress
            progress = (t + 1) / steps
            progress_bar.progress(progress)
            status_text.info(f"Step {t+1}/{steps} ({(t+1)*1000} years simulated)")
            
            # Run simulation step
            sim.step()
            
            # Trigger random events if enabled
            if events_enabled:
                event_manager.maybe_trigger_cosmic_event()
                event_manager.maybe_trigger_civilization_event()
            
            # Record statistics
            stats = sim.stats()
            stats['step'] = t
            stats_history.append(stats)
            
            # Update session state periodically for better responsiveness
            if t % 10 == 0 or t == steps - 1:
                st.session_state['sim'] = sim
                st.session_state['event_manager'] = event_manager
                st.session_state['stats_history'] = stats_history
        
        # Store final state
        st.session_state['sim'] = sim
        st.session_state['event_manager'] = event_manager
        st.session_state['stats_history'] = stats_history
        st.session_state['end_time'] = datetime.now()
        
        # Show completion message
        duration = (st.session_state['end_time'] - st.session_state['start_time']).seconds
        status_container.success(f"✅ Simulation completed in {duration} seconds!")
        progress_bar.empty()
        st.balloons()
        
    except Exception as e:
        status_container.error(f"❌ Error during simulation: {str(e)}")
        st.exception(e)  # Show full traceback in the app
        if 'sim' in st.session_state:
            del st.session_state['sim']
        if 'event_manager' in st.session_state:
            del st.session_state['event_manager']
        if 'stats_history' in st.session_state:
            del st.session_state['stats_history']

if st.session_state['sim']:
    sim = st.session_state['sim']
    stats_history = st.session_state['stats_history']
    event_manager = st.session_state['event_manager']
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Galaxy Map", "Stats & Network", "Resource Heatmap", "Civilizations", "Event Log"])
    with tab1:
        st.subheader("🌌 3D Galaxy Map")
        
        # Add description and controls
        st.markdown("""
        Explore the 3D visualization of your simulated galaxy. Stars are shown as yellow points, 
        while civilizations are marked with colored markers. Use the controls to rotate, zoom, 
        and pan the view.
        """)
        
        # Create a container for the 3D plot
        plot_container = st.container()
        
        with plot_container:
            try:
                # Prepare star data
                star_positions = np.array([
                    [star.position[0], star.position[1], star.position[2]]
                    for star in sim.galaxy.stars
                ])
                
                # Prepare civilization data
                civ_data = []
                for civ in sim.galaxy.civilizations:
                    if civ.status == 'alive':
                        pos = civ.home_planet.star.position
                        civ_data.append({
                            'x': pos[0],
                            'y': pos[1],
                            'z': pos[2],
                            'civ_id': f"Civ {civ.id}",
                            'status': civ.status,
                            'population': f"{civ.population:,}",
                            'tech_level': civ.tech_level
                        })
                
                # Create 3D scatter plot for stars
                fig = go.Figure()
                
                # Add stars
                fig.add_trace(go.Scatter3d(
                    x=star_positions[:, 0],
                    y=star_positions[:, 1],
                    z=star_positions[:, 2],
                    mode='markers',
                    marker=dict(
                        size=2,
                        color='yellow',
                        opacity=0.5,
                        sizemode='diameter'
                    ),
                    name='Stars',
                    hoverinfo='none'
                ))
                
                # Add civilizations if any exist
                if civ_data:
                    df_civs = pd.DataFrame(civ_data)
                    fig.add_trace(go.Scatter3d(
                        x=df_civs['x'],
                        y=df_civs['y'],
                        z=df_civs['z'],
                        mode='markers+text',
                        marker=dict(
                            size=8,
                            color='red',
                            symbol='diamond',
                            line=dict(width=1, color='white')
                        ),
                        text=df_civs['civ_id'],
                        textposition='top center',
                        hoverinfo='text',
                        hovertext=[
                            f"<b>{row['civ_id']}</b><br>"
                            f"Status: {row['status'].title()}<br>"
                            f"Population: {row['population']}<br>"
                            f"Tech Level: {row['tech_level']:.1f}"
                            for _, row in df_civs.iterrows()
                        ],
                        name='Civilizations'
                    ))
                
                # Update layout for better visualization
                fig.update_layout(
                    scene=dict(
                        xaxis_title='X (light years)',
                        yaxis_title='Y (light years)',
                        zaxis_title='Z (light years)',
                        aspectmode='auto',
                        camera=dict(
                            eye=dict(x=1.5, y=1.5, z=1.5)
                        ),
                        xaxis=dict(showbackground=False),
                        yaxis=dict(showbackground=False),
                        zaxis=dict(showbackground=False)
                    ),
                    margin=dict(l=0, r=0, b=0, t=30),
                    height=700,
                    legend=dict(
                        yanchor='top',
                        y=0.99,
                        xanchor='left',
                        x=0.01
                    )
                )
                
                # Display the plot
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error generating 3D visualization: {str(e)}")
                st.warning("Falling back to static 2D visualization...")
                
                # Fallback to 2D visualization if 3D fails
                fig, ax = plt.subplots(figsize=(10, 8))
                ax.scatter(
                    [s.position[0] for s in sim.galaxy.stars],
                    [s.position[1] for s in sim.galaxy.stars],
                    c='yellow', alpha=0.3, s=1
                )
                
                # Plot civilizations
                for civ in sim.galaxy.civilizations:
                    if civ.status == 'alive':
                        pos = civ.home_planet.star.position
                        ax.scatter(pos[0], pos[1], c='red', s=50, marker='*')
                        ax.annotate(
                            f"Civ {civ.id}",
                            (pos[0], pos[1]),
                            textcoords="offset points",
                            xytext=(0,5),
                            ha='center'
                        )
                
                ax.set_xlabel('X (light years)')
                ax.set_ylabel('Y (light years)')
                ax.set_title('2D Galaxy Projection (Top-Down View)')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
        
        # Add galaxy statistics
        st.markdown("### 🌠 Galaxy Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Stars", f"{len(sim.galaxy.stars):,}")
        with col2:
            st.metric("Total Planets", f"{len(sim.galaxy.planets):,}")
        with col3:
            habitable_planets = sum(1 for p in sim.galaxy.planets if getattr(p, 'habitable', False))
            st.metric("Habitable Planets", f"{habitable_planets:,}")
        with col4:
            st.metric("Civilizations", f"{sum(1 for c in sim.galaxy.civilizations if c.status == 'alive')}")
    
    with tab2:
        st.subheader("📊 Civilization Statistics")
        
        # Add description
        st.markdown("""
        Track the evolution of civilizations over time. Use the tabs below to explore different aspects 
        of the simulation including population trends, technology development, and inter-civilization relationships.
        """)
        
        # Create tabs for different visualizations
        tab2_1, tab2_2, tab2_3 = st.tabs(["Population & Tech", "Civilization Count", "Advanced Metrics"])
        
        with tab2_1:
            # Population and Tech Level Over Time
            st.markdown("### Population and Technology Over Time")
            
            # Create figure with secondary y-axis
            fig = go.Figure()
            
            # Add population trace (primary y-axis)
            fig.add_trace(
                go.Scatter(
                    x=[s['step'] * 1000 for s in stats_history],
                    y=[s['total_population'] for s in stats_history],
                    name="Total Population",
                    line=dict(color='#1f77b4', width=2.5),
                    yaxis='y1'
                )
            )
            
            # Add tech level trace (secondary y-axis)
            fig.add_trace(
                go.Scatter(
                    x=[s['step'] * 1000 for s in stats_history],
                    y=[s['avg_tech'] for s in stats_history],
                    name="Average Tech Level",
                    line=dict(color='#ff7f0e', width=2.5, dash='dash'),
                    yaxis='y2'
                )
            )
            
            # Update layout
            fig.update_layout(
                title="Population and Technology Trends Over Time",
                xaxis_title="Years",
                yaxis=dict(
                    title="Total Population",
                    title_font=dict(color='#1f77b4'),
                    tickfont=dict(color='#1f77b4')
                ),
                yaxis2=dict(
                    title="Average Tech Level",
                    title_font=dict(color='#ff7f0e'),
                    tickfont=dict(color='#ff7f0e'),
                    anchor="x",
                    overlaying="y",
                    side="right"
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                height=500,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Peak Population", 
                    f"{max(s['total_population'] for s in stats_history):,}",
                    f"{max(s['total_population'] for s in stats_history) - stats_history[0]['total_population']:+,}"
                )
            with col2:
                st.metric(
                    "Current Population",
                    f"{stats_history[-1]['total_population']:,}",
                    f"{stats_history[-1]['total_population'] - stats_history[-2]['total_population'] if len(stats_history) > 1 else 0:+,}"
                )
            with col3:
                st.metric(
                    "Average Tech Level",
                    f"{stats_history[-1]['avg_tech']:.2f}",
                    f"{stats_history[-1]['avg_tech'] - stats_history[-2]['avg_tech'] if len(stats_history) > 1 else 0:+.2f}"
                )
        
        with tab2_2:
            # Civilization Count Over Time
            st.markdown("### Civilization Count Over Time")
            
            # Prepare data
            steps = [s['step'] * 1000 for s in stats_history]
            alive_civs = [s['alive_civs'] for s in stats_history]
            
            # Create area chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=steps,
                y=alive_civs,
                fill='tozeroy',
                mode='lines',
                line=dict(color='#2ca02c', width=2.5),
                name='Alive Civilizations',
                hovertemplate='%{y} civilizations<extra></extra>'
            ))
            
            # Add annotations for major changes
            changes = [i for i in range(1, len(stats_history)) 
                     if stats_history[i]['alive_civs'] != stats_history[i-1]['alive_civs']]
            
            for i in changes:
                fig.add_annotation(
                    x=steps[i],
                    y=alive_civs[i],
                    text=f"{alive_civs[i]}",
                    showarrow=True,
                    arrowhead=1,
                    yshift=10
                )
            
            # Update layout
            fig.update_layout(
                title="Number of Civilizations Over Time",
                xaxis_title="Years",
                yaxis_title="Number of Civilizations",
                showlegend=True,
                hovermode='x unified',
                height=500,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add statistics
            initial_civs = stats_history[0]['alive_civs']
            final_civs = stats_history[-1]['alive_civs']
            max_civs = max(s['alive_civs'] for s in stats_history)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Initial Civilizations", initial_civs)
            with col2:
                st.metric("Final Civilizations", final_civs, f"{final_civs - initial_civs:+.0f}")
            with col3:
                st.metric("Peak Civilizations", max_civs)
        
        with tab2_3:
            st.markdown("### Advanced Metrics")
            
            # Calculate additional metrics
            war_count = [s.get('war_count', 0) for s in stats_history]
            trade_volume = [s.get('trade_volume', 0) for s in stats_history]
            
            # Create subplots
            fig = make_subplots(
                rows=2, 
                cols=1, 
                subplot_titles=("Wars Over Time", "Trade Volume Over Time"),
                vertical_spacing=0.15
            )
            
            # War count plot
            fig.add_trace(
                go.Bar(
                    x=steps,
                    y=war_count,
                    name="Wars",
                    marker_color='indianred',
                    opacity=0.7
                ),
                row=1, col=1
            )
            
            # Trade volume plot
            fig.add_trace(
                go.Scatter(
                    x=steps,
                    y=trade_volume,
                    name="Trade Volume",
                    line=dict(color='#17becf', width=2.5),
                    fill='tozeroy',
                    fillcolor='rgba(23, 190, 207, 0.1)'
                ),
                row=2, col=1
            )
            
            # Update layout
            fig.update_layout(
                height=800,
                showlegend=False,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            fig.update_xaxes(title_text="Years", row=1, col=1)
            fig.update_xaxes(title_text="Years", row=2, col=1)
            fig.update_yaxes(title_text="Number of Wars", row=1, col=1)
            fig.update_yaxes(title_text="Trade Volume", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add summary statistics
            st.markdown("#### Simulation Summary")
            
            total_wars = sum(war_count)
            peak_trade = max(trade_volume) if trade_volume else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Total Simulation Time", 
                    f"{steps[-1]:,} years" if steps else "N/A"
                )
            with col2:
                st.metric("Total Wars", f"{total_wars:,}")
            with col3:
                st.metric("Peak Trade Volume", f"{peak_trade:,.0f}" if trade_volume else "N/A")
            
            # Add network visualization if available
            if hasattr(sim, 'diplomacy') and hasattr(sim.diplomacy, 'relationships'):
                st.markdown("---")
                st.markdown("### 🌐 Inter-Civilization Network")
                
                # Create a network graph
                G = nx.Graph()
                
                # Add nodes (civilizations)
                for civ in sim.galaxy.civilizations:
                    if civ.status == 'alive':
                        G.add_node(
                            civ.id,
                            label=f"Civ {civ.id}",
                            size=10 + np.log1p(civ.population/1e6),
                            color='red' if hasattr(civ, 'at_war') and civ.at_war else 'green'
                        )
                
                # Add edges (relationships)
                for (civ1_id, civ2_id), rel in sim.diplomacy.relationships.items():
                    if rel['relation'] > 0.5:  # Positive relationship
                        G.add_edge(civ1_id, civ2_id, color='green', width=2)
                    elif rel['relation'] < -0.5:  # Negative relationship
                        G.add_edge(civ1_id, civ2_id, color='red', width=2)
                
                # Create network visualization
                pos = nx.spring_layout(G, k=0.5, iterations=50)
                
                # Create edge traces
                edge_x = []
                edge_y = []
                edge_colors = []
                
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                    edge_colors.append(G.edges[edge].get('color', '#888'))
                
                edge_trace = go.Scatter(
                    x=edge_x, 
                    y=edge_y,
                    line=dict(width=0.5, color='#888'),
                    hoverinfo='none',
                    mode='lines'
                )
                
                # Create node traces
                node_x = []
                node_y = []
                node_text = []
                node_size = []
                node_color = []
                
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    node_text.append(G.nodes[node]['label'])
                    node_size.append(G.nodes[node]['size'])
                    node_color.append(G.nodes[node]['color'])
                
                node_trace = go.Scatter(
                    x=node_x, 
                    y=node_y,
                    mode='markers+text',
                    text=node_text,
                    textposition="top center",
                    hoverinfo='text',
                    marker=dict(
                        size=node_size,
                        color=node_color,
                        line_width=2
                    )
                )
                
                # Create figure
                fig = go.Figure(
                    data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Civilization Diplomatic Network',
                        title_font_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002
                        )],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add legend
                st.markdown("""
                **Node Colors:**
                - 🔴 At War
                - 🟢 Peaceful
                
                **Edge Colors:**
                - Green: Positive Relationship
                - Red: Negative Relationship
                """)
            else:
                st.info("Relationship data not available. Enable diplomacy in the simulation to see the network visualization.")
    
    with tab3:
        st.subheader("🌡️ Resource Distribution Heatmap")
        
        # Add description
        st.markdown("""
        Explore the distribution of resources across the galaxy. The heatmap shows the concentration 
        of resources in different regions, helping identify valuable areas for expansion and conflict.
        """)
        
        # Create tabs for different resource types
        resource_tabs = st.tabs(["Minerals", "Energy", "Research"])
        
        with resource_tabs[0]:
            st.markdown("### Mineral Resources")
            # Create a placeholder for the heatmap
            fig_minerals = plt.figure(figsize=(10, 8))
            plot_resource_heatmap(sim.galaxy)
            st.pyplot(fig_minerals)
            
            # Add statistics
            mineral_values = [p.minerals for p in sim.galaxy.planets if hasattr(p, 'minerals')]
            if mineral_values:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Minerals", f"{np.mean(mineral_values):.1f}")
                with col2:
                    st.metric("Max Minerals", f"{max(mineral_values):.1f}")
                with col3:
                    st.metric("Total Minerals", f"{sum(mineral_values):,.0f}")
        
        with resource_tabs[1]:
            st.markdown("### Energy Resources")
            # Create a placeholder for the heatmap
            fig_energy = plt.figure(figsize=(10, 8))
            plot_resource_heatmap(sim.galaxy)
            st.pyplot(fig_energy)
            
            # Add statistics
            energy_values = [p.energy for p in sim.galaxy.planets if hasattr(p, 'energy')]
            if energy_values:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Energy", f"{np.mean(energy_values):.1f}")
                with col2:
                    st.metric("Max Energy", f"{max(energy_values):.1f}")
                with col3:
                    st.metric("Total Energy", f"{sum(energy_values):,.0f}")
        
        with resource_tabs[2]:
            st.markdown("### Research Points")
            # Create a placeholder for the heatmap
            fig_research = plt.figure(figsize=(10, 8))
            plot_resource_heatmap(sim.galaxy)
            st.pyplot(fig_research)
            
            # Add statistics
            research_values = [p.research for p in sim.galaxy.planets if hasattr(p, 'research')]
            if research_values:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Research", f"{np.mean(research_values):.1f}")
                with col2:
                    st.metric("Max Research", f"{max(research_values):.1f}")
                with col3:
                    st.metric("Total Research", f"{sum(research_values):,.0f}")
        
        # Add interactive 3D visualization if possible
        st.markdown("---")
        st.markdown("### 3D Resource Distribution")
        
        try:
            # Create 3D scatter plot of planets with resource values
            fig_3d = go.Figure()
            
            # Add planets as 3D scatter points
            for planet in sim.galaxy.planets:
                if hasattr(planet, 'minerals') and hasattr(planet, 'energy') and hasattr(planet, 'research'):
                    # Calculate total resource value for size
                    total_resources = planet.minerals + planet.energy + planet.research
                    
                    # Add the planet to the 3D plot
                    fig_3d.add_trace(go.Scatter3d(
                        x=[planet.star.position[0]],
                        y=[planet.star.position[1]],
                        z=[planet.star.position[2]],
                        mode='markers',
                        marker=dict(
                            size=5 + (total_resources / 10),  # Scale size by resources
                            color=planet.minerals,  # Color by mineral content
                            colorscale='Viridis',
                            opacity=0.8,
                            colorbar=dict(title='Mineral Content'),
                            showscale=True
                        ),
                        text=f"Planet at ({planet.star.position[0]:.1f}, {planet.star.position[1]:.1f}, {planet.star.position[2]:.1f})<br>"
                             f"Minerals: {planet.minerals:.1f}<br>"
                             f"Energy: {planet.energy:.1f}<br>"
                             f"Research: {planet.research:.1f}",
                        hoverinfo='text'
                    ))
            
            # Update layout for 3D plot
            fig_3d.update_layout(
                scene=dict(
                    xaxis=dict(
                        title_text='X (ly)',
                        tickfont=dict(size=10)
                    ),
                    yaxis=dict(
                        title_text='Y (ly)',
                        tickfont=dict(size=10)
                    ),
                    zaxis=dict(
                        title_text='Z (ly)',
                        tickfont=dict(size=10)
                    ),
                    aspectmode='manual',
                    aspectratio=dict(x=1, y=1, z=0.7)
                ),
                height=700,
                margin=dict(l=0, r=0, b=0, t=30)
            )
            
            st.plotly_chart(fig_3d, use_container_width=True)
            
        except Exception as e:
            st.warning(f"Could not generate 3D resource visualization: {str(e)}")
            st.info("Falling back to 2D visualization...")
            
            # Fallback to 2D scatter plot
            fig_2d = go.Figure()
            
            # Add planets as 2D scatter points
            for planet in sim.galaxy.planets:
                if hasattr(planet, 'minerals') and hasattr(planet, 'energy') and hasattr(planet, 'research'):
                    total_resources = planet.minerals + planet.energy + planet.research
                    
                    fig_2d.add_trace(go.Scatter(
                        x=[planet.star.position[0]],
                        y=[planet.star.position[1]],
                        mode='markers',
                        marker=dict(
                            size=5 + (total_resources / 10),
                            color=planet.minerals,
                            colorscale='Viridis',
                            opacity=0.8,
                            showscale=True,
                            colorbar=dict(title='Mineral Content')
                        ),
                        text=f"Planet at ({planet.star.position[0]:.1f}, {planet.star.position[1]:.1f})<br>"
                             f"Minerals: {planet.minerals:.1f}<br>"
                             f"Energy: {planet.energy:.1f}<br>"
                             f"Research: {planet.research:.1f}",
                        hoverinfo='text',
                        name=''
                    ))
            
            fig_2d.update_layout(
                xaxis_title='X (ly)',
                yaxis_title='Y (ly)',
                height=600,
                margin=dict(l=0, r=0, b=0, t=30)
            )
            
            st.plotly_chart(fig_2d, use_container_width=True)
    with tab4:
        st.subheader("Civilization Details")
        for civ in sim.galaxy.civilizations:
            st.markdown(f"### Civilization {civ.id} - Status: {civ.status}")
            st.write(f"Population: {civ.population:,}")
            st.write(f"Planets: {len(civ.planets)}")
            st.write(f"Tech Level: {civ.tech_level}")
            st.write(f"Traits: {civ.traits}")
            st.write(f"Government: {getattr(civ, 'government', 'N/A')}")
            st.write(f"Language: {getattr(civ, 'language', 'N/A')}")
            st.write(f"Religion: {getattr(civ, 'religion', 'N/A')}")
            st.write(f"Economy: {getattr(civ, 'economy', 'N/A')}")
            st.write(f"History: {civ.history}")
            if st.button(f"Show History Plot for Civ {civ.id}"):
                plot_civilization_history(civ)
                st.pyplot(plt.gcf())
            if st.button(f"Show Tech Tree for Civ {civ.id}"):
                plot_tech_tree(civ)
                st.pyplot(plt.gcf())
    with tab5:
        st.subheader("Event Log")
        if event_manager and hasattr(event_manager, 'log'):
            st.text(format_event_log(event_manager.log))
        else:
            st.write("No events logged yet.") 