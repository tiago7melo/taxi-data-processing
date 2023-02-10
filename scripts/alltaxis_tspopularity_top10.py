import matplotlib.pyplot as plt
import numpy as np
import psycopg2
from collections import defaultdict

#conn = psycopg2.connect("dbname=TABD user=tiago")
conn = psycopg2.connect("dbname=taxi_services user=joao")
cursor_psql = conn.cursor()

sql = "select distinct name from taxi_stands"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

ts_name = []
for row in results:
    ts_name.append(row[0])

sql = "select distinct taxi_id from taxi_services"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

taxi_ids = []
for row in results:
    taxi_ids.append(row[0])

popularity = defaultdict(int)

for id in taxi_ids:
    sql = "select name, count(initial_point_proj) from taxi_stands, taxi_services where taxi_id = {} AND st_distance(proj_location,initial_point_proj) < 150 GROUP BY 1 ORDER BY 2 DESC LIMIT 1;".format(id)
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    print(id)
    if len(results) > 0:
            popularity[results[0][0]] += 1
    
popularity = {key:value for key,value in sorted(popularity.items(),key = lambda item: item[1],reverse=True)}

top_stands = [key for key in list(popularity.keys())[:10]]
top_stands_count = [value for value in list(popularity.values())[:10]]

for stand in popularity:
    print(stand + ": " + str(popularity[stand]))

fig, ax = plt.subplots()

width = 0.4 #width of bars
x = np.arange(10) #label locations

p1 = ax.bar(x,top_stands_count,width,yerr=0,color='red')

ax.set_ylabel('Amount of drivers who use stand the most of all stands')
ax.set_title('Most Popular Stands among drivers')
ax.set_xticks(x)
ax.set_xticklabels(top_stands)

#ax.bar_label(p1,label_type='center')

fig.tight_layout()

plt.show()

cursor_psql.close()
conn.close()
#print bar chart


