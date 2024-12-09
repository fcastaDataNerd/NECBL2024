import numpy as np
import pandas as pd

# Load final standings and playoff projections
final_standings = pd.read_excel("Fantasy.xlsx", sheet_name="Final")
playoffs = pd.read_excel("Fantasy.xlsx", sheet_name="Playoffs")

# Sort final standings by Wins (descending) and PF (descending)
final_standings = final_standings.sort_values(by=["Wins", "PF"], ascending=[False, False]).reset_index(drop=True)

# Extract playoff and toilet bowl teams
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

playoff_teams, toilet_bowl_teams = get_playoff_and_toilet_bowl_teams(final_standings)

# Simulate a single game
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

# Simulate a single round of matchups
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

# Simulate the playoff bracket
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

# Track playoff stats over multiple simulations
def simulate_season(playoff_teams, playoffs, std_dev, n_simulations=10000):
    """
    Simulate the playoffs multiple times and track stats.

    Args:
        playoff_teams (DataFrame): Teams in the playoffs.
        playoffs (DataFrame): Playoff projections (R1, R2, R3).
        std_dev (float): League-wide standard deviation.
        n_simulations (int): Number of simulations to run.

    Returns:
        DataFrame: Summary of playoff results.
    """
    # Initialize tracking
    team_stats = {team: {"Wins League": 0, "Advances to R2": 0, 
                         "Advances to R3": 0} for team in playoff_teams['Team']}
    
    for _ in range(n_simulations):
        # Simulate playoffs
        first_round_winners, _ = simulate_playoffs()
        for _ in range(n_simulations):
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
        
        # Simulate first round
        first_round_winners, _ = simulate_round(first_round_matchups, std_dev)
        
        # Track first round advancements
        for team in first_round_winners:
            team_stats[team]["Advances to R2"] += 1
        
        # Simulate second round
        second_round_matchups = [
            (first_round_winners[0], playoffs.loc[playoffs['Team'] == first_round_winners[0], 'R2'].values[0],
             first_round_winners[1], playoffs.loc[playoffs['Team'] == first_round_winners[1], 'R2'].values[0]),
            (first_round_winners[2], playoffs.loc[playoffs['Team'] == first_round_winners[2], 'R2'].values[0],
             first_round_winners[3], playoffs.loc[playoffs['Team'] == first_round_winners[3], 'R2'].values[0]),
        ]
        second_round_winners, _ = simulate_round(second_round_matchups, std_dev)
        
        # Track second round advancements
        for team in second_round_winners:
            team_stats[team]["Advances to R3"] += 1
        
        # Simulate championship
        championship_matchup = [
            (second_round_winners[0], playoffs.loc[playoffs['Team'] == second_round_winners[0], 'R3'].values[0],
             second_round_winners[1], playoffs.loc[playoffs['Team'] == second_round_winners[1], 'R3'].values[0]),
        ]
        championship_winner, _ = simulate_round(championship_matchup, std_dev)
        
        # Track championship win
        team_stats[championship_winner[0]]["Wins League"] += 1

    # Convert stats to percentages
    summary = []
    for team, stats in team_stats.items():
    summary.append({
            "Team": team,
            "Wins League (%)": (stats["Wins League"] / n_simulations) * 100,
            "Advances to R2 (%)": (stats["Advances to R2"] / n_simulations) * 100,
            "Advances to R3 (%)": (stats["Advances to R3"] / n_simulations) * 100,
        })

    return pd.DataFrame(summary)

# Define league-wide standard deviation
n_iterations = 1000
score_values = playoffs['R1']  # Assuming 'R1' column contains initial projections for teams
bootstrap_stds = [np.std(np.random.choice(score_values, size=len(score_values), replace=True)) for _ in range(n_iterations)]
league_std = np.mean(bootstrap_stds)

# Run the simulation
n_simulations = 10000
summary_table = simulate_season(playoff_teams, playoffs, league_std, n_simulations=n_simulations)

# Display the summary table
print(summary_table)


