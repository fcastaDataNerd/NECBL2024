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
st.header("Greetings, gentlemen. Discover your tanking scenarios below")
print()
print()
print()



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

st.subheader("Your face when Max Zornada surges at the end of the year to eliminate you from playoff contention")
st.image("Screenshot (1393).png", use_column_width=True)



import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
print(records)
print(scores)
print(schedule)

score_values = scores['Points']  # Replace 'Points' with the actual column name if different
n_iterations = 1000
bootstrap_stds = [np.std(np.random.choice(score_values, size=len(score_values), replace=True)) for _ in range(n_iterations)]
league_std = np.mean(bootstrap_stds)

def simulate_game(projection1, projection2, std_dev):
    """
    Simulate a single game given two projections and league-wide standard deviation.
    
    Args:
        projection1 (float): Projected score for team 1.
        projection2 (float): Projected score for team 2.
        std_dev (float): League-wide standard deviation for score variability.

    Returns:
        tuple: Simulated scores for team 1 and team 2.
    """
    score1 = np.random.normal(loc=projection1, scale=std_dev)
    score2 = np.random.normal(loc=projection2, scale=std_dev)
    return score1, score2


def simulate_regular_season(schedule, records, std_dev):
    """
    Simulate all games in the regular season (Weeks 12-14) and update records.

    Args:
        schedule (DataFrame): Weekly matchups with projections.
        records (DataFrame): Existing records with Wins, Loss, and PF.
        std_dev (float): League-wide standard deviation for score variability.

    Returns:
        DataFrame: Sorted standings based on Wins and PF after Weeks 12-14.
    """
    # Create a copy of the records to retain the original data
    updated_records = records.copy()

    # Loop through each game in the schedule
    for _, game in schedule.iterrows():
        # Extract team names and projections
        team1 = game['Team1']
        team2 = game['Team2']
        proj1 = game['Team1Proj']
        proj2 = game['Team2Proj']

        # Simulate the game
        score1, score2 = simulate_game(proj1, proj2, std_dev)

        # Update Points For (PF)
        updated_records.loc[updated_records['Team'] == team1, 'PF'] += score1
        updated_records.loc[updated_records['Team'] == team2, 'PF'] += score2

        # Update Wins and Losses
        if score1 > score2:
            updated_records.loc[updated_records['Team'] == team1, 'Wins'] += 1
            updated_records.loc[updated_records['Team'] == team2, 'Loss'] += 1
        else:
            updated_records.loc[updated_records['Team'] == team2, 'Wins'] += 1
            updated_records.loc[updated_records['Team'] == team1, 'Loss'] += 1

    # Sort the standings by Wins (descending) and PF (descending)
    updated_records = updated_records.sort_values(by=['Wins', 'PF'], ascending=[False, False]).reset_index(drop=True)

    return updated_records
# Simulate the regular season (Weeks 12-14) and sort standings
final_standings = simulate_regular_season(schedule, records, league_std)

# Display the final standings
print(final_standings)





