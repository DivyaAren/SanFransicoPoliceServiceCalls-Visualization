#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd


# In[5]:


df = pd.read_csv("b.csv")


# In[6]:


df.head(10)


# In[7]:


print("Police Service Calls -  rows:", df.shape[0]," columns:", df.shape[1])


# In[8]:


#checking for null records
df['Original_Crime_Type_Name'].isnull()


# In[9]:


#checking for missing values
print (df.isnull().sum())


# In[10]:


#Replace Law Code Section with name 
df = df.replace("22500e", "Improper parking stopping or standing")


# In[12]:


#creating new columns for identifying calls received during daytime and at night
df['year'] = pd.DatetimeIndex(df['Call_Date']).year
df['hour'] = df['Call_Time'].apply(lambda s: int(s.split(':')[0]))
df['is_day'] = df['hour'].apply(lambda s: int(1 if s>=6 and s<=18 else 0))
df['months'] = pd.DatetimeIndex(df['Call_Date']).month
df['my'] = df['months']+df['year']*100
df['ts'] = pd.DatetimeIndex(df['Call_Date_Time'])
m ={
    1:"Jan ",
    2:"Feb ",
    3:"Mar ",
    4:"Apr ",
    5:"May ",
    6:"Jun ",
    7:"Jul ",
    8:"Aug ",
    9:"Sep ",
    10:"Oct ",
    11:"Nov ",
    12:"Dec ",
}
df['mname'] = df['months'].apply(lambda s: m[int(s)])


# In[37]:


df.head(10)


# In[13]:


#Top 10 crimes 
crimes = df['Original_Crime_Type_Name'].value_counts().iloc[:10]


# In[14]:


#Indexing Top 10 crimes
crime_list = list (crimes.index)


# In[15]:


#Sorting Top 10 Crimes
crime_list.sort()


# In[16]:


crime_list


# In[56]:


x= df[['Original_Crime_Type_Name', 'year', 'is_day']]


# In[57]:


x.head(10)


# In[58]:


#total number of cases
len(x.index)


# In[59]:


#total number of cases of top 10 crimes
p = x[x['Original_Crime_Type_Name'].isin(crime_list)]


# In[60]:


len(p.index)


# In[61]:


p.head(10)


# In[62]:


my_ans = p.groupby(['Original_Crime_Type_Name','year']).agg({"Original_Crime_Type_Name":"count"})


# In[63]:


my_ans.to_csv('dibs.csv')


# In[64]:


p.to_csv('dibs2.csv')


# In[65]:


is_audible_vala = (x['Original_Crime_Type_Name']=='Audible Alarm')


# In[66]:


my_ans


# In[67]:


df_m  = pd.read_csv('dibs.csv')


# In[68]:


df_m.columns


# In[69]:


list(set(df_m['Original_Crime_Type_Name'].values))


# In[70]:


cri = df_m.pivot_table('Original_Crime_Type_Name.1', ['year'], 'Original_Crime_Type_Name').transpose()


# In[71]:


#data for visualisation 1
cri


# In[72]:


cri.to_csv("bar_race.csv")


# In[107]:


x


# In[73]:


x['year'].value_counts()


# In[74]:


p = (x['Original_Crime_Type_Name'].value_counts())


# In[105]:


p.head(10)


# In[113]:


is_2019 = (x['year']==2019)


# In[122]:


is_day = (x['is_day']==1) 
is_night = (x['is_day']==0)


# In[115]:


x[is_2019]


# In[116]:


x[is_day]


# In[120]:


g1 = x[is_2019 & is_day]
x[is_day].groupby(['year']).agg({"year":"count"})


# In[135]:


p1 = x.groupby(['year','is_day']).agg({"year":"count"})
p1


# In[138]:


p1.to_csv('sec1.csv')


# In[139]:


p2 = pd.read_csv('sec1.csv')


# In[141]:


p2.columns


# In[145]:


p2


# In[148]:


#data for visualization 2
p2.pivot_table('year.1',['is_day'],'year').transpose()


# In[94]:


import matplotlib.pyplot as plt
from wordcloud import WordCloud
fields = ['Original_Crime_Type_Name']
text2 = pd.read_csv('b.csv', usecols=fields)
text3 = ' '.join(text2['Original_Crime_Type_Name'])
wordcloud2 = WordCloud().generate(text3)
# Generate plot
plt.imshow(wordcloud2)
plt.figure(figsize=[50,50])
plt.axis("off")
plt.show()


# In[101]:


def multi_color_func(word=None, font_size=None,
                     position=None, orientation=None,
                     font_path=None, random_state=None):
    colors = [[4, 77, 82],
              [25, 74, 85],
              [82, 43, 84],
              [158, 48, 79]]
    rand = random_state.randint(0, len(colors) - 1)
    return "hsl({}, {}%, {}%)".format(colors[rand][0], colors[rand][1], colors[rand][2])


# In[106]:


# modules for generating the word cloud
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
fields = ['Original_Crime_Type_Name']
text2 = pd.read_csv('b.csv', usecols=fields)
text3 = ' '.join(text2['Original_Crime_Type_Name'])
mask2 = np.array(Image.open('chl.png'))
wc = WordCloud(mask=mask2, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask2.shape[1],
               height=mask2.shape[0], color_func=multi_color_func)
#wc = WordCloud(background_color="white", max_words=2000, mask=mask2,
            #max_font_size=90, random_state=35)
wc.generate(text3)
# create coloring from image
image_colors = ImageColorGenerator(mask2)
plt.figure(figsize=[70,70])
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
_=plt.show()

