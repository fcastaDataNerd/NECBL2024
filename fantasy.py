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
print()
st.subheader("The worst player in league history")
st.image("Screenshot (1397).png", use_column_width=True)
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
st.subheader("The face of the mouse god one seed")
st.image("Screenshot (1394).png", use_column_width=True)

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
st.subheader("Mike Sawyer preparing for a voodoo style playoff run")
st.image("Screenshot (1395).png", use_column_width=True)

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
# Load data and historical scores
scores = pd.read_excel("C:\\Users\\Franco Castagliuolo\\OneDrive - Bentley University\\Fantasy.xlsx", sheet_name="ScoringData")
records = pd.read_excel("C:\\Users\\Franco Castagliuolo\\OneDrive - Bentley University\\Fantasy.xlsx", sheet_name="Records")
schedule = pd.read_excel("C:\\Users\\Franco Castagliuolo\\OneDrive - Bentley University\\Fantasy.xlsx", sheet_name="Schedule")
playoffs = pd.read_excel("C:\\Users\\Franco Castagliuolo\\OneDrive - Bentley University\\Fantasy.xlsx", sheet_name="Playoffs")
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

def get_playoff_and_toilet_bowl_teams(final_standings):
    """
    Extract playoff and toilet bowl teams from final standings.

    Args:
        final_standings (DataFrame): Sorted standings after the regular season.

    Returns:
        tuple: (playoff_teams, toilet_bowl_teams)
    """
    # Top 8 teams for playoffs
    playoff_teams = final_standings.iloc[:8].reset_index(drop=True)

    # Bottom 4 teams for the toilet bowl
    toilet_bowl_teams = final_standings.iloc[-4:].reset_index(drop=True)

    return playoff_teams, toilet_bowl_teams

# Extract playoff and toilet bowl teams
playoff_teams, toilet_bowl_teams = get_playoff_and_toilet_bowl_teams(final_standings)

# Display the playoff and toilet bowl teams
print("Playoff Teams:")
print(playoff_teams)
print("\nToilet Bowl Teams:")
print(toilet_bowl_teams)

def simulate_round(matchups, std_dev):
    """
    Simulate a single round of matchups.

    Args:
        matchups (list of tuples): List of matchups, where each tuple contains (team1, proj1, team2, proj2).
        std_dev (float): League-wide standard deviation for score variability.

    Returns:
        list: Winners and losers of the round.
    """
    winners = []
    losers = []
    for team1, proj1, team2, proj2 in matchups:
        score1, score2 = simulate_game(proj1, proj2, std_dev)
        if score1 > score2:
            winners.append(team1)
            losers.append(team2)
        else:
            winners.append(team2)
            losers.append(team1)
    return winners, losers


def simulate_playoffs(playoff_teams, playoffs_data, std_dev):
    """
    Simulate the playoff bracket using projections from the playoffs sheet.

    Args:
        playoff_teams (DataFrame): DataFrame of the top 8 teams in the playoffs.
        playoffs_data (DataFrame): DataFrame with R1, R2, and R3 projections for all teams.
        std_dev (float): League-wide standard deviation for score variability.

    Returns:
        str: The champion of the league.
    """
    # First-round matchups
    first_round_matchups = [
        (playoff_teams.iloc[0]['Team'], playoffs_data.loc[playoffs_data['Team'] == playoff_teams.iloc[0]['Team'], 'R1'].values[0],
         playoff_teams.iloc[7]['Team'], playoffs_data.loc[playoffs_data['Team'] == playoff_teams.iloc[7]['Team'], 'R1'].values[0]),
        (playoff_teams.iloc[1]['Team'], playoffs_data.loc[playoffs_data['Team'] == playoff_teams.iloc[1]['Team'], 'R1'].values[0],
         playoff_teams.iloc[6]['Team'], playoffs_data.loc[playoffs_data['Team'] == playoff_teams.iloc[6]['Team'], 'R1'].values[0]),
        (playoff_teams.iloc[2]['Team'], playoffs_data.loc[playoffs_data['Team'] == playoff_teams.iloc[2]['Team'], 'R1'].values[0],
         playoff_teams.iloc[5]['Team'], playoffs_data.loc[playoffs_data['Team'] == playoff_teams.iloc[5]['Team'], 'R1'].values[0]),
        (playoff_teams.iloc[3]['Team'], playoffs_data.loc[playoffs_data['Team'] == playoff_teams.iloc[3]['Team'], 'R1'].values[0],
         playoff_teams.iloc[4]['Team'], playoffs_data.loc[playoffs_data['Team'] == playoff_teams.iloc[4]['Team'], 'R1'].values[0]),
    ]
    first_round_winners, _ = simulate_round(first_round_matchups, std_dev)

    # Second-round matchups
    second_round_matchups = [
        (first_round_winners[0], playoffs_data.loc[playoffs_data['Team'] == first_round_winners[0], 'R2'].values[0],
         first_round_winners[1], playoffs_data.loc[playoffs_data['Team'] == first_round_winners[1], 'R2'].values[0]),
        (first_round_winners[2], playoffs_data.loc[playoffs_data['Team'] == first_round_winners[2], 'R2'].values[0],
         first_round_winners[3], playoffs_data.loc[playoffs_data['Team'] == first_round_winners[3], 'R2'].values[0]),
    ]
    second_round_winners, _ = simulate_round(second_round_matchups, std_dev)

    # Championship matchup
    championship_matchup = [
        (second_round_winners[0], playoffs_data.loc[playoffs_data['Team'] == second_round_winners[0], 'R3'].values[0],
         second_round_winners[1], playoffs_data.loc[playoffs_data['Team'] == second_round_winners[1], 'R3'].values[0]),
    ]
    championship_winner, _ = simulate_round(championship_matchup, std_dev)

    return championship_winner[0]  # Return the single winner of the championship


def simulate_toilet_bowl(toilet_bowl_teams, playoffs_data, std_dev):
    """
    Simulate the toilet bowl bracket using projections from the playoffs sheet.

    Args:
        toilet_bowl_teams (DataFrame): DataFrame of the bottom 4 teams in the toilet bowl.
        playoffs_data (DataFrame): DataFrame with R1 and R2 projections for all teams.
        std_dev (float): League-wide standard deviation for score variability.

    Returns:
        str: The loser of the league.
    """
    # First-round matchups
    first_round_matchups = [
        (toilet_bowl_teams.iloc[0]['Team'], playoffs_data.loc[playoffs_data['Team'] == toilet_bowl_teams.iloc[0]['Team'], 'R1'].values[0],
         toilet_bowl_teams.iloc[3]['Team'], playoffs_data.loc[playoffs_data['Team'] == toilet_bowl_teams.iloc[3]['Team'], 'R1'].values[0]),
        (toilet_bowl_teams.iloc[1]['Team'], playoffs_data.loc[playoffs_data['Team'] == toilet_bowl_teams.iloc[1]['Team'], 'R1'].values[0],
         toilet_bowl_teams.iloc[2]['Team'], playoffs_data.loc[playoffs_data['Team'] == toilet_bowl_teams.iloc[2]['Team'], 'R1'].values[0]),
    ]
    first_round_winners, first_round_losers = simulate_round(first_round_matchups, std_dev)

    # Final matchup (losers of the first round)
    final_matchup = [
        (first_round_losers[0], playoffs_data.loc[playoffs_data['Team'] == first_round_losers[0], 'R2'].values[0],
         first_round_losers[1], playoffs_data.loc[playoffs_data['Team'] == first_round_losers[1], 'R2'].values[0]),
    ]
    final_winners, final_losers = simulate_round(final_matchup, std_dev)

    # Return the final loser as the league loser
    return final_losers[0]

# Simulate playoffs
league_champion = simulate_playoffs(playoff_teams, playoffs, league_std)
print(f"The league champion is: {league_champion}")

# Simulate toilet bowl
league_loser = simulate_toilet_bowl(toilet_bowl_teams, playoffs, league_std)
print(f"The league loser is: {league_loser}")


def simulate_season_10000(schedule, records, playoffs, league_std, n_simulations=10000):
    """
    Simulate the entire season and calculate percentages for milestones.

    Args:
        schedule (DataFrame): Regular season schedule.
        records (DataFrame): Team records at the start of the season.
        playoffs (DataFrame): Playoffs projections for R1, R2, and R3.
        league_std (float): League-wide standard deviation for score variability.
        n_simulations (int): Number of simulations to run.

    Returns:
        DataFrame: Summary table with percentage stats for each team.
    """
    # Initialize trackers
    team_stats = {team: {"Wins League": 0, "Makes Playoffs": 0, "Advances to R2": 0, 
                         "Advances to R3": 0, "Loses League": 0} for team in records['Team']}
    
    for sim in range(n_simulations):
        # Debug print to track progress
        if sim % 10 == 0:  # Print progress every 10 simulations
            print(f"Simulation {sim + 1} of {n_simulations}...")

        # Simulate the regular season
        final_standings = simulate_regular_season(schedule, records, league_std)
        
        # Get playoff and toilet bowl teams
        playoff_teams, toilet_bowl_teams = get_playoff_and_toilet_bowl_teams(final_standings)

        # Track teams that make playoffs
        for team in playoff_teams['Team']:
            team_stats[team]["Makes Playoffs"] += 1

        # Simulate playoffs
        first_round_matchups = [
            (playoff_teams.iloc[0]['Team'], playoffs.loc[playoffs['Team'] == playoff_teams.iloc[0]['Team'], 'R1'].values[0],
             playoff_teams.iloc[7]['Team'], playoffs.loc[playoffs['Team'] == playoff_teams.iloc[7]['Team'], 'R1'].values[0]),
            (playoff_teams.iloc[1]['Team'], playoffs.loc[playoffs['Team'] == playoff_teams.iloc[1]['Team'], 'R1'].values[0],
             playoff_teams.iloc[6]['Team'], playoffs.loc[playoffs['Team'] == playoff_teams.iloc[6]['Team'], 'R1'].values[0]),
            (playoff_teams.iloc[2]['Team'], playoffs.loc[playoffs['Team'] == playoff_teams.iloc[2]['Team'], 'R1'].values[0],
             playoff_teams.iloc[5]['Team'], playoffs.loc[playoffs['Team'] == playoff_teams.iloc[5]['Team'], 'R1'].values[0]),
            (playoff_teams.iloc[3]['Team'], playoffs.loc[playoffs['Team'] == playoff_teams.iloc[3]['Team'], 'R1'].values[0],
             playoff_teams.iloc[4]['Team'], playoffs.loc[playoffs['Team'] == playoff_teams.iloc[4]['Team'], 'R1'].values[0]),
        ]

        # Track teams that advance to R2
        first_round_winners, _ = simulate_round(first_round_matchups, league_std)
        for team in first_round_winners:
            team_stats[team]["Advances to R2"] += 1

        # Second-round matchups
        second_round_matchups = [
            (first_round_winners[0], playoffs.loc[playoffs['Team'] == first_round_winners[0], 'R2'].values[0],
             first_round_winners[1], playoffs.loc[playoffs['Team'] == first_round_winners[1], 'R2'].values[0]),
            (first_round_winners[2], playoffs.loc[playoffs['Team'] == first_round_winners[2], 'R2'].values[0],
             first_round_winners[3], playoffs.loc[playoffs['Team'] == first_round_winners[3], 'R2'].values[0]),
        ]

        # Track teams that advance to R3
        second_round_winners, _ = simulate_round(second_round_matchups, league_std)
        for team in second_round_winners:
            team_stats[team]["Advances to R3"] += 1

        # Championship matchup
        championship_matchup = [
            (second_round_winners[0], playoffs.loc[playoffs['Team'] == second_round_winners[0], 'R3'].values[0],
             second_round_winners[1], playoffs.loc[playoffs['Team'] == second_round_winners[1], 'R3'].values[0]),
        ]
        championship_winner, _ = simulate_round(championship_matchup, league_std)

        # Track league champion
        team_stats[championship_winner[0]]["Wins League"] += 1

        # Simulate toilet bowl
        first_round_matchups_toilet_bowl = [
            (toilet_bowl_teams.iloc[0]['Team'], playoffs.loc[playoffs['Team'] == toilet_bowl_teams.iloc[0]['Team'], 'R1'].values[0],
             toilet_bowl_teams.iloc[3]['Team'], playoffs.loc[playoffs['Team'] == toilet_bowl_teams.iloc[3]['Team'], 'R1'].values[0]),
            (toilet_bowl_teams.iloc[1]['Team'], playoffs.loc[playoffs['Team'] == toilet_bowl_teams.iloc[1]['Team'], 'R1'].values[0],
             toilet_bowl_teams.iloc[2]['Team'], playoffs.loc[playoffs['Team'] == toilet_bowl_teams.iloc[2]['Team'], 'R1'].values[0]),
        ]
        first_round_losers = simulate_round(first_round_matchups_toilet_bowl, league_std)[1]

        toilet_bowl_matchup = [
            (first_round_losers[0], playoffs.loc[playoffs['Team'] == first_round_losers[0], 'R2'].values[0],
             first_round_losers[1], playoffs.loc[playoffs['Team'] == first_round_losers[1], 'R2'].values[0]),
        ]
        league_loser = simulate_round(toilet_bowl_matchup, league_std)[1][0]

        # Track league loser
        team_stats[league_loser]["Loses League"] += 1

    # Convert stats to percentages
    stats_summary = []
    for team, stats in team_stats.items():
        stats_summary.append({
            "Team": team,
            "Wins League (%)": (stats["Wins League"] / n_simulations) * 100,
            "Makes Playoffs (%)": (stats["Makes Playoffs"] / n_simulations) * 100,
            "Advances to R2 (%)": (stats["Advances to R2"] / n_simulations) * 100,
            "Advances to R3 (%)": (stats["Advances to R3"] / n_simulations) * 100,
            "Loses League (%)": (stats["Loses League"] / n_simulations) * 100,
        })

    return pd.DataFrame(stats_summary)


# Reduce number of simulations for testing
summary_table = simulate_season_10000(schedule, records, playoffs, league_std, n_simulations=1000)

# Display the summary table

st.subheader("Current Playoff Estimates")
print(summary_table)




