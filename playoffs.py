import numpy as np
import pandas as pd
import streamlit as st
pd.set_option('display.max_columns', None)
scores = pd.read_excel("Fantasy.xlsx", sheet_name="ScoringData")
records = pd.read_excel("Fantasy.xlsx", sheet_name="Records")
schedule = pd.read_excel("Fantasy.xlsx", sheet_name="Schedule")
playoffs = pd.read_excel("Fantasy.xlsx", sheet_name="Playoffs")
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
st.dataframe(summary_table)
