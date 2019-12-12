#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
# purchase_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[3]:


#calculate the number of unique players
player_demographics = purchase_data.loc[:, ["Gender", "SN", "Age"]]
player_demographics = player_demographics.drop_duplicates()
num_players = player_demographics.count()[0]
pd.DataFrame({"Total Players": [num_players]})


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[5]:


# run calculation to obtain number of unique items, average price, etc

average_item_price = purchase_data["Price"].mean()
total_purchase_value = purchase_data["Price"].sum()
purchase_count = purchase_data["Price"].count()
item_count = len(purchase_data["Item ID"].unique())

# create a DataFrame to hold results 
summary_table = pd.DataFrame({
                                "Number of Unique Items": [item_count],
                                "Average Price": [average_item_price],
                                "Purchase Count": [purchase_count],
                                "Total Revenue": [total_purchase_value]
                            })

summary_table = summary_table.round(2)
summary_table ["Average Price"] = summary_table["Average Price"].map("${:,.2f}".format)
summary_table ["Purchase Count"] = summary_table["Purchase Count"].map("{:,}".format)
summary_table ["Total Revenue"] = summary_table["Total Revenue"].map("${:,.2f}".format)

summary_table = summary_table.loc[:, ["Number of Unique Items", "Average Price", 
                                      "Purchase Count", "Total Revenue"]]
                                  
summary_table


# 
# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[6]:


#calculate the number of percentage by gender

gender_demographics_total = player_demographics["Gender"].value_counts()
gender_demographics_percent = (gender_demographics_total/num_players)

gender_demographics = pd.DataFrame({
                        "Total Count": gender_demographics_total,
                        "Percentage of Players": gender_demographics_percent
                    })
#clean data
gender_demographics["Percentage of Players"] = gender_demographics["Percentage of Players"].map("{:,.2%}".format)

gender_demographics


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[7]:


# run calculations
gender_purchase_total = purchase_data.groupby(["Gender"]).sum()["Price"].rename("Total Purchase Value")
gender_average = purchase_data.groupby(["Gender"]).mean()["Price"].rename("Average Purchase Price")
gender_counts = purchase_data.groupby(["Gender"]).count()["Price"].rename("Purchase Count")

#calculate normalized purhasing 
normalized_total = gender_purchase_total/gender_demographics["Total Count"]

# convert to Data Frame
gender_data = pd.DataFrame ({"Purchase Count": gender_counts,
                            "Average Purchase Price": gender_average,
                            "Total Purchase Value": gender_purchase_total,
                            "Normalized Totals": normalized_total})

#clean data
gender_data["Average Purchase Price"] = gender_data["Average Purchase Price"].map("${:,.2f}".format)
gender_data["Total Purchase Value"] = gender_data["Total Purchase Value"].map("${:,.2f}".format)
gender_data["Avg Total Purchase per Person"] = gender_data["Normalized Totals"].map("${:,.2f}".format)
gender_data["Purchase Count"] = gender_data["Purchase Count"].map("{:,}".format)

gender_data[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Avg Total Purchase per Person"]]


# 
# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[8]:


#determine bins
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# categorize the existing players using age bins
player_demographics["Age Ranges"] = pd.cut(player_demographics["Age"], age_bins, 
                                           labels=group_names)

age_demographics_totals = player_demographics["Age Ranges"].value_counts()
age_demographics_percents = age_demographics_totals/num_players

age_demographics = pd.DataFrame({"Total Count":age_demographics_totals,
                               "Percentage of Players":age_demographics_percents})

# clean
age_demographics["Percentage of Players"] = age_demographics["Percentage of Players"].map("{:,.2%}".format)

# sort and display table
age_demographics = age_demographics.sort_index()

age_demographics


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[9]:


#bin the purchasing data
purchase_data["Age Ranges"] = pd.cut(purchase_data["Age"], age_bins, labels= group_names)

#calculation time
age_purchase_total = purchase_data.groupby(["Age Ranges"]).sum()["Price"].rename("Total Purchase Value")
age_average = purchase_data.groupby(["Age Ranges"]).mean()["Price"].rename("Average Purchase Price")
age_count = purchase_data.groupby(["Age Ranges"]).count()["Price"].rename("Purchase Count")

#normalize the total
normalized_total = age_purchase_total / age_demographics["Total Count"]

#convert to data frame
age_data = pd.DataFrame({"Purchase Count": age_count,
                        "Average Purchase Price": age_average,
                        "Total Purchase Value": age_purchase_total,
                        "Normalized Totals": normalized_total
                        })

#format
age_data["Average Purchase Price"] = age_data["Average Purchase Price"].map("${:,.2f}".format)
age_data["Total Purchase Value"] = age_data["Total Purchase Value"].map("${:,.2f}".format)
age_data["Average Total Purchase per Person"] = age_data["Normalized Totals"].map("${:,.2f}".format)
age_data["Purchase Count"] = age_data["Purchase Count"].map("{:,}".format)


#extract and print
age_data[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Average Total Purchase per Person"]]


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[10]:


user_total = purchase_data.groupby(["SN"]).sum()["Price"].rename("Total Purchase Value")
user_average = purchase_data.groupby(["SN"]).mean()["Price"].rename("Average Purchase Price")
user_count = purchase_data.groupby(["SN"]).count()["Price"].rename("Purchase Count")

user_data = pd.DataFrame({"Total Purchase Value": user_total,
                         "Average Purchase Price": user_average,
                         "Purchase Count": user_count})

user_sorted = user_data.sort_values("Total Purchase Value", ascending = False)

#format data
user_sorted["Total Purchase Value"] = user_sorted["Total Purchase Value"].map("${:,.2f}".format)
user_sorted["Average Purchase Price"] = user_sorted["Average Purchase Price"].map("${:,.2f}".format)

#extract
user_sorted[["Purchase Count","Average Purchase Price", "Total Purchase Value"]].head(5)


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[11]:


item_data = purchase_data [["Item ID", "Item Name", "Price"]]

#perform calculaiton
total_item_purchase = item_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchase Price")
average_item_purchase = item_data.groupby(["Item ID", "Item Name"]).mean()["Price"].rename("Item Price")
item_count = item_data.groupby(["Item ID", "Item Name"]).count()["Price"].rename("Purchase Count")


#create dataframe
item_data_pd = pd.DataFrame({"Total Purchase Value": total_item_purchase, 
                            "Item Price": average_item_purchase,
                            "Purchase Count": item_count})

#sort values
item_data_count_sorted = item_data_pd.sort_values("Purchase Count", ascending = False)

#clean data
item_data_count_sorted["Total Purchase Value"] = item_data_count_sorted["Total Purchase Value"].map("${:,.2f}".format)
item_data_count_sorted["Item Price"] = item_data_count_sorted["Item Price"].map("${:,.2f}".format)
item_data_count_sorted["Purchase Count"] = item_data_count_sorted["Purchase Count"].map("{:,}".format)

item_data_count_sorted[["Purchase Count", "Item Price", "Total Purchase Value"]].head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[12]:


#item table
item_total_purchase = item_data_pd.sort_values("Total Purchase Value", ascending = False)

#format
item_total_purchase["Item Price"] = item_total_purchase["Item Price"].map("${:,.2f}".format)
item_total_purchase["Purchase Count"] = item_total_purchase["Purchase Count"].map("{:,}".format)
item_total_purchase["Total Purchase Value"] = item_total_purchase["Total Purchase Value"].map("${:,.2f}".format)

item_total_purchase[["Purchase Count", "Item Price", "Total Purchase Value"]].head(5)


# In[ ]:




