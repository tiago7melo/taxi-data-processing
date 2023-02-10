import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns;
import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register


minx = -46843.16270000022
miny = 163345.06010000035

a = np.ones((53, 116))

conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
register(conn)
cursor_psql = conn.cursor()

sql ="select final_point_proj from taxi_services, cont_aad_caop2018 where st_within(final_point_proj,proj_boundary) and concelho='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

for result in results:
    (x,y) = result[0].coords
    y1=int((y-miny)/100)
    x1=int((x-minx)/100)
    a[y1][x1] = a[y1][x1] + 1

a=np.log10(a)



fig = plt.figure(figsize=(12,5.2))

ax = sns.heatmap(a)
ax.set_axis_off()
fig.add_axes(ax)
ax.invert_yaxis()


#É ESTAAAAAAA
sql = "SELECT proj_boundary from cont_aad_caop2018 where concelho in ('PORTO')"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

for row in results:
    xs=[]
    ys=[]
    for (x,y) in row[0][0].coords:
        if(x<minx):
            minx=x
        if(y<miny):
            miny=y
        xs.append((x-minx)/100)
        ys.append((y-miny)/100)
    plt.plot(xs,ys,color='white',lw='0.5')

plt.savefig('heatmap_final.png')
conn.close()