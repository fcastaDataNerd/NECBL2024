#Name: Francesco Castagliuolo

#CS230: Section 1

#Data: California Rest Stops

#Description: This streamlit application is intended to help users find the best rest stop for their needs. Three core tools are offered for this. If the user wants to simply find the closest one, the "Find Nearest Rest Stop" tool would be used. If they want the best overall rest stop based on how important each service is for them, the custom weighting tool would be used. If they want to narrow in on rest stops that have certain services and are within an acceptable distance, the "Must Have Services?" page would be accessed. Additionally, maps of where the rest stops are located and some analytics about postmile, longitude, and latitude are offered.


import streamlit as st
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import pydeck as pdk
import os
from scipy.stats import zscore

os.environ["MAPBOX_KEY"]="pk.eyJ1IjoiZmNhc3RhMTgiLCJhIjoiY2x2ZnlrbnIxMHEybzJpbjE4ZXh0Z3hxbyJ9.DfHnFoLH40bOJoImJs001Q"
rest=pd.read_excel("Rest_Areas.xlsx")

page=st.sidebar.selectbox("Choose a page", ["Home", "Find Nearest Rest Stop", "Find the Best Option For You", "Must Have Services? Filter Rest Stops Here", "Rest Stop Location Maps", "Cool Analytics"])

#Navigation functions. Home, NearestStop, BestStop, Essential, Map, and Analytics
def Home():
    if page=="Home":
        st.title("California Rest Stops: An Interactive Guide")
        st.markdown("<h2 style='color: red;'>Welcome!</h2>",  unsafe_allow_html=True) #changing text color
        st.subheader("This application has many helpful and interactive tools to help you find the rest stop that best suits your needs. Looking for the nearest rest stop? We got you covered. Use our coveted custom weighting tool to find the best overall stop or visit the must have services page to filter the rest stops that have your essential services. We also provide some cool maps and analytics about each rest stop. Enjoy the journey!")
        st.image("https://th.bing.com/th/id/R.ad72005ef6232c0938d0068821046b3b?rik=SwDIP52ggr4wbA&riu=http%3a%2f%2fbesttraveltips.net%2fwp-content%2fuploads%2f2015%2f11%2fdv.jpg&ehk=Pt94THx7REv8UFi2wci4xCQQClVNEeqNZojbQ50udfA%3d&risl=1&pid=ImgRaw&r=0")
        st.image("https://printablemapforyou.com/wp-content/uploads/2019/03/regions-of-california-map-map-hd-california-geographical-map-klipy-california-geography-map.jpg")
        
def NearestStop():
    if page=="Find Nearest Rest Stop":
        st.header("Looking for the nearest rest stop?")
        st.write("Use our interactive tool find the closest rest stop and its services.")
        long=st.number_input("Enter current longitude") #basically an input statement and asks user for number
        lat=st.number_input("Enter current latitude")
        if long and lat>-90 and lat <90: #check to see long and lat have been entered and within the acceptable range
            if st.button("Click here for nearest rest stop."): #button appears to find closest stop after valid long and lat entered, code to find it runs after button clicked which evaluates to True
                rest=AddDistanceCol(lat, long) #adding the distance column
                miles_away=rest.Distance.min() #variable created to find the shortest distance to a rest stop from the newly created distance column.
                stop=rest[rest.Distance==miles_away].iloc[0] #rest[rest.distance==miles_away] collects all rows where distance equals miles_away, the minimum distance. New dataframe created. iloc[0] selects first row of new dataframe in order to display only the closest rest stop
                services={service: stop[service] for service in ["RESTROOM", "WATER", "PICNICTAB", "PHONE", "HANDICAP", "RV_STATION", "VENDING", "PET_AREA"]} #dictionary comprehension to create a dictionary of the rest stop in "stop" with services as the keys and yes/no as the values. 
                st.subheader("Recommendation:")
                st.write(f"Head over to {stop['NAME']}, which is {round(miles_away,2)} miles away. This rest stop is in District {stop['DISTRICT']}, the city of {stop['CITY']}, and {stop['COUNTY']} county on Route {stop['ROUTE']}.") #since stop variable extracts entire row, need to extract the name of the rest stop within it and other information
                st.subheader("Services")
                for s, yesno in services.items(): #extracting the keys an values from the service dictionary. For each pair we print the service and the yes/no value. 
                    st.write(f"{s}? - {yesno}")
        else: 
            st.write("Value Error: Enter latitude between -90 and 90")

def BestStop():
    if page=="Find the Best Option For You":
        st.header("Use Our Custom Weighting System to Find the Best Rest Stop For Your Needs")
        st.subheader("Enter your current longitude and latitude, the maximum distance you are willing to travel, then for each of the services and proximity to the rest stop, indicate how important each is to you.")
        st.write("Enter current longitude and latitude and the maximum distance you are willing to travel")
        long=st.number_input("Enter current longitude") 
        lat=st.number_input("Enter current latitude")
        #line below collects all user slider inputs indicating how important each service is using the CollectInfoAndDisplay function.
        max_dist, distance, restroom, water, picnictab, phone, handicap, rv_station, vending, pet_area=CollectInfoAndDisplay()
        points=distance+restroom+water+picnictab+phone+handicap+rv_station+vending+pet_area #total points calculated by slider value for each service
        scoresDict={"Distance": distance, "RESTROOM":restroom, "WATER":water, "PICNICTAB":picnictab, "PHONE":phone, "HANDICAP":handicap, "RV_STATION": rv_station, "VENDING": vending, "PET_AREA": pet_area} #dictionary with services as the keys and the values are the slider points for each. 
        weightsDict={} #stores services as keys but values will be the weighting of each services calculated by slider points/total
        for service, importance in scoresDict.items(): #iterating through each service and its slider points in the scoresDict dictionary
            score=scoresDict[service] #slider value for service
            weightsDict[service]=[score/points] #adding the current service as the key and its weight as the value to weightsDict
        
        updated=AddDistanceCol(lat, long) #column added showing distance from user to rest stop
        updated=updated.loc[updated["Distance"]<=max_dist, ["NAME", "Distance", "RESTROOM", "WATER", "PICNICTAB", "PHONE", "HANDICAP", "RV_STATION", "VENDING", "PET_AREA"]] #filters the updated dictionary(just rest+distance col) to only include rows less than or equal to the maximum distance the user is willing to travel.
        
        service_scores=[] #score for each rest stop
        for index, row in updated.iterrows(): #iterate through updated df by row index and series(column) pairs. Each rest stop score calculated one at a time
            score=0 #counter variable for each stop score
            for service in row.index: #nested loop to find the score for the current rest stop in the overall for statement. Iterates through each service column in the updated df with the row.index argument
                if service!="Distance": #binary services and distance calculated differently in score. If it is not distance and the service is yes, collect the first element in service list in weightsDict and add it to total score. 
                    if row[service]=="Yes":
                        score+=weightsDict[service][0] #0 needed to access first and only item in list of weightsDict[service]
                else: #when the loop reaches distance, similarly take its weighting use the distance_score calculation to add to overall score. 
                    distance_score=weightsDict["Distance"][0]*((max_dist-row["Distance"])/max_dist)    
                    score+=distance_score
            service_scores.append(score) #for each rest stop remaining add the score to the service_scores list
       
        updated["ServiceScore"]=service_scores #updated dictionary with new column adding the scores to the corresponding rest stop. 
        updated_sort=updated.sort_values(by="ServiceScore", ascending=False) #created a new df with updated df sorted by service score from highest to lowest. 
        st.write(f"Here are the rest stops within your maximum distance of {max_dist} miles sorted from highest service score to lowest.")
        st.write(updated_sort)
        if len(updated_sort)>0: #only proceed with further information and visualizations if at least one rest stop is within maximum distance
            st.subheader("Best Rest Stop for You:")
            #two lines below extract the best score and best rest stop name by accessing the updated_sort df, the appropriate column, and using iloc[0] to get the first row, which represents the best score and rest stop since it is sorted.
            bestScore=updated_sort["ServiceScore"].iloc[0] 
            bestName=updated_sort["NAME"].iloc[0]
            st.write(f"With a service score of {round(bestScore,2)} out of 1, our custom weighting system recommends {bestName}")
            st.write()
            st.write("The bar chart below shows the weighting of each service in the calculation of the total service score for each rest stop within your range. The bars represent the points to be gained for each service besides the distance bar, which represents the total points a stop would receive if it was zero miles away.")
            weights_df=pd.DataFrame.from_dict(weightsDict, orient="index", columns=["Weight"]) #converting the weightDict into a df for visualization purposes with pd.DataFrame.from_dict function. weightsDict is the dictionary to convert, orient=index forces the dict keys to be used as the row labels in the dataframe and columns=[weight] sets column labels to weight. Each dict value in weightDict is a list and this format allows each key value to occupy rows of one column named weight. 
            fig, ax=plt.subplots() #matplotlib subplot. fig is the figure for the plot to be drawn on and ax are the axes for the plot.
            weights_df["Weight"].plot(kind="bar", ax=ax) #plotting the data in bar plot form. Extracting the weight column from weight_df and using .plot method on it, kind=bar indicates bar plot, ax=ax plots the data on the ax variable and ensures the plot produced in this line is added to the correct subplot in the line above. 
            ax.set_xlabel("Service")  
            ax.set_ylabel("Importance Percentage Weighting")  
            ax.set_title("Your Service Importance")  
            st.pyplot(fig) #pyplot function shows the figure and the bar plot 
            st.subheader(f"Scores For Each Stop Within Your Range")
            #mostly same syntax to produce the bar plot of all service scores for rest stops within max range. 
            fig2, ax2=plt.subplots()
            updated_sort.set_index("NAME")["ServiceScore"].plot(kind="bar", ax=ax2) #slight difference here as the set_index method must be used on updated_sort to force the rest stop names to populate the x axis. Then service score is extracted as the selected column to plot
            ax2.set_xlabel("Rest Stop")  
            ax2.set_ylabel("Service Score")  
            ax2.set_title("Service Scores of Rest Stops Within Maximum Distance")  
            ax2.set_ylim(0,1) #service scores range from 0-1, setting custom y axis creates more visually appealing plot.
            st.pyplot(fig2)   
            st.subheader("How are service scores calculated?")
            st.write(f"Based on your sliders, a rest stop can receive a potential {points} points. The weighting for each service is calculated as the number on the slider divided by the total available points. For example, you weighted restroom as {round(restroom/points,2)} since it makes up {restroom} out of the {points} points available. If a rest stop has each binary service, their total score will be increased by the weighted value for that service. So a rest stop having a restroom will gain {round(restroom/points,2)} points.")
            st.write(f"The distance calculation is different since it is not a binary outcome. The system first filters the rest stops within the maximum distance you are willing to travel of {max_dist} miles. For each remaining rest stop, we calculate the distance points as the proximity weighting on the slider divided by the total points available similar to the other services, and for you this is {round(distance/points,2)}. We take {round(distance/points,2)} *(your max distance {max_dist}-distance from rest stop)/your max distance {max_dist}) to calculate the distance points.")
            st.write(f"Each of these is added together to get a score on a scale of 0-1. ")
        else:
            st.write("No rest stops within your range")   
             
        
def Essential():
    if page=="Must Have Services? Filter Rest Stops Here":
        st.header("Narrow Down Rest Stops with all the Services You Need")
        st.subheader("We love our custom weighting system, but sometimes a restroom, phone, or rv station are non-negotiable. Find all rest stops that have the services you require below.")
        long=st.number_input("Enter current longitude") 
        lat=st.number_input("Enter current latitude")
        max_dist=st.number_input("Enter maximum distance in miles")
        #two lines below is same process as beststop function to add the distance column and create a dataframe with rest stops that are within the maximum range specififed by the user. 
        updated=AddDistanceCol(lat, long) 
        updated=updated.loc[updated["Distance"]<=max_dist, ["NAME", "Distance", "RESTROOM", "WATER", "PICNICTAB", "PHONE", "HANDICAP", "RV_STATION", "VENDING", "PET_AREA"]]
        essential_services = { #a dictionary storing the services as key and its values are either yes/no depending on what the user selects. This dictionary is designed to extract all the essential services to the user
            "RESTROOM": st.selectbox("Is a restroom essential?", ["Yes", "No"]),
            "WATER": st.selectbox("Is water essential?", ["Yes", "No"]),
            "PICNICTAB": st.selectbox("Is a picnic table essential?", ["Yes", "No"]),
            "PHONE": st.selectbox("Is a phone essential?", ["Yes", "No"]),
            "HANDICAP": st.selectbox("Is a handicap restroom essential?", ["Yes", "No"]),
            "RV_STATION": st.selectbox("Is an RV station essential?", ["Yes", "No"]),
            "VENDING": st.selectbox("Is a vending machine essential?", ["Yes", "No"]),
            "PET_AREA": st.selectbox("Is a pet area essential?", ["Yes", "No"])
        }
        for service, need in essential_services.items(): #loop to iterate through the key value pairs in the essential_service dictionary. If the service is essential, the updated df is further filtered to contain only the rest stops that have that service. The process is repeated for each service to create a df containing only rest stops within the maximum distance that have all the user's essential services
            if need=="Yes":
                updated=updated.loc[updated[service]=="Yes"] 
        updated_sort=updated.sort_values(by="Distance", ascending=True) #new df to rank the rest stops with all services required. 
        updated_sort=updated_sort.loc[:,["NAME", "Distance"]] #final filter to only show the rest stop and its distance. loc allows us to extract only the name and distance columns and [:,["NAME", "Distance"]] uses the : to extract all rows from the name and distance columns.
        st.write("Here are the rest stops that meet your requirements, ranked by how close they are to you.")
        st.write(updated_sort)

def Map(): #the map function calls the AllMap, DistrictMap, and CityMap functions to display the Map page
    if page=="Rest Stop Location Maps":
        AllMap()
        DistrictMap()
        CityMap()
        
def Analytics(): #function to display the cool analytics page, showing multiple data tables of the quantitative measures in the dataset and some analytics I found interesting. 
    if page=="Cool Analytics":
        st.header("Explore Some Numbers Behind Postmile, Latitude, and Longitude")
        st.subheader("This table displays the postmile, latitude, and longitude for each rest stop and the z scores for each as well. The z scores represent how many standard deviations each rest stop's postmile, latitude, and longitude are from the mean, measured in standard deviations")
        subset=rest[["NAME", "POSTMILE", "LATITUDE", "LONGITUDE"]] #I wanted to focus on the core quantitative columns, so I created a subset of the rest df to only include the rest stop name, and the postmile, latitude, and longitude columns.
        #three lines below add z score columns to the subset df with a very easy function to calculate them. From scipy.stats I imported the zscore function which calculates z score for each row in each column. 
        subset["POSTMILE Z"]=zscore(rest["POSTMILE"]) 
        subset["LATITUDE Z"]=zscore(rest["LATITUDE"])
        subset["LONGITUDE Z"]=zscore(rest["LONGITUDE"])
        st.write(subset)
        data={ #nested dictionary to store summary stats for each column of interest. postmile, latitude, and longitude are the outer keys and the inner keys are the summary stats of mean, median, stdev, and skewness, and each is calculated by extracting the relevant column from subset and using the necessary method to extract the stat from the column.
            "POSTMILE": {
                "Mean": subset["POSTMILE"].mean(),
                "Median": subset["POSTMILE"].median(),
                "Stdev": subset["POSTMILE"].std(),
                "Skewness": subset["POSTMILE"].skew(),
                }, 
            "LATITUDE": {
                "Mean": subset["LATITUDE"].mean(),
                "Median": subset["LATITUDE"].median(),
                "Stdev": subset["LATITUDE"].std(),
                "Skewness": subset["LATITUDE"].skew(),
                }, 
            "LONGITUDE": {
                "Mean": subset["LONGITUDE"].mean(),
                "Median": subset["LONGITUDE"].median(),
                "Stdev": subset["LONGITUDE"].std(),
                "Skewness": subset["LONGITUDE"].skew(),
                }
            }
        data_df=pd.DataFrame(data) #conversion of dictionary into df that will index the summary stats as the rows and postmile, latitude, and longitude as the columns.
        st.subheader("Summary statistics for postmile, latitude and longitude including mean, median, standard deviation and skewness.")
        st.write(data_df)
        st.write("Some interesting numbers here. The mean for postmile is 40.8 and the median is 29.3, indicating that the distribution is significantly right skewed. As seen by the histogram below, the right tail is considerably longer and most values are concentrated on the left side of the histogram. Skewness of 1.28 confirms the distribution is heavily right skewed as any skewness metric greater than 0.5 indicates the distribution is not symmetric and heavily right skewed. Additionally, the variation of values in the postmile column is quite large with a standard deviation near 40, which we would expect considering there are some substantial outliers in the postmile column.")
        #the histogram function is called to create the density histograms for postmile, longitude, and latitude. 
        histogram(subset, "POSTMILE")
        st.write("The Longitude density histogram indicates a multimodal distribution and one that is slightly right skewed based on the skewness statistic of 0.43. We see a steep increase in density from -124 to -122 followed by a steady decrease from -122 to -119, then another increase from -118 to -116. It appears to resemble a concave down quadratic function.")
        histogram(subset, "LONGITUDE", bins=15)
        st.write("The Latitude density histogram is quite interesting. Based on the summary statistics we would expect a normal distribution but it seems more complicated with many sharp changes in frequency based on latitude. This is likely a multimodal distribution indicated by the significant changes in direction at multiple intervals on the x axis.")
        histogram(subset, "LATITUDE", bins=15)


#Convenience functions 
def AddDistanceCol(lat, long, df=rest): #function used to add the distance column to the rest dataframe. Used when user enters long and lat and I need to calculate how far away in miles each rest stop is from the user. Mostly used to make a new dataframe based on this column where the distance values are less than the maximum distance the user can travel.
    location=(lat, long) #tuple that represents the geographical location of the user and the starting point to calculate the distance from each rest stop
    df["Distance"]=df.apply(lambda row: geodesic(location, (row["LATITUDE"], row["LONGITUDE"])).miles, axis=1) #complicated line here that I needed to do a lot of research on because it uses geopy package which I was unfamiliar with. New column is added by first using .apply which applies the function within the parenthesis to each row and this is achieved by setting axis=1. Lambda row calculates distance for each row individually in rest df. It iterates over each row in rest and extracts the latitude and longitude then inserts them into the geodesic function. This is apparently needed because geodesic method doesn't work on DataFrame rows and the lambda row function is needed to guide geodesic to work on a row by row basis. The geodesic function itself calculates the shortest distance from the first argument of the user location and location of the rest stop extracted by the lambda row function and converts the units to miles.
    return df #returns updated rest df with the distance row representing the shortest distance from the user location to each rest stop

def AllMap(): #one of three functions to be called in the map navigation function. Shows all the rest stops in California populated with red dots
    st.header("Explore Different Maps of California Rest Stops")
    st.subheader("All Rest Stops")
    state=pdk.ViewState( #pdk.ViewState configures the center viewpoint of the map
        latitude=rest["LATITUDE"].mean(),
        longitude=rest["LONGITUDE"].mean(),
        #latitude and longitude determine where the map will be focused by extract the mean lat and long from the rest df. Map becomes centered based on these averages.
        zoom=6, 
        pitch=0 #angle which viewer sees map. 0 is best as it looks like a normal and flat map. 
        )
    layer=pdk.Layer( #pdk.layer is a function used to create the layer used on the pydeck map.
        "ScatterplotLayer", #the type of layer to be used and scatterplotlayer is typically used when we want to display individual points and locations on a map
        data=rest, #df to use
        get_position="[LONGITUDE, LATITUDE]", #from the rest df, "[LONGITUDE, LATITUDE]" determines how to get lat and long from rest df to be used in plotting of points on map
        get_color="[255,0,0,255]", #this uses a red, green, blue, alpha color model. Scale ranges from 0-255. The first three values represent how apparent red, green, and blue are in the dots, so I set red to the maximum value and green and blue to the lowest. The alpha argument controls how visible the red dots are and I also set this to the maximum value. 
        get_radius=5000 #the size of each red dot
        )    
    createMap=pdk.Deck( #pdk.Deck displays the map
        layers=[layer], #accepts list of layers to plot
        initial_view_state=state, #using ViewState method in state argument for map centering and zoom
        map_style="mapbox://styles/mapbox/light-v9" #mapbox theme
        )    
    st.pydeck_chart(createMap) #streamlit function to display map

def DistrictMap(): #second of three function to be used in the map function. This allows users to filter rest stop locations based on district and see their locations on the map
    st.subheader("Explore Maps Displaying Rest Stops by District(s)")
    st.write("Select the District(s) Below:")
    opt=rest["DISTRICT"].unique() #extracting all unique district values
    selected=st.multiselect("Districts", options=opt)
    if len(selected)>0:
        rest_districts=rest[rest["DISTRICT"].isin(selected)] #if the district in the rest df is part of the multiselect, create a filtered df with rows only containing those districts. 
        state=pdk.ViewState(
        latitude=rest_districts["LATITUDE"].mean(),
        longitude=rest_districts["LONGITUDE"].mean(),
        zoom=6,
        pitch=0
        )
        layer=pdk.Layer(
        "ScatterplotLayer",
        data=rest_districts,
        get_position="[LONGITUDE, LATITUDE]",
        get_color="[255,0,0,255]",
        get_radius=5000
        )    
        createMap=pdk.Deck(
        layers=[layer],
        initial_view_state=state,
        map_style="mapbox://styles/mapbox/light-v9"
        )    
        st.pydeck_chart(createMap)
            
def CityMap(): #third of three functions used in the map function. This allows users to filter rest stop locations based on cities and see their locations on the map
    st.subheader("Explore Maps Displaying Rest Stops by Cities")
    st.write("Select the Cities Below:")
    opt=rest["CITY"].unique() #from the city column in the rest dataset the, unique method finds each individual city and stores them in the opt variable
    selected=st.multiselect("Cities", options=opt) #selected variable contains the results of the multiselect where the user can insert one or more cities and the options are the individual cities in the opt variable
    if len(selected)>0: #if at least one is selected the map will be displayed
        rest_cities=rest[rest["CITY"].isin(selected)] #rest_cities is a filtered version of rest. It includes only the rows where the city in the rest["CITY"] column is one of the cities selected by the user in the multiselect box. .isin(selected) is the method to filter
        state=pdk.ViewState(
        latitude=rest_cities["LATITUDE"].mean(),
        longitude=rest_cities["LONGITUDE"].mean(),
        zoom=6,
        pitch=0
        )
        layer=pdk.Layer(
        "ScatterplotLayer",
        data=rest_cities,
        get_position="[LONGITUDE, LATITUDE]",
        get_color="[255,0,0,255]",
        get_radius=5000
        )    
        createMap=pdk.Deck(
        layers=[layer],
        initial_view_state=state,
        map_style="mapbox://styles/mapbox/light-v9"
        )    
        st.pydeck_chart(createMap)
        

def histogram(df, column, bins=11, alpha=0.7): #used to display density histograms which are used in the Analytics function. Takes parameters of a dataframe and a specific column with default values of bins and alpha that can be adjusted.
    fig, ax = plt.subplots() #creating figure and axes where the histogram will be plotted with the plt.subplots function
    df[column].plot.hist(bins=bins, alpha=alpha, ax=ax, density=True) #creates a histogram from the specified column and making it a density histogram by setting density=True
    ax.set_title(f"Density Histogram of {column}")
    ax.set_xlabel(f"{column}")
    ax.set_ylabel("Density")
    st.pyplot(fig) #display the histogram

def CollectInfoAndDisplay(): #function used to collect all slider inputs from the user and return them
    max_dist=st.number_input("Enter maximum distance in miles")
    st.write("Now indicate how important each of the following is to you, with 0 being not important at all and 10 being essential.")
    distance=st.slider("Select the importance of proximity", 0,10,1)
    restroom=st.slider("Select the importance of having a restroom", 0,10,1)
    water=st.slider("Select the importance of providing water", 0,10,1)
    picnictab=st.slider("Select the importance of having a picnic table", 0,10,1)
    phone=st.slider("Select the importance of phone services", 0,10,1)
    handicap=st.slider("Select the importance of a handicap restroom", 0,10,1)
    rv_station=st.slider("Select the importance of an rv_station", 0,10,1)
    vending=st.slider("Select the importance of a vending machine", 0,10,1)
    pet_area=st.slider("Select the importance of providing a pet area", 0,10,1)
    return max_dist, distance, restroom, water, picnictab, phone, handicap, rv_station, vending, pet_area
    
            
#Main function for the application to run
def main():
    Home()
    NearestStop()
    BestStop()
    Essential()
    Map()
    Analytics()
main()


#"C:\Users\Franco Castagliuolo\AppData\Local\Microsoft\WindowsApps\python.exe" -m streamlit run "C:\Users\Franco Castagliuolo\eclipse-workspace\Final\StreamLitFinal.py"





