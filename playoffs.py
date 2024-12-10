import numpy as np
import pandas as pd
import streamlit as st

# Load final standings and playoff projections
final_standings = pd.read_excel("Fantasy.xlsx", sheet_name="Final")
playoffs = pd.read_excel("Fantasy.xlsx", sheet_name="Playoffs")
scoring_data = pd.read_excel("Fantasy.xlsx", sheet_name="ScoringData")

# Sort final standings by Wins (descending) and PF (descending)
final_standings = final_standings.sort_values(by=["Wins", "PF"], ascending=[False, False]).reset_index(drop=True)

# Extract playoff and toilet bowl teams
def get_playoff_and_toilet_bowl_teams(final_standings):
    playoff_teams = final_standings.iloc[:8].reset_index(drop=True)
    toilet_bowl_teams = final_standings.iloc[-4:].reset_index(drop=True)
    return playoff_teams, toilet_bowl_teams

playoff_teams, toilet_bowl_teams = get_playoff_and_toilet_bowl_teams(final_standings)

# Simulate a single game
def simulate_game(projection1, projection2, std_dev):
    score1 = np.random.normal(loc=projection1, scale=std_dev)
    score2 = np.random.normal(loc=projection2, scale=std_dev)
    return score1, score2

# Simulate a single round of matchups
def simulate_round(matchups, std_dev):
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

# Simulate the playoff bracket
def simulate_playoffs(playoff_teams, playoffs_data, std_dev):
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

    second_round_matchups = [
        (first_round_winners[0], playoffs_data.loc[playoffs_data['Team'] == first_round_winners[0], 'R2'].values[0],
         first_round_winners[1], playoffs_data.loc[playoffs_data['Team'] == first_round_winners[1], 'R2'].values[0]),
        (first_round_winners[2], playoffs_data.loc[playoffs_data['Team'] == first_round_winners[2], 'R2'].values[0],
         first_round_winners[3], playoffs_data.loc[playoffs_data['Team'] == first_round_winners[3], 'R2'].values[0]),
    ]
    second_round_winners, _ = simulate_round(second_round_matchups, std_dev)

    championship_matchup = [
        (second_round_winners[0], playoffs_data.loc[playoffs_data['Team'] == second_round_winners[0], 'R3'].values[0],
         second_round_winners[1], playoffs_data.loc[playoffs_data['Team'] == second_round_winners[1], 'R3'].values[0]),
    ]
    championship_winner, _ = simulate_round(championship_matchup, std_dev)

    return championship_winner[0]  # Return the single winner of the championship

# Simulate the toilet bowl bracket
def simulate_toilet_bowl(toilet_bowl_teams, playoffs_data, std_dev):
    first_round_matchups = [
        (toilet_bowl_teams.iloc[0]['Team'], playoffs_data.loc[playoffs_data['Team'] == toilet_bowl_teams.iloc[0]['Team'], 'R1'].values[0],
         toilet_bowl_teams.iloc[3]['Team'], playoffs_data.loc[playoffs_data['Team'] == toilet_bowl_teams.iloc[3]['Team'], 'R1'].values[0]),
        (toilet_bowl_teams.iloc[1]['Team'], playoffs_data.loc[playoffs_data['Team'] == toilet_bowl_teams.iloc[1]['Team'], 'R1'].values[0],
         toilet_bowl_teams.iloc[2]['Team'], playoffs_data.loc[playoffs_data['Team'] == toilet_bowl_teams.iloc[2]['Team'], 'R1'].values[0]),
    ]
    _, first_round_losers = simulate_round(first_round_matchups, std_dev)

    # Final matchup between the two losers
    final_matchup = [
        (first_round_losers[0], playoffs_data.loc[playoffs_data['Team'] == first_round_losers[0], 'R2'].values[0],
         first_round_losers[1], playoffs_data.loc[playoffs_data['Team'] == first_round_losers[1], 'R2'].values[0]),
    ]
    _, toilet_bowl_loser = simulate_round(final_matchup, std_dev)

    return toilet_bowl_loser[0]  # Return the loser of the league

# Simulate playoffs and toilet bowl
def simulate_season(playoff_teams, toilet_bowl_teams, playoffs, std_dev, n_simulations=10000):
    team_stats = {team: {"Wins League": 0, "Loses League": 0} for team in final_standings['Team']}
    
    for _ in range(n_simulations):
        # Simulate playoffs
        champion = simulate_playoffs(playoff_teams, playoffs, std_dev)
        team_stats[champion]["Wins League"] += 1

        # Simulate toilet bowl
        loser = simulate_toilet_bowl(toilet_bowl_teams, playoffs, std_dev)
        team_stats[loser]["Loses League"] += 1

    # Convert stats to percentages
    summary = []
    for team, stats in team_stats.items():
        summary.append({
            "Team": team,
            "Wins League (%)": (stats["Wins League"] / n_simulations) * 100,
            "Loses League (%)": (stats["Loses League"] / n_simulations) * 100,
        })

    return pd.DataFrame(summary)

# Define league-wide standard deviation
score_values = scoring_data['Points']  # Replace 'Points' with actual column name in ScoringData
n_iterations = 1000
bootstrap_stds = [np.std(np.random.choice(score_values, size=len(score_values), replace=True)) for _ in range(n_iterations)]
league_std = np.mean(bootstrap_stds)

# Run the simulation
n_simulations = 10000
summary_table = simulate_season(playoff_teams, toilet_bowl_teams, playoffs, league_std, n_simulations)

# Display the summary table
st.write(summary_table)
