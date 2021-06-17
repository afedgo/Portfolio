import pandas as pd
from collections import Counter

""" Program: Tournament.py
    Author:  Alyssa Fedgo
    Date:   June 17, 2021
    Purpose: Look at top 20 golfers for score and strokes gained total
             in the past 6 and 2 years for a specific tournament
    """

#read in file

df=pd.read_csv('Input.csv',parse_dates=['date'])

# Keep only instances for course of interest and keep features of interest

features=['player','season','final position','course','Score','date','sg_putt',
          'sg_arg','sg_app','sg_ott','sg_t2g','sg_total']

torrey=df[features].loc[df['course'] == 'Torrey Pines - La Jolla, CA']
torrey_2yrs=torrey.loc[(torrey['date'] >= '2019-03-01')]

# Clean score feature
torrey['Score']=torrey['Score'].replace('E','0').astype(float)

#averages for score and strokes gained total

averages =torrey.groupby('player',as_index=False)['Score'].mean()


averages2=torrey_2yrs.groupby('player',as_index=False)['Score'].mean()


avg_tot=torrey.groupby('player',as_index=False)['sg_total'].mean()


avg_tot2=torrey_2yrs.groupby('player',as_index=False)['sg_total'].mean()

#combine series to a dataframe

data = [averages.nsmallest(20,'Score'),
        averages2.nsmallest(20,'Score'),
        avg_tot.nlargest(20,'sg_total'),
        avg_tot2.nlargest(20,'sg_total')]

all=pd.concat(data,axis=0)

#Count how many times the players appear in the stats categories I created

stats=Counter(all['player'])
print(stats)

stats_df = pd.DataFrame.from_dict(stats, orient='index').reset_index()

#output results

stats_df.to_csv('Predictions.csv')
all.to_csv('All.csv')
