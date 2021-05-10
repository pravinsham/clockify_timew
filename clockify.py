#!/usr/bin/python3
import pandas as pd
import json
import datetime
import sys
import numpy as np
from datetime import timedelta
from datetime import datetime
pd.set_option('display.max_columns', 5)
pd.set_option('display.width', 200)
header = 1
configuration = dict()
DATEFORMAT = '%Y%m%dT%H%M%SZ'
body = ''
for line in sys.stdin:
    if header:
        if line == '\n':
            header = 0
        else:
            fields = line.strip().split(': ', 2)
            if len(fields) == 2:
                configuration[fields[0]] = fields[1]
            else:
                configuration[fields[0]] = ''
    else:
         body += line
df = pd.DataFrame(json.loads(body))
df['start'] = pd.to_datetime(df["start"])
df['end'] = pd.to_datetime(df["end"])
df['total_hours'] = (df.end - df.start)/pd.Timedelta(hours = 1)
df['project'] = [i[i.find('$'):6] for i in df['annotation']]
#df['startdate'] = df['start'].dt.normalize()
#df['startdate'] = df['startdate'].dt.strftime('%Y-%m-%d')
#df['enddate'] = df['end'].dt.normalize()
#df['enddate'] = df['enddate'].dt.strftime('%Y-%m-%d')
def get_date_range(date_value):
    #date_value = datetime.strptime(date_value, '%Y-%m-%d')
    start_of_week = date_value - timedelta(days = date_value.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.strftime('%Y-%b-%d') + ' - ' + end_of_week.strftime('%Y-%b-%d')
#print('---------------Summary with annotations-----------------------')
#print(df.iloc[:,[0,1,2,3]])
print('---------------monthly out put of time-----------------------')
print(pd.pivot_table(df, index = [df['start'].dt.strftime('%Y-%b')], values=["total_hours"] , aggfunc= np.sum))
print('---------------weekly out put of time-----------------------')
pivot_values = pd.pivot_table(df, index =[get_date_range(i) for i in df['start']], values=["total_hours"] , aggfunc= np.sum).sort_values(by='total_hours',ascending = False)
print(pivot_values)
print('---------------print effort by project----------------------')
pivot_values_1 = pd.pivot_table(df, index = ['project'], columns = pd.date_range(start = '2020-11-01', end = '2020-11-15') ,values=["total_hours"], aggfunc= np.sum).sort_values(by='total_hours',ascending = False)
print(pivot_values_1)








