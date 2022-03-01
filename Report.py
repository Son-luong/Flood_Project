#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install cufflinks


# In[2]:


import pandas as pd
import numpy as np
import cufflinks as cf
import plotly.graph_objs as go 
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.graph_objs as go 
from plotly.offline import init_notebook_mode,iplot,plot
init_notebook_mode(connected=True) 
import plotly.express as px
from urllib.request import urlopen
import json


# In[3]:


df = pd.read_csv("us_disaster_declarations.csv")
df.head(5)


# In[4]:


sns.heatmap(df.isnull(),
            yticklabels=False,
            cbar=False)


# In[5]:


df.info()


# In[6]:


comparison_column = np.where(df["incident_begin_date"] == df["incident_end_date"], True, False)
df["equal"] = comparison_column
df["equal"].value_counts()


# In[28]:


#fema_declaration_string = declaration_type + disaster_number + state
#df["declaration_request_number"].value_counts()
#df["fema_declaration_string"].value_counts()
df["disaster_number"].value_counts()


# In[8]:


#split date to year, month
df[["begin_year", "begin_month", "begin_time"]] = df["incident_begin_date"].str.split("-", expand = True)
df[["begin_day","x"]] = df["begin_time"].str.split("T", expand = True)
df[["end_year", "end_month", "end_time"]] = df["incident_end_date"].str.split("-", expand = True)
df[["end_day","y"]] = df["end_time"].str.split("T", expand = True)
df


# In[9]:


#Drop repeated information columns, unneccessary infos for analysis
df=df.drop(columns = ["fema_declaration_string","declaration_request_number",
                       "disaster_closeout_date","end_time","begin_time","x","y","incident_end_date","incident_begin_date",
                       "id","hash","last_refresh","equal"])
df


# In[10]:


# What happend in 2020
sns.histplot(df["fy_declared"],kde=False, bins=30)


# In[11]:


#Biological disaster!!!! Covid?
fig = plt.figure(figsize=(30,15))
sns.histplot(data=df,x='fy_declared', stat='count', hue='incident_type', multiple='stack',palette="Paired")
plt.show()


# In[22]:


flood_month= df.loc[(df.incident_type =='Flood'),['begin_month']]
flood_month=flood_month.sort_values(by='begin_month')
sns.histplot(flood_month["begin_month"],kde=True, bins=30)


# In[25]:


flood_state= df.loc[(df.incident_type =='Flood'),['state']]
flood_state = pd.DataFrame(list(flood_state["state"].value_counts().iteritems()))
flood_state.columns =["state","flood_report"]

data = dict(type='choropleth',
            colorscale = 'Viridis',
            reversescale = True,
            locations = flood_state['state'],
            z = flood_state['flood_report'],
            locationmode = 'USA-states',
            text = flood_state['state'],
            marker = dict(line = dict(color = 'rgb(255,255,255)',width = 1)),
            colorbar = {'title':"Floods Declared since 1953"}
            ) 
layout = dict(title = 'Flood Report by State',
              geo = dict(scope = 'usa',
                         showlakes = True,
                         lakecolor = 'rgb(85,173,240)')
             )
choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)


# In[26]:


flood_df= df.loc[(df.incident_type =='Flood'),['state']]
fig = plt.figure(figsize=(20,5))
sns.countplot(x = 'state',
              data = flood_df,
              order = flood_df['state'].value_counts().index,
              palette="crest")
plt.show()


# In[15]:


flood= df.loc[(df.incident_type =='Flood'),['fips']]
flood= pd.DataFrame(list(flood["fips"].value_counts().iteritems()))
flood.columns =["fips","flood_report"]

flood


# In[27]:


from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd

fig = px.choropleth_mapbox(flood, geojson=counties, locations='fips', color='flood_report',
                           color_continuous_scale="Viridis",
                           #range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'flood_report':'Total Flood Report since 1953'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


# In[17]:


tx = df.loc[(df.state == 'TX')&(df.incident_type=='Flood')]


# In[ ]:




