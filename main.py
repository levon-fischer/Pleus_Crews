import random

import networkx as nx
import pandas as pd
import streamlit
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

st.set_page_config(page_title='Pleus Crews',
                   layout='wide')

titles = ["Pleus' Crews",
          "Pleus' Rank Reviews",
          "Pleus' Who's Who",
          "Choosin' Crews with Chief Pleus",
          "Pleus' Organizational Muse",
          "Pleus' Command Views",
          "Pleus' Chain of Command Stand",
          "Pleus' Team Scheme",
          "Pleus' Crew Stew"]

streamlit.title(random.choice(titles))

# Load data
sq = pd.read_csv('roster.csv')
sq = sq[['FULL_NAME', 'GRADE', 'OFFICE_SYMBOL', 'SUPV_NAME']]

sq['EMPLOYEE'] = sq['FULL_NAME'].str.split(', ').apply(lambda x: ' '.join([x[0], x[1].split(' ')[0]]))
sq['SUPV_NAME'] = sq['SUPV_NAME'].fillna('UNKNOWN SUPERVISOR')
sq.loc[sq['SUPV_NAME'] == 'UNKNOWN', 'SUPV_NAME'] = 'UNKNOWN SUPERVISOR'
sq.loc[~sq['SUPV_NAME'].isin(sq['EMPLOYEE']), 'SUPV_NAME'] = 'OUT OF UNIT'
sq['OFFICE_SYMBOL'] = sq['OFFICE_SYMBOL'].fillna('UNKNOWN')

# Define the rank order of the grades
rank_order = {
    'COL': 1,
    'LTC': 2,
    'MAJ': 3,
    'CPT': 4,
    '1LT': 5,
    '2LT': 6,
    'CMS': 7,
    'SMS': 8,
    'MSG': 9,
    'TSG': 10,
    'SSG': 11,
    'SRA': 12,
    'A1C': 13,
    'AMN': 14,
    'AB': 15
}
sq['rank_order'] = sq['GRADE'].map(rank_order)
sq = sq.sort_values('rank_order')





# Create list of unique offices
offices = sorted(sq['OFFICE_SYMBOL'].unique())
offices = ['All'] + offices
# Create dropdown for office selection
selected_office = st.selectbox('Select Office', offices)
# Filter to selected office
if selected_office != 'All':
    sq = sq[sq['OFFICE_SYMBOL'] == selected_office]

# Create list of unique supervisors
supervisors = sq['SUPV_NAME'].unique()
supervisors = ['All'] + sorted(supervisors)
# Create dropdown for supervisor selection
selected_supervisor = st.selectbox('Select Supervisor', supervisors)
# Filter to selected supervisor
if selected_supervisor != 'All':
    sq = sq[sq['SUPV_NAME'] == selected_supervisor]


# Display dataframe
st.dataframe(sq, use_container_width=True)






# Create graph
G = nx.from_pandas_edgelist(sq, source='SUPV_NAME', target='EMPLOYEE', edge_attr='GRADE', create_using=nx.DiGraph())

# Save graph to dot format
# graph = nx.drawing.nx_pydot.to_pydot(G)
#
# dot_data = graph.to_string()
#
#
# # Create graph in streamlit
# st.graphviz_chart(dot_data, use_container_width=True)



org_net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', directed=True, layout='hierarchical')

org_net.from_nx(G)

# Set node size based on grade
# node_size = {
#     'COL': 50,
#     'LTC': 45,
#     'MAJ': 40,
#     'CPT': 35,
#     '1LT': 30,
#     '2LT': 25,
#     'CMS': 20,
#     'SMS': 15,
#     'MSG': 10,
#     'TSG': 5,
#     'SSG': 5,
#     'SRA': 5,
#     'A1C': 5,
#     'AMN': 5,
#     'AB': 5
# }
# org_net.nodes['id'].map(node_size)

org_net.repulsion(
    node_distance=150,
    central_gravity=0.05,
    spring_length=100,
    spring_strength=0.001,
    damping=0.09
)

try:
    path = 'tmp'
    org_net.save_graph(f'{path}/org_net.html')
    HtmlFile = open(f'{path}/org_net.html', 'r', encoding='utf-8')
except:
    path = 'html_files'
    org_net.save_graph(f'{path}/org_net.html')
    HtmlFile = open(f'{path}/org_net.html', 'r', encoding='utf-8')

components.html(HtmlFile.read(), height=750)