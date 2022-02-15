#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import pdb
import datetime
import time

plt.rc('font', size=14)
df = pd.read_csv('data/merged.csv')
df['date'] = pd.to_datetime(df['date'])
df.head()


# In[ ]:


county_count = df[['state', 'county', 'death', 'injured']].groupby(by=['state', 'county']).sum()
county_count['total'] = county_count['death'] + county_count['injured']
county_count.sort_values(by='total', ascending=False, inplace=True)
county_count.head()


# In[ ]:


def plot_victim_groupby(df, days=3, limit=20, groupby=['state', 'county']):
    df = df[df.date > datetime.datetime.now() - pd.to_timedelta(f'{days}day')]
    count = df[['state', 'county', 'death', 'injured']].groupby(by=groupby).sum()
    count['total'] = count['death'] + count['injured']
    count.sort_values(by='total', ascending=False, inplace=True)
    if len(groupby) == 2:
        labels = [county + ', ' + state for state, county in count[:limit].index]
    else:
        labels = count[:limit].index
    # print(labels)
    
    fig = plt.figure(figsize=(8, 8))
    plt.barh(labels, count[:limit]['death'], label='death', color='black')
    plt.barh(labels, count[:limit]['injured'], left=count[:limit]['death'], label='injured', color='gray')
    plt.legend()
    plt.xlabel('Count')
    plt.ylabel('Location')
    plt.title(f'US gun violence victim count within the past {days} days')
    return fig

fig = plot_victim_groupby(df)
fig.savefig('docs/imgs/victim_city_3days.png')


# In[ ]:


fig = plot_victim_groupby(df, groupby=['state'])
fig.savefig('docs/imgs/victim_state_3days.png')


# In[ ]:


date_count = df[['date', 'injured', 'death']].groupby('date').sum()
date_count['total'] = date_count['injured'] + date_count['death']
date_count


# In[ ]:


def plot_victim_time(df, days=90):
    df = df[df.date > datetime.datetime.now() - pd.to_timedelta(f'{days}day')]
    date_count = df[['date', 'injured', 'death']].groupby('date').sum()
    date_count['total'] = date_count['injured'] + date_count['death']
    fig = plt.figure(figsize=(8, 6))
    plt.bar(date_count.index, date_count['death'], label='death', color='black')
    plt.bar(date_count.index, date_count['injured'], bottom=date_count['death'], color='gray', label='injured')
    xlabels = [date.strftime('%Y-%m-%d') for date in date_count.index]
    plt.xticks(date_count.index, xlabels , rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title(f"Gun violence victim count within {days} days")
    plt.legend()
    return fig

fig = plot_victim_time(df, days=90)
fig.savefig('docs/imgs/victim_count_90days.png')

