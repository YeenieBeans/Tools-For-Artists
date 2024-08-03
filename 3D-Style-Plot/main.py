import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Define colors and size
colors = {
    "lavender": "#9876B6",
    "obsidian": "#222326",
    "desaturated_cream": "#E6E7C9",
    "lime": "#D6DC82",
    "cherry": "#DE6072",
    "gray_fill": "#CFCFCF",
    "user_point": "#3D2FD0",
    "friend_point": "#B469C4"
}
size = 10

def create_initial_plot():
    fig = go.Figure()

    # Axes
    axes = [
        ([0, size], [0, 0], [0, 0], colors['lavender']),
        ([0, -size], [0, 0], [0, 0], colors['lavender']),
        ([0, 0], [0, size], [0, 0], colors['lime']),
        ([0, 0], [0, -size], [0, 0], colors['lime']),
        ([0, 0], [0, 0], [0, size], colors['cherry']),
        ([0, 0], [0, 0], [0, -size], colors['cherry'])
    ]
    for x, y, z, color in axes:
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color=color, width=4), hoverinfo="none"))

    # Cube edges
    cube_vertices = [
        [-size, -size, -size], [-size, -size, size], [-size, size, -size], [-size, size, size],
        [size, -size, -size], [size, -size, size], [size, size, -size], [size, size, size]
    ]
    cube_edges = [
        [0, 1], [1, 3], [3, 2], [2, 0],
        [4, 5], [5, 7], [7, 6], [6, 4],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]
    for edge in cube_edges:
        fig.add_trace(go.Scatter3d(
            x=[cube_vertices[edge[0]][0], cube_vertices[edge[1]][0]],
            y=[cube_vertices[edge[0]][1], cube_vertices[edge[1]][1]],
            z=[cube_vertices[edge[0]][2], cube_vertices[edge[1]][2]],
            mode='lines', line=dict(color=colors['desaturated_cream'], width=2), hoverinfo="none"
        ))

    # Hyperplanes
    hyperplanes = [
        # X-Y plane
        (np.array([[-size, -size], [0, 0]]), np.array([[-size, size], [-size, size]]), np.zeros((2, 2)),
         'rgba(152, 118, 182, 0.85)'),
        (np.array([[0, 0], [size, size]]), np.array([[-size, size], [-size, size]]), np.zeros((2, 2)),
         'rgba(211, 211, 211, 0.85)'),
        # Y-Z plane
        (np.zeros((2, 2)), np.array([[-size, -size], [0, 0]]), np.array([[-size, size], [-size, size]]),
         'rgba(214, 220, 130, 0.85)'),
        (np.zeros((2, 2)), np.array([[0, 0], [size, size]]), np.array([[-size, size], [-size, size]]),
         'rgba(211, 211, 211, 0.85)'),
        # X-Z plane
        (np.array([[-size, size], [-size, size]]), np.zeros((2, 2)), np.array([[-size, -size], [0, 0]]),
         'rgba(222, 96, 114, 0.85)'),
        (np.array([[-size, size], [-size, size]]), np.zeros((2, 2)), np.array([[0, 0], [size, size]]),
         'rgba(211, 211, 211, 0.85)')
    ]
    for x, y, z, color in hyperplanes:
        fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale=[[0, color], [1, color]], opacity=0.85, showscale=False,
                                 hoverinfo="none"))

    # Text annotations
    fig.add_trace(go.Scatter3d(
        x=[size, -size, 0, 0, 0, 0],
        y=[0, 0, size, -size, 0, 0],
        z=[0, 0, 0, 0, size, -size],
        mode='text',
        text=['Realistic', 'Cartoony', 'Anthro', 'Feral', 'Detailed', 'Simple'],
        textfont=dict(family='Arial, sans-serif', size=18, color=colors['desaturated_cream']),
        textposition='top center',
        hoverinfo="none"
    ))

    # Layout settings
    fig.update_layout(
        title=dict(
            text='<b>3D Representation of Artistic Styles</b>',
            font=dict(size=30, color=colors['desaturated_cream']),
            x=0.5, y=0.95, xanchor='center', yanchor='top'
        ),
        scene=dict(
            xaxis=dict(nticks=4, range=[-size, size], showbackground=False,
                       title_text='<b>Realistic — Cartoony</b>',
                       title_font=dict(size=18, color=colors['desaturated_cream']),
                       tickvals=[-10, 10], ticktext=['', ''], tickfont=dict(color=colors['desaturated_cream']),
                       showticklabels=False),
            yaxis=dict(nticks=4, range=[-size, size], showbackground=False,
                       title_text='<b>Feral — Anthro</b>',
                       title_font=dict(size=18, color=colors['desaturated_cream']),
                       tickvals=[-10, 10], ticktext=['', ''], tickfont=dict(color=colors['desaturated_cream']),
                       showticklabels=False),
            zaxis=dict(nticks=4, range=[-size, size], showbackground=False,
                       title_text='<b>Simple — Detailed</b>',
                       title_font=dict(size=18, color=colors['desaturated_cream']),
                       tickvals=[-10, 10], ticktext=['', ''], tickfont=dict(color=colors['desaturated_cream']),
                       showticklabels=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5), projection=dict(type='perspective')),
            dragmode='orbit',
            bgcolor=colors['obsidian']
        ),
        annotations=[
            dict(
                text='Made by <a href="https://x.com/yeeniebeans" style="color:#9876B6; size=18"><b>YeenieBeans</b></a>',
                x=0.5, y=0.01,
                xref='paper', yref='paper',
                showarrow=False,
                font=dict(size=14, color='#fafae9'),
                align='center'
            )
        ],
        width=1280,
        height=720,
        margin=dict(r=3, l=3, b=3, t=3),
        showlegend=False,
    )
    return fig

def update_plot():
    fig = create_initial_plot()

    # Add the user point if available
    if 'user' in st.session_state:
        user_data = st.session_state['user']
        fig.add_trace(go.Scatter3d(
            x=[user_data['x']], y=[user_data['y']], z=[user_data['z']],
            mode='markers+text',
            marker=dict(size=8, color=user_data['color']),
            text=[user_data['name']],
            textposition='top center',
            hoverinfo="none"
        ))

    # Add friends if available
    for friend in st.session_state['friends']:
        if friend['show']:
            fig.add_trace(go.Scatter3d(
                x=[friend['x']], y=[friend['y']], z=[friend['z']],
                mode='markers+text',
                marker=dict(size=6, color=friend['color']),
                text=[friend['name']],
                textposition='top center',
                hoverinfo="none"
            ))

    return fig

# Streamlit App Setup
st.title("3D Artistic Alignment Plot")
st.markdown("""
Welcome to the 3D Artistic Alignment Plot! This tool helps you visualize where you and your friends align in a three-dimensional artistic space based on realism, ferality, and detail. Adjust the sliders to find your place in the style spectrum, and see how you compare to others!
""")

# SECTION ONE: Discover Your Artistic Alignment
st.header("Discover Your Artistic Alignment")
st.markdown("Use the sliders to determine your position on the style spectrum and see where you align in the 3D space.")

# User inputs
col1, col2 = st.columns([3, 1])
username = col1.text_input("Name", "")
user_color = col2.color_picker("Pick a color", value=colors['user_point'])

col1, col2, col3 = st.columns(3)
x_value = col1.slider("Realistic — Cartoony", -10, 10, 0, key="user_slider_x", format="%d")
y_value = col2.slider("Feral — Anthro", -10, 10, 0, key="user_slider_y", format="%d")
z_value = col3.slider("Simple — Detailed", -10, 10, 0, key="user_slider_z", format="%d")

# Display the values directly below the sliders
col1.markdown(f"<div style='text-align: center;'>{x_value}</div>", unsafe_allow_html=True)
col2.markdown(f"<div style='text-align: center;'>{y_value}</div>", unsafe_allow_html=True)
col3.markdown(f"<div style='text-align: center;'>{z_value}</div>", unsafe_allow_html=True)

# Adjusting vertical spacing
st.markdown("<style>div.row-widget.stSlider { margin-bottom: -10px; }</style>", unsafe_allow_html=True)

if st.button("Submit"):
    if username:
        # Store user data
        st.session_state['user'] = {
            'name': username,
            'x': x_value,
            'y': y_value,
            'z': z_value,
            'color': user_color
        }
        st.write(f"Your alignment is ({x_value}, {y_value}, {z_value}).")

st.markdown("---")

# SECTION TWO: Add Your Friends
st.header("Add Your Friends")
st.markdown("Add your friends to the artistic style alignment plot.")

# Friend inputs
friend_col1, friend_col2 = st.columns([3, 1])
friend_name = friend_col1.text_input("Friend's Name")
friend_color = friend_col2.color_picker("Pick a color", value=colors['friend_point'])

col1, col2, col3 = st.columns(3)
friend_x = col1.number_input("Realistic — Cartoony", value=0, key="friend_input_x")
friend_y = col2.number_input("Feral — Anthro", value=0, key="friend_input_y")
friend_z = col3.number_input("Simple — Detailed", value=0, key="friend_input_z")

if 'friends' not in st.session_state:
    st.session_state['friends'] = []

if st.button("Add Friend"):
    if friend_name:
        st.session_state['friends'].append({
            'name': friend_name,
            'x': friend_x,
            'y': friend_y,
            'z': friend_z,
            'color': friend_color,
            'show': True
        })
    else:
        st.warning("Please enter your friend's name before adding.")

# Display current friends and manage visibility
st.write("Current Friends:")
if st.session_state['friends']:
    friends_checklist = st.session_state['friends']
    for i, friend in enumerate(friends_checklist):
        is_checked = st.checkbox(f"{friend['name']} ({friend['x']}, {friend['y']}, {friend['z']})", key=f"friend_{i}_check", value=friend['show'])
        friends_checklist[i]['show'] = is_checked

st.markdown("---")

# SECTION THREE: Artistic Style Alignment
st.header("Artistic Style Alignment")
st.markdown("This is an interactive plot you can drag around! View options are in the upper-right corner.")

# Create and display plot
plot = update_plot()
st.plotly_chart(plot, use_container_width=True)
