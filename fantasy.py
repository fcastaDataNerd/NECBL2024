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
        
        # Reorder standings: Sort by Wins (descending), then PF (descending)
        st.session_state.updated_records = st.session_state.updated_records.sort_values(
            by=["Wins", "PF"], ascending=[False, False]
        ).reset_index(drop=True)
        
        st.success(f"Result submitted for {team1} vs. {team2}")

# Display updated records
st.subheader("Updated Standings")
st.dataframe(st.session_state.updated_records)

st.subheader("Week 13 Matchups")
week13_matchups = schedule[schedule['Week'] == 13]
for i, matchup in week13_matchups.iterrows():
    team1 = matchup['Team1']
    team2 = matchup['Team2']
    proj1 = matchup['Team1Proj']
    proj2 = matchup['Team2Proj']

    st.markdown(f"### {team1} vs. {team2}")

    # Select winner
    winner = st.selectbox(f"Select the winner for {team1} vs. {team2}:",
                          [team1, team2], key=f"winner_13_{i}")

    # Point entry option
    st.write(f"Projected Points: {team1} - {proj1}, {team2} - {proj2}")
    custom_points = st.checkbox(f"Enter custom points for {team1} vs. {team2}?", key=f"custom_points_13_{i}")

    if custom_points:
        # Custom points input
        points1 = st.number_input(f"Enter points for {team1}:", min_value=0, key=f"points1_13_{i}")
        points2 = st.number_input(f"Enter points for {team2}:", min_value=0, key=f"points2_13_{i}")
    else:
        # Use projected points
        points1 = proj1
        points2 = proj2

    # Update records
    if winner == team1:
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'Wins'] += 1
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'Loss'] += 1
    else:
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'Wins'] += 1
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'Loss'] += 1

    st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'PF'] += points1
    st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'PF'] += points2

# Sort standings after week 13
st.session_state.updated_records = st.session_state.updated_records.sort_values(
    by=['Wins', 'PF'], ascending=[False, False]).reset_index(drop=True)

# Display updated standings after Week 13
st.subheader("Updated Standings")
st.dataframe(st.session_state.updated_records)

# Week 14 Loop
st.subheader("Week 14 Matchups")
week14_matchups = schedule[schedule['Week'] == 14]
for i, matchup in week14_matchups.iterrows():
    team1 = matchup['Team1']
    team2 = matchup['Team2']
    proj1 = matchup['Team1Proj']
    proj2 = matchup['Team2Proj']

    st.markdown(f"### {team1} vs. {team2}")

    # Select winner
    winner = st.selectbox(f"Select the winner for {team1} vs. {team2}:",
                          [team1, team2], key=f"winner_14_{i}")

    # Point entry option
    st.write(f"Projected Points: {team1} - {proj1}, {team2} - {proj2}")
    custom_points = st.checkbox(f"Enter custom points for {team1} vs. {team2}?", key=f"custom_points_14_{i}")

    if custom_points:
        # Custom points input
        points1 = st.number_input(f"Enter points for {team1}:", min_value=0, key=f"points1_14_{i}")
        points2 = st.number_input(f"Enter points for {team2}:", min_value=0, key=f"points2_14_{i}")
    else:
        # Use projected points
        points1 = proj1
        points2 = proj2

    # Update records
    if winner == team1:
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'Wins'] += 1
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'Loss'] += 1
    else:
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'Wins'] += 1
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'Loss'] += 1

    st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team1, 'PF'] += points1
    st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == team2, 'PF'] += points2

# Sort standings after week 14
st.session_state.updated_records = st.session_state.updated_records.sort_values(
    by=['Wins', 'PF'], ascending=[False, False]).reset_index(drop=True)

# Display final standings after Week 14
st.subheader("Updated Standings")
st.dataframe(st.session_state.updated_records)
