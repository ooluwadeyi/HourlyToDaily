
import numpy as np
import pandas as pd
import sys
import os
import glob
import re
import datetime

path = sys.argv[1]
df = pd.read_csv(path)

df = df.rename(columns={'water_level(ft below land surface)':'waterlevel', 'battery_voltage(v)':'batteryvoltage'})
df['avgDailyWater'] = np.zeros(df.shape[0], dtype=float)

HOURS = 24
count = 0
waterlevel_count = 0

#date1 = datetime.datetime.strptime(df.datetime[0], "%m/%d/%y")

date2 = df.datetime[0].rsplit(" ", 2)


#print date2[0]



for i in df.index:
    count += 1
    waterlevel_count += df.ix[i, 'waterlevel'] 
    
    if (i == df.index[-1]):

        level_avg = float(waterlevel_count)/ (count)
        df.ix[i, 'avgDailyWater'] = level_avg
        count = 0
        waterlevel_count = 0

    elif (df.datetime[i].rsplit(" ", 2)[0] != df.datetime[i+1].rsplit(" ", 2)[0]):
        # if count == 1:
        #     df.ix[i, 'avgDailyWater'] = df.ix[i-1, 'waterlevel']
        #else:   
        level_avg = float(waterlevel_count)/ (count)
        df.ix[i, 'avgDailyWater'] = level_avg
        count = 0
        waterlevel_count = 0

for i in df.index:
    #if (df[i, 'avgDailyWater'] !=0)

    df.ix[i, 'NewLevel'] = df.ix[i, 'avgDailyWater']
    df.ix[i, 'NewDate'] = df.ix[i, 'datetime']      

# #print df.head(24)
df['NewDate'] = pd.to_datetime(df['NewDate'])


df = df[df.NewLevel != 0]


new_path = "".join(["Daily_", path])


df.to_csv(new_path, encoding='utf-8')
 
print("done processing file %s") %(path)

