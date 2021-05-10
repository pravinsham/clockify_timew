#!/usr/bin/python3
import pandas as pd
import json
import datetime
import sys
import numpy as np
from datetime import timedelta
from datetime import datetime
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 200)
header = 1
configuration = dict()
DATEFORMAT = '%Y%m%dT%H%M%SZ'
body = ''
def listTostring(s):
    str1 = ""
    for ele in s:
        str1 += ele
    str1 = str1[0:3]
    return str1
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
df['start_pivot']=[i.strftime('%Y-%b-%d') for i in df['start']]
df['end'] = pd.to_datetime(df["end"])
df['total_hours'] = round(((df.end - df.start)/pd.Timedelta(minutes = 1))/60,2)
df['project'] = [listTostring(i) for i in df["tags"]]

print('---------------clockify_effort_filling----------------------')
pivot_values_1 = pd.pivot_table(df, index = ['project'],values=["total_hours"], columns=['start_pivot'], aggfunc= np.sum , fill_value=0)
print(pivot_values_1.iloc[:,-7:])






