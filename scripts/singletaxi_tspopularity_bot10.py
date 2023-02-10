import matplotlib.pyplot as plt
import numpy as np
import psycopg2

#conn = psycopg2.connect("dbname=TABD user=tiago")
conn = psycopg2.connect("dbname=taxi_services user=joao")
cursor_psql = conn.cursor()
sql = "select  name, count(initial_point_proj) from taxi_stands, taxi_services where taxi_id = 7 and st_distance(proj_location,initial_point_proj) < 150 GROUP BY 1 ORDER BY 2 ASC LIMIT 10;"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

labels = []
services = []

for row in results:
    print(row[0], " ", row[1])
    labels.append(row[0])
    services.append(row[1])


fig, ax = plt.subplots()

width = 0.4 #width of bars
x = np.arange(10) #label locations

p1 = ax.bar(x,services,width,yerr=0)

ax.set_ylabel('Services started within 150m of stand')
ax.set_title('Taxi 7 - Least Favourite Taxi Stands')
ax.set_xticks(x)
ax.set_xticklabels(labels)

#ax.bar_label(p1,label_type='center')

fig.tight_layout()

plt.show()
