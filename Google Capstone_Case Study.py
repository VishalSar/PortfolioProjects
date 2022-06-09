#!/usr/bin/env python
# coding: utf-8

# # Case Study: How Does a Bike-Share Navigate Speedy Success?
# 
# After finishing the Google Data Analytics Certification courses, I had to use the skills and knowledge gained into solving a Capstone Project. Now, let me walk you through my approach to this Data Analytics case study.
# 
# **Let's begin!**

# ## Background

# ### Scenario
# You are a junior data analyst working in the marketing analyst team at Cyclistic, a bike-share company in Chicago. The director of marketing believes the company’s future success depends on maximizing the number of annual memberships. Therefore, your team wants to understand how casual riders and annual members use Cyclistic bikes differently. From these insights, your team will design a new marketing strategy to convert casual riders into annual members. **But first, Cyclistic executives must approve your recommendations, so they must be backed up with compelling data insights and professional data visualizations.**

# ### Characters and Teams
# 1) Cyclistic: A bike-share program that features more than 5,800 bicycles and 600 docking stations. Cyclistic sets itself apart by also offering reclining bikes, hand tricycles, and cargo bikes, making bike-share more inclusive to people with disabilities and riders who can’t use a standard two-wheeled bike. The majority of riders opt for traditional bikes; about 8% of riders use the assistive options. Cyclistic users are more likely to ride for leisure, but about 30% use them to commute to work each day.
# 
# 2) Lily Moreno: The director of marketing and your manager. Moreno is responsible for the development of campaigns and initiatives to promote the bike-share program. These may include email, social media, and other channels.
# 
# 3) Cyclistic marketing analytics team: A team of data analysts who are responsible for collecting, analyzing, and reporting data that helps guide Cyclistic marketing strategy. You joined this team six months ago and have been busy learning about Cyclistic’s mission and business goals — as well as how you, as a junior data analyst, can help Cyclistic achieve them.
# 
# 4) Cyclistic executive team: The notoriously detail-oriented executive team will decide whether to approve the recommended marketing program.

# ### About the company
# In 2016, Cyclistic launched a successful bike-share offering. Since then, the program has grown to a fleet of 5,824 bicycles that are geotracked and locked into a network of 692 stations across Chicago. The bikes can be unlocked from one station and returned to any other station in the system anytime.
# Until now, Cyclistic’s marketing strategy relied on building general awareness and appealing to broad consumer segments. One approach that helped make these things possible was the flexibility of its **pricing plans: single-ride passes, full-day passes, and annual memberships. Customers who purchase single-ride or full-day passes are referred to as casual riders. Customers who purchase annual memberships are Cyclistic members.**
# Cyclistic’s finance analysts have concluded that annual members are much more profitable than casual riders. Although the pricing flexibility helps Cyclistic attract more customers, Moreno believes that maximizing the number of annual members will be key to future growth. Rather than creating a marketing campaign that targets all-new customers, Moreno believes there is a very good chance to convert casual riders into members. She notes that casual riders are already aware of the Cyclistic program and have chosen Cyclistic for their mobility needs.
# Moreno has set a clear goal: Design marketing strategies aimed at converting casual riders into annual members. In order to do that, however, the marketing analyst team needs to better understand how annual members and casual riders differ, why casual riders would buy a membership, and how digital media could affect their marketing tactics. Moreno and her team are interested in analyzing the Cyclistic historical bike trip data to identify trends.

# <img src="bike_share.png" width=1200 height=200>

# ### Objective
# 
# To maximize the number of annual memberships by converting casual riders to annual members.

# ### Questions
# 
# 1. How do annual members and casual riders use Cyclistic bikes differently?
# 2. Why would casual riders buy Cyclistic annual memberships?
# 3. How can Cyclistic use digital media to influence casual riders to become members?

# **Follow these steps:**
# 
# 1) Download the previous 12 months of Cyclistic trip data
# 2) Unzip the files
# 3) Create a folder on your desktop or Drive to house the file and use appropriate file-naming conventions
# 
# We decide to use 12 months of data from June 2021 to May 2022.
# 
# Download the data from this [public dataset](https://divvy-tripdata.s3.amazonaws.com/index.html) made available by Motivate International Inc. under this [license](https://ride.divvybikes.com/data-license-agreement)

# ### Solution
# 
# #### Libraries
# Let's start by importing necessary libraries

# In[1]:


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime


# #### Load the data and Prepare
# 
# Read the data from downloaded CSV into data frames

# In[2]:


jun21 = pd.read_csv("Raw Data/202106.csv")
jul21 = pd.read_csv("Raw Data/202107.csv")
aug21 = pd.read_csv("Raw Data/202108.csv")
sep21 = pd.read_csv("Raw Data/202109.csv")
oct21 = pd.read_csv("Raw Data/202110.csv")
nov21 = pd.read_csv("Raw Data/202111.csv")
dec21 = pd.read_csv("Raw Data/202112.csv")
jan22 = pd.read_csv("Raw Data/202201.csv")
feb22 = pd.read_csv("Raw Data/202202.csv")
mar22 = pd.read_csv("Raw Data/202203.csv")
apr22 = pd.read_csv("Raw Data/202204.csv")
may22 = pd.read_csv("Raw Data/202205.csv")


# After checking for consistent formatting, merge the above data frames into one data frame

# In[3]:


data_frames = [jun21, jul21, aug21, sep21 , oct21, nov21, dec21, jan22, feb22, mar22, apr22, may22]
trips_df = pd.concat(data_frames)


# Let's take a quick look at the merged data frame

# In[4]:


trips_df.head()


# In[5]:


trips_df.shape


# In[6]:


trips_df.info()


# Notice that *started_at* and *ended_at* are 'object' data type, let's cast them to 'date and time'. Now, when we subtract *started_at* from *ended_at* we get the *ride_duration*

# In[7]:


trips_df["started_at"] = pd.to_datetime(trips_df["started_at"])
trips_df["ended_at"] = pd.to_datetime(trips_df["ended_at"])

trips_df.dtypes # checking


# Calculate the *ride_length*

# In[8]:


trips_df["ride_duration"] = trips_df["ended_at"] - trips_df["started_at"]
trips_df["ride_duration"] # view the new column


# Next, find out which days of the week and month of the year/s has how many trips per user type
# To do this:
# 1) Extract the start date and start time
# 2) Convert to date and time format
# 4) Add new columns for month and year from start date
# 3) Add new column for weekday and weekday_name from start date
# 4) Sort by start date

# In[9]:


# extract
trips_df[['start_date','start_time']] = trips_df['started_at'].astype(str).str.split(' ', n=1, expand=True) # n=1 split at the first space


# In[10]:


# convert
trips_df["start_time"] = pd.to_datetime(trips_df["start_time"])
trips_df["start_date"] = pd.to_datetime(trips_df["start_date"])

trips_df["start_time"] = pd.to_datetime(trips_df["start_time"], format = "%H%M%S").dt.time # selecting only time


# In[11]:


#add year and month
trips_df['year'] = pd.DatetimeIndex(trips_df['start_date']).year
trips_df['month'] = pd.DatetimeIndex(trips_df['start_date']).month


# In[12]:


#add weekday and weekday_name
trips_df["weekday"] = trips_df["start_date"].apply(lambda x:x.weekday()) #A lambda function is a nameless function used for a short period of time

trips_df["weekday"].unique()


# In[13]:


# create a dictionary to assign day number to day name
day_dict = {0:"Sunday", 1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"saturday"}
trips_df["weekday_name"] = trips_df['weekday'].apply(lambda y:day_dict[y])


# In[14]:


#sort
trips_df.sort_values(by = ['start_date'], inplace= True)


# In[15]:


trips_df.head()


# Check for:
# 1) Null values
# 2) Duplicates

# In[16]:


# null values
trips_df.isnull().sum()


# We have no missing data for start time and end time and other date columns which is good. Notice that some of the start and end station position details are missing and we might need to investigate and strategize to handle missing data if we need these details.
# Let us continue with analysis as current data is in good condition for our analysis.

# In[17]:


# duplicates
trips_df.duplicated().any()


# No duplicate rows.

# #### Process and Analyze

# Let's find the differences between Casual Group and Member Group of users

# **Average and max ride duration**

# In[18]:


# members average duration
data_mem = trips_df[trips_df["member_casual"] == "member"]
data_mem_ride_dur_avg = data_mem["ride_duration"].mean()
data_mem_ride_dur_avg


# Total member average ride duration= 13 mins 02 secs

# In[19]:


# casuals average duration
data_cas = trips_df[trips_df["member_casual"] == "casual"]
data_cas_ride_dur_avg = data_cas["ride_duration"].mean()
data_cas_ride_dur_avg


# Total casual average ride duration= 30 mins 32 secs

# In[20]:


# members average ride duration per day of week
data_mem_ride_dur_pday = trips_df[trips_df["member_casual"] == "member"].groupby('weekday')['ride_duration'].mean()
data_mem_ride_dur_pday


# In[21]:


# casuals average ride duration per day of week
data_cas_ride_dur_pday = trips_df[trips_df["member_casual"] == "casual"].groupby('weekday')['ride_duration'].mean()
data_cas_ride_dur_pday


# In[22]:


# plotting above data
plt.figure(figsize=(8,6))
plt.plot(data_mem_ride_dur_pday/pd.Timedelta(minutes=1)) 
plt.plot(data_cas_ride_dur_pday/pd.Timedelta(minutes=1)) # getting average in minutes
plt.title("Average Ride Duration Per Day")
plt.legend(["member","casual"])
labels = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
plt.xticks(data_mem_ride_dur_pday.index,labels)
plt.show()


# So on an average, the casual group of users have longest duration of rides.

# In[23]:


# members max duration 
data_mem_ride_dur_max = data_mem["ride_duration"].max()
data_mem_ride_dur_max


# In[24]:


# casuals max duration 
data_cas_ride_dur_max = data_cas["ride_duration"].max()
data_cas_ride_dur_max


# It seems casuals maximum is much higher than usual. We need to dig deeper to find out the reason.

# **Day of week with most rides**

# In[25]:


# members
data_mem_ride_day_most = data_mem["weekday"].mode()
data_mem_ride_day_most


# In[26]:


# casuals
data_cas_ride_day_most = data_cas["weekday"].mode()
data_cas_ride_day_most


# Day of week with most rides: For member users Monday and for casual users Friday

# **Total number of rides**

# In[27]:


# total rides by members and casuals
mem_type_total = trips_df["member_casual"].value_counts()
mem_type_total


# In[28]:


# plotting above data
plt.title("Total number of rides")
plt.bar(mem_type_total.index, mem_type_total.values)
plt.ticklabel_format(style = 'plain', axis = 'y')
plt.show()


# In[29]:


# percentage share through a pie-chart
plt.figure(figsize = (8,6))
plt.pie(mem_type_total.values, labels = mem_type_total.index, autopct='%1.1f%%')
plt.title("Percentage Share of User Types")
plt.legend(mem_type_total.index)
plt.show()


# In[30]:


# member user rides total by day of week
mem_rides_pday= trips_df[trips_df["member_casual"]=="member"].groupby('weekday')['ride_id'].count()
mem_rides_pday


# In[31]:


# casual user rides total by day of week
cas_rides_pday = trips_df[trips_df["member_casual"] == "casual"].groupby('weekday')['ride_id'].count()
cas_rides_pday


# In[32]:


# plotting above data
plt.figure(figsize = (9,6))
plt.plot(mem_rides_pday)
plt.plot(cas_rides_pday)
plt.title("Rides per day of week")
plt.legend(["member", "casual"])
labels=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
plt.xticks(mem_rides_pday.index, labels)
plt.show()


# As we can see, member riders more in total and they tend to take rides on weekdays. Whereas, casual riders are more active riders on weekends. This insight will help us in planning promotional offers and advertisements targeted for weekend riders.

# In[33]:


# checking monthly trends
monthly_users = trips_df.groupby("month")['member_casual'].value_counts()
monthly_users


# In[34]:


# plotting above data
plt.figure(figsize = (8,6))
sns.countplot(x = "member_casual", hue="month", data = trips_df)
plt.show()


# We can see that the riders increase from month of May through the summer. This could be because of good weather, summer break and holidays.

# **Type of bikes used by members and casuals**

# There are 3 types of bikes provided by the company. Let's have a look at what the riders prefer. 

# In[35]:


plt.figure(figsize = (8,6))
sns.countplot(x = "member_casual", hue = "rideable_type", data = trips_df)
plt.ticklabel_format(style = 'plain', axis = 'y')
plt.show()


# **Stations with highest riders (highest activity)**

# In[36]:


# top 10 start stations
pop_station_start = trips_df["start_station_name"].value_counts()
pop_station_start.head(10)


# In[37]:


plt.figure(figsize = (18,6))
plt.title("Popular Start Stations")
plt.bar(pop_station_start.head(10).index, pop_station_start.head(10).values)
plt.ticklabel_format(style = 'plain', axis = 'y')
plt.xticks(rotation = 45)
plt.show()


# In[38]:


# top 10 end stations
pop_station_end = trips_df["end_station_name"].value_counts()
pop_station_end.head(10)


# In[39]:


plt.figure(figsize = (18,6))
plt.title("Popular End Stations")
plt.bar(pop_station_end.head(10).index, pop_station_end.head(10).values)
plt.ticklabel_format(style = 'plain', axis = 'y')
plt.xticks(rotation = 45)
plt.show()


# From the above data we get an idea of which stations have high activity. This data could be useful in targeted campaigns by marketing team

# #### Recap

# Finally, we will do a recap of the findings before proceeding for recommendations
# 
# 1) There's a large share of casual riders to be addressed
# 2) We found the trends between the 2 rider types like
#     1) Weekly and monthly riding habits
#     2) Duration of their rides
#     3) Type of bike preference
# 3) Stations with most activity i.e. popular stations

# ### Recommendations
# 
# 1) Marketing campaign offering membership offers should focus on most popular stations and be during: 
#     
#     a) the busiest casual riders days i.e. during weekends and
#     b) the busiest months of the year i.e. during summer
# 
# 2) Weekend discounts can be introduced to the member riders to increase their activity during weekends and will also be lucrative deal for casual members who prefer riding on weekends
# 
# 3) Dockers can be on discounted rate for members as they are currently only used by casual riders. This will attract casual members who prefer dockers to consider membership
