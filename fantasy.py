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

st.subheader("I am the worst player in league history and I colluded")
st.image("Screenshot (1391).png", use_column_width=True)


# Initialize session state for updated records and finalized predictions
if "updated_records" not in st.session_state:
    st.session_state.updated_records = records.copy()

if "finalized_predictions" not in st.session_state:
    st.session_state.finalized_predictions = {}

# Function to adjust wins/losses and points
def update_records(winner, loser, winner_points, loser_points, week_key):
    # Undo the previous outcome if it exists
    if week_key in st.session_state.finalized_predictions:
        prev_winner, prev_loser, prev_winner_points, prev_loser_points = st.session_state.finalized_predictions[week_key]
        # Reverse previous adjustments
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == prev_winner, 'Wins'] -= 1
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == prev_loser, 'Loss'] -= 1
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == prev_winner, 'PF'] -= prev_winner_points
        st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == prev_loser, 'PF'] -= prev_loser_points

    # Apply the new outcome
    st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == winner, 'Wins'] += 1
    st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == loser, 'Loss'] += 1
    st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == winner, 'PF'] += winner_points
    st.session_state.updated_records.loc[st.session_state.updated_records['Team'] == loser, 'PF'] += loser_points

    # Store the new prediction in session state
    st.session_state.finalized_predictions[week_key] = (winner, loser, winner_points, loser_points)


# Week 12 Matchups
st.subheader("Week 12 Matchups")
week12_matchups = schedule[schedule['Week'] == 12]
for i, matchup in week12_matchups.iterrows():
    team1 = matchup['Team1']
    team2 = matchup['Team2']
    proj1 = matchup['Team1Proj']
    proj2 = matchup['Team2Proj']

    st.markdown(f"### {team1} vs. {team2}")

    # Select winner
    winner = st.radio(f"Select the winner for {team1} vs. {team2}:",
                      [team1, team2], key=f"winner_12_{i}")

    # Point entry option
    st.write(f"Projected Points: {team1} - {proj1:.2f}, {team2} - {proj2:.2f}")
    custom_points = st.checkbox(f"Enter custom points for {team1} vs. {team2}?", key=f"custom_points_12_{i}")

    if custom_points:
        # Custom points input with up to 2 decimal places
        points1 = st.number_input(f"Enter points for {team1}:", min_value=0.0, format="%.2f", key=f"points1_12_{i}")
        points2 = st.number_input(f"Enter points for {team2}:", min_value=0.0, format="%.2f", key=f"points2_12_{i}")
    else:
        # Use projected points
        points1 = round(proj1, 2)
        points2 = round(proj2, 2)

    # Finalize prediction
    if st.button(f"Finalize Winner for {team1} vs. {team2}", key=f"finalize_12_{i}"):
        loser = team2 if winner == team1 else team1
        winner_points = points1 if winner == team1 else points2
        loser_points = points2 if winner == team1 else points1
        update_records(winner, loser, winner_points, loser_points, week_key=f"12_{i}")

# Sort standings after week 12
st.session_state.updated_records = st.session_state.updated_records.sort_values(
    by=['Wins', 'PF'], ascending=[False, False]).reset_index(drop=True)

# Display updated standings after Week 12
st.subheader("Standings After Week 12")
st.dataframe(st.session_state.updated_records)


# Week 13 Matchups
st.subheader("Week 13 Matchups")
week13_matchups = schedule[schedule['Week'] == 13]
for i, matchup in week13_matchups.iterrows():
    team1 = matchup['Team1']
    team2 = matchup['Team2']
    proj1 = matchup['Team1Proj']
    proj2 = matchup['Team2Proj']

    st.markdown(f"### {team1} vs. {team2}")

    # Select winner
    winner = st.radio(f"Select the winner for {team1} vs. {team2}:",
                      [team1, team2], key=f"winner_13_{i}")

    # Point entry option
    st.write(f"Projected Points: {team1} - {proj1:.2f}, {team2} - {proj2:.2f}")
    custom_points = st.checkbox(f"Enter custom points for {team1} vs. {team2}?", key=f"custom_points_13_{i}")

    if custom_points:
        # Custom points input with up to 2 decimal places
        points1 = st.number_input(f"Enter points for {team1}:", min_value=0.0, format="%.2f", key=f"points1_13_{i}")
        points2 = st.number_input(f"Enter points for {team2}:", min_value=0.0, format="%.2f", key=f"points2_13_{i}")
    else:
        # Use projected points
        points1 = round(proj1, 2)
        points2 = round(proj2, 2)

    # Finalize prediction
    if st.button(f"Finalize Winner for {team1} vs. {team2}", key=f"finalize_13_{i}"):
        loser = team2 if winner == team1 else team1
        winner_points = points1 if winner == team1 else points2
        loser_points = points2 if winner == team1 else points1
        update_records(winner, loser, winner_points, loser_points, week_key=f"13_{i}")

# Sort standings after week 13
st.session_state.updated_records = st.session_state.updated_records.sort_values(
    by=['Wins', 'PF'], ascending=[False, False]).reset_index(drop=True)

# Display updated standings after Week 13
st.subheader("Standings After Week 13")
st.dataframe(st.session_state.updated_records)


# Week 14 Matchups
st.subheader("Week 14 Matchups")
week14_matchups = schedule[schedule['Week'] == 14]
for i, matchup in week14_matchups.iterrows():
    team1 = matchup['Team1']
    team2 = matchup['Team2']
    proj1 = matchup['Team1Proj']
    proj2 = matchup['Team2Proj']

    st.markdown(f"### {team1} vs. {team2}")

    # Select winner
    winner = st.radio(f"Select the winner for {team1} vs. {team2}:",
                      [team1, team2], key=f"winner_14_{i}")

    # Point entry option
    st.write(f"Projected Points: {team1} - {proj1:.2f}, {team2} - {proj2:.2f}")
    custom_points = st.checkbox(f"Enter custom points for {team1} vs. {team2}?", key=f"custom_points_14_{i}")

    if custom_points:
        # Custom points input with up to 2 decimal places
        points1 = st.number_input(f"Enter points for {team1}:", min_value=0.0, format="%.2f", key=f"points1_14_{i}")
        points2 = st.number_input(f"Enter points for {team2}:", min_value=0.0, format="%.2f", key=f"points2_14_{i}")
    else:
        # Use projected points
        points1 = round(proj1, 2)
        points2 = round(proj2, 2)

    # Finalize prediction
    if st.button(f"Finalize Winner for {team1} vs. {team2}", key=f"finalize_14_{i}"):
        loser = team2 if winner == team1 else team1
        winner_points = points1 if winner == team1 else points2
        loser_points = points2 if winner == team1 else points1
        update_records(winner, loser, winner_points, loser_points, week_key=f"14_{i}")

# Sort standings after week 14
st.session_state.updated_records = st.session_state.updated_records.sort_values(
    by=['Wins', 'PF'], ascending=[False, False]).reset_index(drop=True)

# Display updated standings after Week 14
st.subheader("Final Standings After Week 14")
st.dataframe(st.session_state.updated_records)


