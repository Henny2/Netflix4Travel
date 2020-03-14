#TripAdvisor Crawler to Get User Name and Rating
#Melvin Ang 14/2/2020

import requests
import pandas as pd
import timeit

start = timeit.default_timer()

#Loop through each link in the csv file
bodyhtml = []
linkpage = 0
link = "https://www.tripadvisor.com/Attraction_Review-g60713-d103856-Reviews-Haight_Ashbury-San_Francisco_California.html"
#To obtain x number of review pages in that link
for i in range(190):
    print(link)
    print("Getting review pages:", i)
    url =  (link.split("Reviews")[0]+"Reviews-or"+str(linkpage)+link.split("Reviews")[1])
    print(url)
    bodyhtml.append(url)
    linkpage = linkpage + 5 #every new review page changes by -or5- in the url

#To loop through each review page and get the name and rating
profilename = []
reviewrating = []
for i in range(len(bodyhtml)):
    html_text = requests.get(bodyhtml[i]).text #get entire page html text #IT IS ONLY GETTING 3RD PAGE OF GOLDEN GATE!!! Previously entire body HTML is only one place!!!
    print("Extracting each review:", i)
    parse = html_text.split("<div class=\"location-review-card-Card__ui_card")  #To obtain each html review section in that page
    #To obtain profile name and rating  
    for i in range(1,len(parse)):
        profilename.append(parse[i].split("/Profile/")[1].split("\"")[0])
        reviewrating.append(parse[i].split("ui_bubble_rating bubble_")[1].split("\">")[0])
        print("Append name and rating", i)
         
#To combine lists into a dataframe
df_HaightAshbury = pd.DataFrame(profilename, columns=["Name"])
place_name = link.split("Reviews-")[1].split("-San_Francisco_California")[0]
df_HaightAshbury[place_name] = reviewrating
df_HaightAshbury

stop = timeit.default_timer()
print('Time: ', stop - start) 

#Merge dataframes into one 
df_Combined = df_16Avenue

df_Combined = df_Combined.merge(df_Exploratorium, on='Name', how='outer')
#Count unique names
df_Combined['Name'].value_counts()
#Remove duplicate rows
df_Combined.drop_duplicates(subset="Name", inplace=True)

#Export to csv
df_Combined.to_csv('df_Combined.csv', index = None)

#df_16Avenue
#df_AcademyOfScience
#df_Alcatraz
#df_CableCar
#df_Exploratorium
#df_GoldenGate
#df_GoldenGatePark
#df_LandsEnd
#df_OraclePark
#df_PalaceOfFineArts
#df_TwinPeak
#df_WaltDisneyMuseum
#df_FerryMarket
#df_LombardStreet
#df_MOMA
#df_CoitTower
#df_LegionOfHonor
#df_SFBay
#df_Pier39
#df_MuseumIceCream
#df_BotanicalGarden
#df_DeYoungMuseum
#df_CableCarMuseum
#df_Presidio
#df_BakerBeach
#df_AngelIsland
#df_MissionDoloresPark
#df_FishermanWharf
#df_JapTeaGarden
#df_16Avenue
#df_GhirardelliSquare
#df_Chinatown
#df_UnionSquare
#df_PaintedLadies
#df_HaightAshbury