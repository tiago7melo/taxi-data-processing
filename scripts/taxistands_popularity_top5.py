import matplotlib.pyplot as plt
import numpy as np
import psycopg2

#conn = psycopg2.connect("dbname=TABD user=tiago")
conn = psycopg2.connect("dbname=taxi_services user=joao")
cursor_psql = conn.cursor()
sql = "select  name, count(initial_point_proj) from taxi_stands, taxi_services where st_distance(proj_location,initial_point_proj) < 150 GROUP BY 1 ORDER BY 2 DESC LIMIT 5;"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

labels = []
services = []

for row in results:
    print(row[0], " ", row[1])
    labels.append(row[0])
    services.append(row[1])


fig, ax = plt.subplots()

width = 0.8 #width of bars
x = np.arange(5) #label locations

p1 = ax.bar(x,services,width,yerr=0,color='red')

ax.set_ylabel('Services started within 150m of stand')
ax.set_title('Popularity of Taxi Stands in Porto')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

#ax.bar_label(p1,label_type='center')

fig.tight_layout()

plt.show()
