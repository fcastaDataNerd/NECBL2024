import numpy as np
import pandas as pd
import streamlit as st

# Load data
pd.set_option('display.max_columns', None)
scores = pd.read_excel("Fantasy.xlsx", sheet_name="ScoringData")
records = pd.read_excel("Fantasy.xlsx", sheet_name="Records")
schedule = pd.read_excel("Fantasy.xlsx", sheet_name="Schedule")
playoffs = pd.read_excel("Fantasy.xlsx", sheet_name="Playoffs")

# Streamlit App Title
st.title("ROS Playoff Scenarios")
st.header("Greetings, gentlemen. Discover your tanking scenarios below (except for FS)")

# Initialize session state for updated records
if "updated_records" not in st.session_state:
    st.session_state.updated_records = records.copy()

# Filter Week 12 matchups
week_12_matchups = schedule[schedule['Week'] == 12]

# Display Week 12 matchups
st.subheader("Week 12 Matchups")
for i, matchup in week_12_matchups.iterrows():
    team1 = matchup['Team1']
    team2 = matchup['Team2']
    proj1 = matchup['Team1Proj']
    proj2 = matchup['Team2Proj']
    
    st.markdown(f"### {team1} vs. {team2}")
    
    # Select winner
    winner = st.selectbox(f"Select the winner for {team1} vs. {team2}:",
                          [team1, team2], key=f"winner_{i}")
    
    # Point entry option
    st.write(f"Projected Points: {team1} - {proj1}, {team2} - {proj2}")
    custom_points = st.checkbox(f"Enter custom points for {team1} vs. {team2}?", key=f"custom_points_{i}")
    
    if custom_points:
        # Custom points input
        points1 = st.number_input(f"Enter {team1}'s points:", min_value=0.0, value=float(proj1), key=f"points1_{i}")
        points2 = st.number_input(f"Enter {team2}'s points:", min_value=0.0, value=float(proj2), key=f"points2_{i}")
    else:
        # Default to projected points
        points1, points2 = proj1, proj2
    
    # Submit the results and update session state
    if st.button(f"Submit result for {team1} vs. {team2}", key=f"submit_{i}"):
        # Add a win to the selected winner, and a loss to the loser
        if winner == team1:
            st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'Wins'] += 1
            st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'Loss'] += 1
        else:
            st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'Wins'] += 1
            st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'Loss'] += 1
        
        # Update points for both teams
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'PF'] += points1
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'PF'] += points2
        
        st.success(f"Result submitted for {team1} vs. {team2}")

# Display updated records
st.subheader("Updated Records")
st.dataframe(st.session_state.updated_records)
