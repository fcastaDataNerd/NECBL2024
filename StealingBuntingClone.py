import pandas as pd
import streamlit as st

file = "C:\\Users\\Franco Castagliuolo\\OneDrive - Bentley University\\GitHubPython\\Exports.xlsx"

def excel(file, sheet):
    data = pd.read_excel(file, sheet)
    return data

xWA = excel(file, "xWA")
xSteal = excel(file, "xSteal")
xZones = excel(file, "xZones")
xSteal = pd.concat([xSteal, xZones], axis=1)
WA1S = excel(file, "WA1S")
Z1S = excel(file, "Z1S")
WA2S = excel(file, "WA2S")
Z2S = excel(file, "Z2S")
WA3S = excel(file, "WA3S")
Z3S = excel(file, "Z3S")
BMAX = excel(file, "BMAX")
B1 = excel(file, "B1")
B2 = excel(file, "B2")
BVALS = excel(file, "BVALS")
B10 = excel(file, "B10")
B20 = excel(file, "B20")
B120 = excel(file, "B120")
squeeze = excel(file, "Squeeze")
projections = excel(file, "Projections")

players = {
    "Lucas Manning": 22 / 23,
    "Jake Walman(NA stealing)": 0/1,
    "Nathan Waugh(NA stealing)": 0/1,
    "Casey Bishop": 29 / 32,
    "Max Jensen": 13 / 14,
    "David Michael Jefferson": 38 / 43,
    "Carlos Martinez(small steal sample)": 5 / 8,
    "Nic Notarangelo": 32 / 40,
    "Cam Santerre": 142 / 158,
    "Johnny Luetzow (small steal sample)": 5 / 8,
    "Samuel Angelo": 16 / 19,
    "Braxton Meguiar": 65 / 81,
    "Josean Sanchez": 8 / 10,
    "Beau Root": 50/58,
    "Johnny Knox": 38/49
    
}

def get_steal_data(data, runners, outs, location=None):
    # Filter the data based on user input
    if location:
        return data[(data['Runners'] == runners) & (data['Outs'] == outs) & (data['Location'] == location)]
    else:
        return data[(data['Runners'] == runners) & (data['Outs'] == outs)]

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Dictionary", "Stealing (Max)", "Stealing (1 Run)", "Stealing (2 Runs)", "Stealing (3 Runs)", "Bunting"])

if page == "Stealing (Max)":
    st.title("Run Maximization Guide")
    selected_player = st.selectbox("Select Player", list(players.keys()))
    runners = st.text_input("Enter the runners on base (e.g., '1', '13', '123'):")
    outs = st.number_input("Enter the number of outs:", min_value=0, max_value=2, step=1)
    # Conditional input for location if runners include '12'
    location = None
    base = None
    if '12' in runners:
        location = st.selectbox("Select the location:", ['Double', '3rd'])
        if location == "Double":
            base = st.selectbox("Are we focusing on the runner stealing 2nd or 3rd?", ["2nd", "3rd"])
    runners = int(runners)
    # Button to fetch and display data
    if st.button('Get Steal Information'):
        if base == "2nd":
            location = "Double (2nd)"
        result = get_steal_data(xSteal, runners, outs, location)
        st.write(f"{selected_player}: {players[selected_player]:.2%}")
        conf = result.iloc[0]['AVG Confidence']
        SB = result.iloc[0]["SB Value"]
        SBMax = result.iloc[0]["Max SB"]
        SBMin = result.iloc[0]["Min SB"]
        CS = result.iloc[0]["CS Value"]
        CSMax = result.iloc[0]["CS max"]
        CSMin = result.iloc[0]["CS min"]
        spread = players[selected_player] - conf
        st.write(f"Breakeven Rate: {round(conf*100, 2)}%")  # Assuming 'conf' is already in percentage format
        st.write(f"Advantage/Disadvantage Spread: {round(spread*100, 2)}%")
        st.write(f"Successful steal nets us {round(SB, 2)} ({round(SBMax, 2)} , {round(SBMin, 2)}) runs")
        st.write(f"Caught stealing costs us {round(CS, 2)} ({round(CSMax, 2)} , {round(CSMin, 2)}) runs")
        steal_percentage = players[selected_player]
        tilt_minY = result.iloc[0]['Tilt min']
        tilt_maxY = result.iloc[0]['Tilt max']
        lean_minY = result.iloc[0]['Lean min']
        lean_maxY = result.iloc[0]['Lean max']
        likely_minY = result.iloc[0]['Likely min']
        likely_maxY = result.iloc[0]['Likely max']
        tilt_minN = result.iloc[0]['Tilt min.1']
        tilt_maxN = result.iloc[0]['Tilt max.1']
        lean_minN = result.iloc[0]['Lean min.1']
        lean_maxN = result.iloc[0]['Lean max.1']
        likely_minN = result.iloc[0]['Likely min.1']
        likely_maxN = result.iloc[0]['Likely max.1']
        if tilt_minY <= steal_percentage <= tilt_maxY:
            recommendation = 'Tilt Steal'
        elif lean_minY <= steal_percentage <= lean_maxY:
            recommendation = 'Lean Steal'
        elif likely_minY <= steal_percentage <= likely_maxY:
            recommendation = 'Likely Steal'
        elif steal_percentage > likely_maxY:
            recommendation = 'Safe Steal'
        elif tilt_minN >= steal_percentage >= tilt_maxN:
            recommendation = "Tilt Stay"
        elif lean_minN >= steal_percentage >= lean_maxN:
            recommendation = "Lean Stay"
        elif likely_minN >= steal_percentage >= likely_maxN:
            recommendation = "Likely Stay"
        elif steal_percentage < likely_maxN:
            recommendation = "Safe Stay"
        st.header(f"Recommendation: {recommendation}")
        projected = (SB*steal_percentage)+(CS*(1-steal_percentage))
        st.write(f"Projected Gain/Loss if Attempted: {round(projected, 3)}")
        pivot_table = pd.pivot_table(xWA, values='Weighted Average', index='Runners', columns='Outs', aggfunc='first')
        pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
        pivot_table = pivot_table.round(2)
        custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
        pivot_table = pivot_table.reindex(custom_order)
        st.subheader("The Run Expectancy Matrix")
        st.write(pivot_table)

elif page == "Dictionary":
    st.title("Dictionary")
    st.write("Breakeven Rate: % of the time we must be successful in the baserunner/out state to net runs over a large sample.")
    st.write("Advantage/Disadvantage Spread: Just player SB%-Breakeven%. Represents the advantage or disadvantage we have compared to breakeven rate.")
    st.write("Successful steal net: The first value is the mean runs we would gain if the steal is successful. The two numbers in the parenthesis represent the 95% confidence interval for the mean. We only have run expectancy data for 2023 and 2024. Because we don't know the true mean gain in runs (average over all of NECBL history) we use a confidence interval to estimate. We could conceivably be gaining anywhere from the first value to the second value if the steal is successful, but the most true number is more likely to hover somewhere close to the mean")
    st.write("Caught stealing cost: Same structure as the successful steal. The first value is the mean runs we lose if caught, first number in parenthesis is the maximum and the second is the minimum")
    st.subheader("Recommendations:")
    st.write("Tilt steal/bunt: scenarios that marginally suggest a steal/bunt and should only be executed if there are no perceived disadvantages that I cannot numerically adjust for (pitcher and catcher speed of delivery, injuries, weather)")
    st.write("Lean steal/bunt: scenarios that with moderate strength suggest a steal/bunt. Perceived disadvantages would have to be somewhat significant to elect not to execute the steal/bunt.")
    st.write("Likely steal/bunt: scenarios that strongly suggest steal/bunt. The extenuating circumstances would have to be significant to elect not to execute the steal/bunt.")
    st.write("Safe steal/bunt: in these rare circumstances, the steal/bunt should be executed regardless of any perceived disadvantages. The data is so overwhelming in favor of stealing/bunting with this categorization that it is extremely unlikely for any circumstance to nullify the advantage of stealing/bunting.")
    st.write("Tilt stay/no bunt: scenarios that marginally suggest to stay/play it out, but a steal/bunt is recommended if perceived advantages exist.")
    st.write("Lean stay/no bunt: scenarios that with moderate strength suggest to avoid stealing/bunting. Perceived advantages would have to be somewhat significant to execute a steal/bunt.")
    st.write("Likely stay/no bunt: scenarios that strongly suggest avoiding a steal/bunt. A steal/bunt should only be executed if the perceived advantages are significant.")
    st.write("Safe stay/no bunt: The steal/bunt should not be executed regardless of how apparent the perceived advantages are.")
    st.write("Projected Gain/Loss: The mean runs to be gained over a large sample size if we were to steal in this situation factoring in the player. Projected=(SB value x steal%)+(CS value x (1-steal%))")
    st.write("Run Expectancy Matrix: Each cell represents the mean runs scored or odds to score at least 1 in an inning by NECBL teams in 2023 and 2024 from the time that situation occurred until the end of the inning, appropriately giving more weight to 2024 samples.")

elif page == "Stealing (1 Run)":
    st.title("1 Run Guide")
    selected_player = st.selectbox("Select Player", list(players.keys()))
    runners = st.text_input("Enter the runners on base (e.g., '1', '13', '123'):")
    outs = st.number_input("Enter the number of outs:", min_value=0, max_value=2, step=1)
    location = None
    base = None
    if '12' in runners:
        location = st.selectbox("Select the location:", ['Double', '3rd'])
        if location == "Double":
            base = st.selectbox("Are we focusing on the runner stealing 2nd or 3rd?", ["2nd", "3rd"])
    runners = int(runners)
    if st.button('Get Steal Information'):
        if base == "2nd":
            location = "Double (2nd)"
        result = get_steal_data(Z1S, runners, outs, location)
        st.write(f"{selected_player}: {players[selected_player]:.2%}")
        conf = result.iloc[0]['AVG Confidence']
        SB = result.iloc[0]["SB Value"]
        SBMax = result.iloc[0]["Max SB"]
        SBMin = result.iloc[0]["Min SB"]
        CS = result.iloc[0]["CS Value"]
        CSMax = result.iloc[0]["CS max"]
        CSMin = result.iloc[0]["CS min"]
        spread = players[selected_player] - conf
        st.write(f"Breakeven Rate: {round(conf*100, 2)}%")  # Assuming 'conf' is already in percentage format
        st.write(f"Advantage/Disadvantage Spread: {round(spread*100, 2)}%")
        st.write(f"Successful steal improves odds to score 1 by {round(SB*100, 2)}% ({round(SBMax*100, 2)}% , {round(SBMin*100, 2)}%)")
        st.write(f"Caught stealing decreases odds to score 1 by {round(CS*100, 2)}% ({round(CSMax*100, 2)}% , {round(CSMin*100, 2)}%)")
        steal_percentage = players[selected_player]
        tilt_minY = result.iloc[0]['Tilt min']
        tilt_maxY = result.iloc[0]['Tilt max']
        lean_minY = result.iloc[0]['Lean min']
        lean_maxY = result.iloc[0]['Lean max']
        likely_minY = result.iloc[0]['Likely min']
        likely_maxY = result.iloc[0]['Likely max']
        tilt_minN = result.iloc[0]['Tilt min.1']
        tilt_maxN = result.iloc[0]['Tilt max.1']
        lean_minN = result.iloc[0]['Lean min.1']
        lean_maxN = result.iloc[0]['Lean max.1']
        likely_minN = result.iloc[0]['Likely min.1']
        likely_maxN = result.iloc[0]['Likely max.1']
        if tilt_minY <= steal_percentage <= tilt_maxY:
            recommendation = 'Tilt Steal'
        elif lean_minY <= steal_percentage <= lean_maxY:
            recommendation = 'Lean Steal'
        elif likely_minY <= steal_percentage <= likely_maxY:
            recommendation = 'Likely Steal'
        elif steal_percentage > likely_maxY:
            recommendation = 'Safe Steal'
        elif tilt_minN >= steal_percentage >= tilt_maxN:
            recommendation = "Tilt Stay"
        elif lean_minN >= steal_percentage >= lean_maxN:
            recommendation = "Lean Stay"
        elif likely_minN >= steal_percentage >= likely_maxN:
            recommendation = "Likely Stay"
        elif steal_percentage < likely_maxN:
            recommendation = "Safe Stay"
        st.header(f"Recommendation: {recommendation}")
        projected = (SB*steal_percentage)+(CS*(1-steal_percentage))
        st.write(f"Projected Gain/Loss if Attempted: {round(projected*100, 2)}%")
        pivot_table = pd.pivot_table(WA1S, values='WeightedProb', index='Runners', columns='Outs', aggfunc='first')
        pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
        pivot_table = pivot_table*100
        custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
        pivot_table = pivot_table.reindex(custom_order)
        pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%")
        st.subheader("The 1 Run Probability Matrix")
        st.write(pivot_table)

elif page == "Stealing (2 Runs)":
    st.title("2 Run Guide")
    selected_player = st.selectbox("Select Player", list(players.keys()))
    runners = st.text_input("Enter the runners on base (e.g., '1', '13', '123'):")
    outs = st.number_input("Enter the number of outs:", min_value=0, max_value=2, step=1)
    location = None
    base = None
    if '12' in runners:
        location = st.selectbox("Select the location:", ['Double', '3rd'])
        if location == "Double":
            base = st.selectbox("Are we focusing on the runner stealing 2nd or 3rd?", ["2nd", "3rd"])
    runners = int(runners)
    if st.button('Get Steal Information'):
        if base == "2nd":
            location = "Double (2nd)"
        result = get_steal_data(Z2S, runners, outs, location)
        st.write(f"{selected_player}: {players[selected_player]:.2%}")
        conf = result.iloc[0]['AVG Confidence']
        SB = result.iloc[0]["SB Value"]
        SBMax = result.iloc[0]["Max SB"]
        SBMin = result.iloc[0]["Min SB"]
        CS = result.iloc[0]["CS Value"]
        CSMax = result.iloc[0]["CS max"]
        CSMin = result.iloc[0]["CS min"]
        spread = players[selected_player] - conf
        st.write(f"Breakeven Rate: {round(conf*100, 2)}%")  # Assuming 'conf' is already in percentage format
        st.write(f"Advantage/Disadvantage Spread: {round(spread*100, 2)}%")
        st.write(f"Successful steal improves odds to score 2 by {round(SB*100, 2)}% ({round(SBMax*100, 2)}% , {round(SBMin*100, 2)}%)")
        st.write(f"Caught stealing decreases odds to score 2 by {round(CS*100, 2)}% ({round(CSMax*100, 2)}% , {round(CSMin*100, 2)}%)")
        steal_percentage = players[selected_player]
        tilt_minY = result.iloc[0]['Tilt min']
        tilt_maxY = result.iloc[0]['Tilt max']
        lean_minY = result.iloc[0]['Lean min']
        lean_maxY = result.iloc[0]['Lean max']
        likely_minY = result.iloc[0]['Likely min']
        likely_maxY = result.iloc[0]['Likely max']
        tilt_minN = result.iloc[0]['Tilt min.1']
        tilt_maxN = result.iloc[0]['Tilt max.1']
        lean_minN = result.iloc[0]['Lean min.1']
        lean_maxN = result.iloc[0]['Lean max.1']
        likely_minN = result.iloc[0]['Likely min.1']
        likely_maxN = result.iloc[0]['Likely max.1']
        if tilt_minY <= steal_percentage <= tilt_maxY:
            recommendation = 'Tilt Steal'
        elif lean_minY <= steal_percentage <= lean_maxY:
            recommendation = 'Lean Steal'
        elif likely_minY <= steal_percentage <= likely_maxY:
            recommendation = 'Likely Steal'
        elif steal_percentage > likely_maxY:
            recommendation = 'Safe Steal'
        elif tilt_minN >= steal_percentage >= tilt_maxN:
            recommendation = "Tilt Stay"
        elif lean_minN >= steal_percentage >= lean_maxN:
            recommendation = "Lean Stay"
        elif likely_minN >= steal_percentage >= likely_maxN:
            recommendation = "Likely Stay"
        elif steal_percentage < likely_maxN:
            recommendation = "Safe Stay"
        st.header(f"Recommendation: {recommendation}")
        projected = (SB*steal_percentage)+(CS*(1-steal_percentage))
        st.write(f"Projected Gain/Loss if Attempted: {round(projected*100, 2)}%")
        pivot_table = pd.pivot_table(WA2S, values='WeightedProb', index='Runners', columns='Outs', aggfunc='first')
        pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
        pivot_table = pivot_table*100
        custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
        pivot_table = pivot_table.reindex(custom_order)
        pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%")
        st.subheader("The 2 Run Probability Matrix")
        st.write(pivot_table)

elif page == "Stealing (3 Runs)":
    st.title("3 Run Guide")
    selected_player = st.selectbox("Select Player", list(players.keys()))
    runners = st.text_input("Enter the runners on base (e.g., '1', '13', '123'):")
    outs = st.number_input("Enter the number of outs:", min_value=0, max_value=2, step=1)
    location = None
    base = None
    if '12' in runners:
        location = st.selectbox("Select the location:", ['Double', '3rd'])
        if location == "Double":
            base = st.selectbox("Are we focusing on the runner stealing 2nd or 3rd?", ["2nd", "3rd"])
    runners = int(runners)
    if st.button('Get Steal Information'):
        if base == "2nd":
            location = "Double (2nd)"
        result = get_steal_data(Z3S, runners, outs, location)
        st.write(f"{selected_player}: {players[selected_player]:.2%}")
        conf = result.iloc[0]['AVG Confidence']
        SB = result.iloc[0]["SB Value"]
        SBMax = result.iloc[0]["Max SB"]
        SBMin = result.iloc[0]["Min SB"]
        CS = result.iloc[0]["CS Value"]
        CSMax = result.iloc[0]["CS max"]
        CSMin = result.iloc[0]["CS min"]
        spread = players[selected_player] - conf
        st.write(f"Breakeven Rate: {round(conf*100, 2)}%")  # Assuming 'conf' is already in percentage format
        st.write(f"Advantage/Disadvantage Spread: {round(spread*100, 2)}%")
        st.write(f"Successful steal improves odds to score 3 by {round(SB*100, 2)}% ({round(SBMax*100, 2)}% , {round(SBMin*100, 2)}%)")
        st.write(f"Caught stealing decreases odds to score 3 by {round(CS*100, 2)}% ({round(CSMax*100, 2)}% , {round(CSMin*100, 2)}%)")
        steal_percentage = players[selected_player]
        tilt_minY = result.iloc[0]['Tilt min']
        tilt_maxY = result.iloc[0]['Tilt max']
        lean_minY = result.iloc[0]['Lean min']
        lean_maxY = result.iloc[0]['Lean max']
        likely_minY = result.iloc[0]['Likely min']
        likely_maxY = result.iloc[0]['Likely max']
        tilt_minN = result.iloc[0]['Tilt min.1']
        tilt_maxN = result.iloc[0]['Tilt max.1']
        lean_minN = result.iloc[0]['Lean min.1']
        lean_maxN = result.iloc[0]['Lean max.1']
        likely_minN = result.iloc[0]['Likely min.1']
        likely_maxN = result.iloc[0]['Likely max.1']
        if tilt_minY <= steal_percentage <= tilt_maxY:
            recommendation = 'Tilt Steal'
        elif lean_minY <= steal_percentage <= lean_maxY:
            recommendation = 'Lean Steal'
        elif likely_minY <= steal_percentage <= likely_maxY:
            recommendation = 'Likely Steal'
        elif steal_percentage > likely_maxY:
            recommendation = 'Safe Steal'
        elif tilt_minN >= steal_percentage >= tilt_maxN:
            recommendation = "Tilt Stay"
        elif lean_minN >= steal_percentage >= lean_maxN:
            recommendation = "Lean Stay"
        elif likely_minN >= steal_percentage >= likely_maxN:
            recommendation = "Likely Stay"
        elif steal_percentage < likely_maxN:
            recommendation = "Safe Stay"
        st.header(f"Recommendation: {recommendation}")
        projected = (SB*steal_percentage)+(CS*(1-steal-percentage))
        st.write(f"Projected Gain/Loss if Attempted: {round(projected*100, 2)}%")
        pivot_table = pd.pivot_table(WA3S, values='WeightedProb', index='Runners', columns='Outs', aggfunc='first')
        pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
        pivot_table = pivot_table*100
        custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
        pivot_table = pivot_table.reindex(custom_order)
        pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%")
        st.subheader("The 3 Run Probability Matrix")
        st.write(pivot_table)

elif page == "Bunting":
    st.title("Bunting Guide")
    option = st.selectbox("Select Historical or NECBL 2024 for suggestion", ["Historical", "NECBL 2024"])
    selected_player = st.selectbox("Select Player", list(players.keys()))
    if option == "Historical":
        outs = 0
        type = st.selectbox("What is the goal?", ["Maximize Runs", "1 Run", "2 Runs"])
        if type == "Maximize Runs":
            runners = st.text_input("Enter the runners on base (1,2,12):")
            runners = int(runners)
            if runners == 1 and selected_player:
                stats = projections[projections['Player'] == selected_player]
                xruns = stats.iloc[0]["1/0 BMAX"]
                max = BMAX.iloc[0]["Max"]
                min = BMAX.iloc[0]["Min"]
                SAC = BMAX.iloc[0]["Sacrifice Value"]
                tilt_minY = BMAX.iloc[0]['Tilt min']
                tilt_maxY = BMAX.iloc[0]['Tilt max']
                lean_minY = BMAX.iloc[0]['Lean min']
                lean_maxY = BMAX.iloc[0]['Lean max']
                likely_minY = BMAX.iloc[0]['Likely min']
                likely_maxY = BMAX.iloc[0]['Likely max']
                tilt_minN = BMAX.iloc[0]['Tilt min.1']
                tilt_maxN = BMAX.iloc[0]['Tilt max.1']
                lean_minN = BMAX.iloc[0]['Lean min.1']
                lean_maxN = BMAX.iloc[0]['Lean max.1']
                likely_minN = BMAX.iloc[0]['Likely min.1']
                likely_maxN = BMAX.iloc[0]['Likely max.1']
                if tilt_minY >= xruns >= tilt_maxY:
                    recommendation = 'Tilt Bunt'
                elif lean_minY >= xruns >= lean_maxY:
                    recommendation = 'Lean Bunt'
                elif likely_minY >= xruns >= likely_maxY:
                    recommendation = 'Likely Bunt'
                elif xruns < likely_maxY:
                    recommendation = 'Safe Bunt'
                elif tilt_minN <= xruns <= tilt_maxN:
                    recommendation = "Tilt no Bunt"
                elif lean_minN <= xruns <= lean_maxN:
                    recommendation = "Lean no Bunt"
                elif likely_minN <= xruns <= likely_maxN:
                    recommendation = "Likely no Bunt"
                elif xruns > likely_maxN:
                    recommendation = "Safe no Bunt"
                st.header(f"Recommendation: {recommendation}")
                st.write(f"Expected change in runs with successful bunt: {round(SAC, 2)} ({round(max, 2)}, {round(min, 2)})")
                st.write(f"Expected change in runs without bunt: {round(xruns, 2)}")
                st.write(f"No bunt vs bunt projected difference: {round(xruns-SAC, 2)}")
                pivot_table = pd.pivot_table(xWA, values='Weighted Average', index='Runners', columns='Outs', aggfunc='first')
                pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
                pivot_table = pivot_table.round(2)
                custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
                pivot_table = pivot_table.reindex(custom_order)
                st.subheader("The Run Expectancy Matrix")
                st.write(pivot_table)
            elif runners == 2 and selected_player:
                stats = projections[projections['Player'] == selected_player]
                xruns = stats.iloc[0]["2/0 BMAX"]
                SAC = BMAX.iloc[1]["Sacrifice Value"]
                max = BMAX.iloc[1]["Max"]
                min = BMAX.iloc[1]["Min"]
                tilt_minY = BMAX.iloc[1]['Tilt min']
                tilt_maxY = BMAX.iloc[1]['Tilt max']
                lean_minY = BMAX.iloc[1]['Lean min']
                lean_maxY = BMAX.iloc[1]['Lean max']
                likely_minY = BMAX.iloc[1]['Likely min']
                likely_maxY = BMAX.iloc[1]['Likely max']
                tilt_minN = BMAX.iloc[1]['Tilt min.1']
                tilt_maxN = BMAX.iloc[1]['Tilt max.1']
                lean_minN = BMAX.iloc[1]['Lean min.1']
                lean_maxN = BMAX.iloc[1]['Lean max.1']
                likely_minN = BMAX.iloc[1]['Likely min.1']
                likely_maxN = BMAX.iloc[1]['Likely max.1']
                if tilt_minY >= xruns >= tilt_maxY:
                    recommendation = 'Tilt Bunt'
                elif lean_minY >= xruns >= lean_maxY:
                    recommendation = 'Lean Bunt'
                elif likely_minY >= xruns >= likely_maxY:
                    recommendation = 'Likely Bunt'
                elif xruns < likely_maxY:
                    recommendation = 'Safe Bunt'
                elif tilt_minN <= xruns <= tilt_maxN:
                    recommendation = "Tilt no Bunt"
                elif lean_minN <= xruns <= lean_maxN:
                    recommendation = "Lean no Bunt"
                elif likely_minN <= xruns <= likely_maxN:
                    recommendation = "Likely no Bunt"
                elif xruns > likely_maxN:
                    recommendation = "Safe no Bunt"
                st.header(f"Recommendation: {recommendation}")
                st.write(f"Expected change in runs with successful bunt: {round(SAC, 2)} ({round(max, 2)}, {round(min, 2)})")
                st.write(f"Expected change in runs without bunt: {round(xruns, 2)}")
                st.write(f"No bunt vs bunt projected difference: {round(xruns-SAC, 2)}")
                pivot_table = pd.pivot_table(xWA, values='Weighted Average', index='Runners', columns='Outs', aggfunc='first')
                pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
                pivot_table = pivot_table.round(2)
                custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
                pivot_table = pivot_table.reindex(custom_order)
                st.subheader("The Run Expectancy Matrix")
                st.write(pivot_table)
            elif runners == 12 and selected_player:
                stats = projections[projections['Player'] == selected_player]
                xruns = stats.iloc[0]["12/0 BMAX"]
                SAC = BMAX.iloc[2]["Sacrifice Value"]
                max = BMAX.iloc[2]["Max"]
                min = BMAX.iloc[2]["Min"]
                tilt_minY = BMAX.iloc[2]['Tilt min']
                tilt_maxY = BMAX.iloc[2]['Tilt max']
                lean_minY = BMAX.iloc[2]['Lean min']
                lean_maxY = BMAX.iloc[2]['Lean max']
                likely_minY = BMAX.iloc[2]['Likely min']
                likely_maxY = BMAX.iloc[2]['Likely max']
                tilt_minN = BMAX.iloc[2]['Tilt min.1']
                tilt_maxN = BMAX.iloc[2]['Tilt max.1']
                lean_minN = BMAX.iloc[2]['Lean min.1']
                lean_maxN = BMAX.iloc[2]['Lean max.1']
                likely_minN = BMAX.iloc[2]['Likely min.1']
                likely_maxN = BMAX.iloc[2]['Likely max.1']
                if tilt_minY >= xruns >= tilt_maxY:
                    recommendation = 'Tilt Bunt'
                elif lean_minY >= xruns >= lean_maxY:
                    recommendation = 'Lean Bunt'
                elif likely_minY >= xruns >= likely_maxY:
                    recommendation = 'Likely Bunt'
                elif xruns < likely_maxY:
                    recommendation = 'Safe Bunt'
                elif tilt_minN <= xruns <= tilt_maxN:
                    recommendation = "Tilt no Bunt"
                elif lean_minN <= xruns <= lean_maxN:
                    recommendation = "Lean no Bunt"
                elif likely_minN <= xruns <= likely_maxN:
                    recommendation = "Likely no Bunt"
                elif xruns > likely_maxN:
                    recommendation = "Safe no Bunt"
                st.header(f"Recommendation: {recommendation}")
                st.write(f"Expected change in runs with successful bunt: {round(SAC, 2)} ({round(max, 2)}, {round(min, 2)})")
                st.write(f"Expected change in runs without bunt: {round(xruns, 2)}")
                st.write(f"No bunt vs bunt projected difference: {round(xruns-SAC, 2)}")
                pivot_table = pd.pivot_table(xWA, values='Weighted Average', index='Runners', columns='Outs', aggfunc='first')
                pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
                pivot_table = pivot_table.round(2)
                custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
                pivot_table = pivot_table.reindex(custom_order)
                st.subheader("The Run Expectancy Matrix")
                st.write(pivot_table)
        if type == "1 Run":
            runners = st.text_input("Enter the runners on base (1,2,12):")
            runners = int(runners)
            if runners == 1 and selected_player:
                stats = projections[projections['Player'] == selected_player]
                xruns = stats.iloc[0]["1/0 B1"]
                SAC = B1.iloc[0]["Sacrifice Value"]
                max = B1.iloc[0]["Max"]
                min = B1.iloc[0]["Min"]
                tilt_minY = B1.iloc[0]['Tilt min']
                tilt_maxY = B1.iloc[0]['Tilt max']
                lean_minY = B1.iloc[0]['Lean min']
                lean_maxY = B1.iloc[0]['Lean max']
                likely_minY = B1.iloc[0]['Likely min']
                likely_maxY = B1.iloc[0]['Likely max']
                tilt_minN = B1.iloc[0]['Tilt min.1']
                tilt_maxN = B1.iloc[0]['Tilt max.1']
                lean_minN = B1.iloc[0]['Lean min.1']
                lean_maxN = B1.iloc[0]['Lean max.1']
                likely_minN = B1.iloc[0]['Likely min.1']
                likely_maxN = B1.iloc[0]['Likely max.1']
                if tilt_minY >= xruns >= tilt_maxY:
                    recommendation = 'Tilt Bunt'
                elif lean_minY >= xruns >= lean_maxY:
                    recommendation = 'Lean Bunt'
                elif likely_minY >= xruns >= likely_maxY:
                    recommendation = 'Likely Bunt'
                elif xruns < likely_maxY:
                    recommendation = 'Safe Bunt'
                elif tilt_minN <= xruns <= tilt_maxN:
                    recommendation = "Tilt no Bunt"
                elif lean_minN <= xruns <= lean_maxN:
                    recommendation = "Lean no Bunt"
                elif likely_minN <= xruns <= likely_maxN:
                    recommendation = "Likely no Bunt"
                elif xruns > likely_maxN:
                    recommendation = "Safe no Bunt"
                st.header(f"Recommendation: {recommendation}")
                st.write(f"Expected change in odds to score at least 1 with successful bunt: {round(SAC*100, 2)}% ({round(max*100, 2)}%, {round(min*100, 2)}%)")
                st.write(f"Expected change in odds to score at least 1 without bunt: {round(xruns*100, 2)}%")
                st.write(f"No bunt vs bunt projected difference: {round(xruns*100-SAC*100, 2)}%")
                pivot_table = pd.pivot_table(WA1S, values='WeightedProb', index='Runners', columns='Outs', aggfunc='first')
                pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
                pivot_table = pivot_table*100
                custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
                pivot_table = pivot_table.reindex(custom_order)
                pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%")
                st.subheader("The 1 Run Probability Matrix")
                st.write(pivot_table)
            elif runners == 2 and selected_player:
                stats = projections[projections['Player'] == selected_player]
                xruns = stats.iloc[0]["2/0 B1"]
                SAC = B1.iloc[1]["Sacrifice Value"]
                max = B1.iloc[1]["Max"]
                min = B1.iloc[1]["Min"]
                tilt_minY = B1.iloc[1]['Tilt min']
                tilt_maxY = B1.iloc[1]['Tilt max']
                lean_minY = B1.iloc[1]['Lean min']
                lean_maxY = B1.iloc[1]['Lean max']
                likely_minY = B1.iloc[1]['Likely min']
                likely_maxY = B1.iloc[1]['Likely max']
                tilt_minN = B1.iloc[1]['Tilt min.1']
                tilt_maxN = B1.iloc[1]['Tilt max.1']
                lean_minN = B1.iloc[1]['Lean min.1']
                lean_maxN = B1.iloc[1]['Lean max.1']
                likely_minN = B1.iloc[1]['Likely min.1']
                likely_maxN = B1.iloc[1]['Likely max.1']
                if tilt_minY >= xruns >= tilt_maxY:
                    recommendation = 'Tilt Bunt'
                elif lean_minY >= xruns >= lean_maxY:
                    recommendation = 'Lean Bunt'
                elif likely_minY >= xruns >= likely_maxY:
                    recommendation = 'Likely Bunt'
                elif xruns < likely_maxY:
                    recommendation = 'Safe Bunt'
                elif tilt_minN <= xruns <= tilt_maxN:
                    recommendation = "Tilt no Bunt"
                elif lean_minN <= xruns <= lean_maxN:
                    recommendation = "Lean no Bunt"
                elif likely_minN <= xruns <= likely_maxN:
                    recommendation = "Likely no Bunt"
                elif xruns > likely_maxN:
                    recommendation = "Safe no Bunt"
                st.header(f"Recommendation: {recommendation}")
                st.write(f"Expected change in odds to score at least 1 with successful bunt: {round(SAC*100, 2)}% ({round(max*100, 2)}%, {round(min*100, 2)}%)")
                st.write(f"Expected change in odds to score at least 1 without bunt: {round(xruns*100, 2)}%")
                st.write(f"No bunt vs bunt projected difference: {round(xruns*100-SAC*100, 2)}%")
                pivot_table = pd.pivot_table(WA1S, values='WeightedProb', index='Runners', columns='Outs', aggfunc='first')
                pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
                pivot_table = pivot_table*100
                custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
                pivot_table = pivot_table.reindex(custom_order)
                pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%")
                st.subheader("The 1 Run Probability Matrix")
                st.write(pivot_table)
            elif runners == 12 and selected_player:
                stats = projections[projections['Player'] == selected_player]
                xruns = stats.iloc[0]["12/0 B1"]
                SAC = B1.iloc[2]["Sacrifice Value"]
                max = B1.iloc[2]["Max"]
                min = B1.iloc[2]["Min"]
                tilt_minY = B1.iloc[2]['Tilt min']
                tilt_maxY = B1.iloc[2]['Tilt max']
                lean_minY = B1.iloc[2]['Lean min']
                lean_maxY = B1.iloc[2]['Lean max']
                likely_minY = B1.iloc[2]['Likely min']
                likely_maxY = B1.iloc[2]['Likely max']
                tilt_minN = B1.iloc[2]['Tilt min.1']
                tilt_maxN = B1.iloc[2]['Tilt max.1']
                lean_minN = B1.iloc[2]['Lean min.1']
                lean_maxN = B1.iloc[2]['Lean max.1']
                likely_minN = B1.iloc[2]['Likely min.1']
                likely_maxN = B1.iloc[2]['Likely max.1']
                if tilt_minY >= xruns >= tilt_maxY:
                    recommendation = 'Tilt Bunt'
                elif lean_minY >= xruns >= lean_maxY:
                    recommendation = 'Lean Bunt'
                elif likely_minY >= xruns >= likely_maxY:
                    recommendation = 'Likely Bunt'
                elif xruns < likely_maxY:
                    recommendation = 'Safe Bunt'
                elif tilt_minN <= xruns <= tilt_maxN:
                    recommendation = "Tilt no Bunt"
                elif lean_minN <= xruns <= lean_maxN:
                    recommendation = "Lean no Bunt"
                elif likely_minN <= xruns <= likely_maxN:
                    recommendation = "Likely no Bunt"
                elif xruns > likely_maxN:
                    recommendation = "Safe no Bunt"
                st.header(f"Recommendation: {recommendation}")
                st.write(f"Expected change in odds to score at least 1 with successful bunt: {round(SAC*100, 2)}% ({round(max*100, 2)}%, {round(min*100, 2)}%)")
                st.write(f"Expected change in odds to score at least 1 without bunt: {round(xruns*100, 2)}%")
                st.write(f"No bunt vs bunt projected difference: {round(xruns*100-SAC*100, 2)}%")
                pivot_table = pd.pivot_table(WA1S, values='WeightedProb', index='Runners', columns='Outs', aggfunc='first')
                pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
                pivot_table = pivot_table*100
                custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
                pivot_table = pivot_table.reindex(custom_order)
                pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%")
                st.subheader("The 1 Run Probability Matrix")
                st.write(pivot_table)
        if type=="2 Runs" and selected_player:
            st.subheader("Note: The only situation where bunting should be considered when trying to score 2 is 12/0")
            stats = projections[projections['Player'] == selected_player]
            xruns = stats.iloc[0]["12/0 B2"]
            SAC = B2.iloc[0]["Sacrifice Value"]
            max = B2.iloc[0]["Max"]
            min = B2.iloc[0]["Min"]
            tilt_minY = B2.iloc[0]['Tilt min']
            tilt_maxY = B2.iloc[0]['Tilt max']
            lean_minY = B2.iloc[0]['Lean min']
            lean_maxY = B2.iloc[0]['Lean max']
            likely_minY = B2.iloc[0]['Likely min']
            likely_maxY = B2.iloc[0]['Likely max']
            tilt_minN = B2.iloc[0]['Tilt min.1']
            tilt_maxN = B2.iloc[0]['Tilt max.1']
            lean_minN = B2.iloc[0]['Lean min.1']
            lean_maxN = B2.iloc[0]['Lean max.1']
            likely_minN = B2.iloc[0]['Likely min.1']
            likely_maxN = B2.iloc[0]['Likely max.1']
            if tilt_minY >= xruns >= tilt_maxY:
                recommendation = 'Tilt Bunt'
            elif lean_minY >= xruns >= lean_maxY:
                recommendation = 'Lean Bunt'
            elif likely_minY >= xruns >= likely_maxY:
                recommendation = 'Likely Bunt'
            elif xruns < likely_maxY:
                recommendation = 'Safe Bunt'
            elif tilt_minN <= xruns <= tilt_maxN:
                recommendation = "Tilt no Bunt"
            elif lean_minN <= xruns <= lean_maxN:
                recommendation = "Lean no Bunt"
            elif likely_minN <= xruns <= likely_maxN:
                recommendation = "Likely no Bunt"
            elif xruns > likely_maxN:
                recommendation = "Safe no Bunt"
            st.header(f"Recommendation: {recommendation}")
            st.write(f"Expected change in odds to score at least 2 with successful bunt: {round(SAC*100, 2)}% ({round(max*100, 2)}%, {round(min*100, 2)}%)")
            st.write(f"Expected change in odds to score at least 2 without bunt: {round(xruns*100, 2)}%")
            st.write(f"No bunt vs bunt projected difference: {round(xruns*100-SAC*100, 2)}%")
            pivot_table = pd.pivot_table(WA2S, values='WeightedProb', index='Runners', columns='Outs', aggfunc='first')
            pivot_table.columns = [f"{int(col)} Outs" for col in pivot_table.columns]
            pivot_table = pivot_table*100
            custom_order = [0, 1, 2, 3, 12, 13, 23, 123]
            pivot_table = pivot_table.reindex(custom_order)
            pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%")
            st.subheader("The 2 Run Probability Matrix")
            st.write(pivot_table)
           
