import streamlit as st
import pandas as pd
import numpy as np

# ====================================================================
# 1. LOAD 2025 DATA
# ====================================================================

st.title("2025 Fantasy Football — ROS Playoff Picture")
st.subheader("Simulate Weeks 12–14 and View Updated Standings")

DATA_PATH = DATA_PATH = "Fantasy2025.xlsx"

stats_df = pd.read_excel(DATA_PATH, sheet_name="Stats")
schedule_df = pd.read_excel(DATA_PATH, sheet_name="Schedule")

# Expected Stats columns:
# Team, Wins, PF, GP, MeanPF, TeamRank, Week 12, Week 13, Week 14, R1, R2, R3

# We only need Wins, PF for standings here
initial_records = stats_df[["Team", "Wins", "PF"]].copy()
initial_records["Loss"] = 11 - initial_records["Wins"]


# ====================================================================
# 2. INITIALIZE SESSION STATE
# ====================================================================

# Holds the fully updated standings as user interacts
if "records" not in st.session_state:
    st.session_state.records = initial_records.copy()

# Stores previous finalized prediction per matchup so they can be undone
if "finalized" not in st.session_state:
    st.session_state.finalized = {}

# Quick lookup of projected points for each week
proj_lookup = stats_df.set_index("Team")[["Week 12", "Week 13", "Week 14"]]


# ====================================================================
# 3. UNDO / APPLY LOGIC
# ====================================================================

def apply_outcome(winner, loser, w_pts, l_pts, key):
    """
    Handles undoing previous choice (if any), then applying the new one.
    """

    # -------------------------------------------------------
    # Undo old prediction if it exists for this matchup
    # -------------------------------------------------------
    if key in st.session_state.finalized:
        old_winner, old_loser, old_wp, old_lp = st.session_state.finalized[key]

        # reverse Wins/Losses
        st.session_state.records.loc[
            st.session_state.records["Team"] == old_winner, "Wins"
        ] -= 1
        st.session_state.records.loc[
            st.session_state.records["Team"] == old_loser, "Loss"
        ] -= 1

        # reverse PF
        st.session_state.records.loc[
            st.session_state.records["Team"] == old_winner, "PF"
        ] -= old_wp
        st.session_state.records.loc[
            st.session_state.records["Team"] == old_loser, "PF"
        ] -= old_lp

    # -------------------------------------------------------
    # Apply the new outcome
    # -------------------------------------------------------
    st.session_state.records.loc[
        st.session_state.records["Team"] == winner, "Wins"
    ] += 1
    st.session_state.records.loc[
        st.session_state.records["Team"] == loser, "Loss"
    ] += 1

    st.session_state.records.loc[
        st.session_state.records["Team"] == winner, "PF"
    ] += w_pts
    st.session_state.records.loc[
        st.session_state.records["Team"] == loser, "PF"
    ] += l_pts

    # Store new choice
    st.session_state.finalized[key] = (winner, loser, w_pts, l_pts)


# ====================================================================
# 4. HANDLE A SINGLE WEEK'S MATCHUPS
# ====================================================================

def simulate_week(week):
    st.header(f"Week {week}")

    week_games = schedule_df[schedule_df["Week"] == week]

    for i, game in week_games.iterrows():
        team1 = game["Team1"]
        team2 = game["Team2"]

        proj1 = proj_lookup.loc[team1, f"Week {week}"]
        proj2 = proj_lookup.loc[team2, f"Week {week}"]

        st.subheader(f"{team1} vs {team2}")
        st.write(f"Projected: {team1} **{proj1:.2f}** | {team2} **{proj2:.2f}**")

        # Choose winner
        winner = st.radio(
            f"Winner ({team1} vs {team2})",
            [team1, team2],
            key=f"winner_{week}_{i}"
        )

        use_custom = st.checkbox(
            f"Enter custom points for this matchup?",
            key=f"custom_{week}_{i}"
        )

        if use_custom:
            pts1 = st.number_input(
                f"{team1} points", min_value=0.0, step=0.1,
                key=f"pts1_{week}_{i}"
            )
            pts2 = st.number_input(
                f"{team2} points", min_value=0.0, step=0.1,
                key=f"pts2_{week}_{i}"
            )
        else:
            pts1 = float(proj1)
            pts2 = float(proj2)

        # Finalize button
        if st.button(f"Finalize {team1} vs {team2}", key=f"final_btn_{week}_{i}"):

            loser = team2 if winner == team1 else team1
            w_pts = pts1 if winner == team1 else pts2
            l_pts = pts2 if winner == team1 else pts1

            apply_outcome(winner, loser, w_pts, l_pts, key=f"{week}_{i}")

    # Resort standings after every week
    st.session_state.records = st.session_state.records.sort_values(
        ["Wins", "PF"], ascending=[False, False]
    ).reset_index(drop=True)

    st.subheader(f"Standings After Week {week}")
    st.dataframe(st.session_state.records)


# ====================================================================
# 5. DISPLAY FLOW: WEEK 12 → WEEK 13 → WEEK 14
# ====================================================================

simulate_week(12)
simulate_week(13)
simulate_week(14)

st.header("Final Standings After Week 14")
st.dataframe(st.session_state.records)
