import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
from datetime import datetime


def animate(i):
    ax.set_title(datetime.utcfromtimestamp(ts_i+i*10))
    scat.set_offsets(offsets[i])

ts_i = 1570665600
#conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
conn = psycopg2.connect("dbname=taxi_services user=joao")
register(conn)
cursor_psql = conn.cursor()


scale=1/50000
zoomx = 7500
zoomy = 4000
city="Porto"
lon = -8.623
lat = 41.16
sql = "SELECT ST_Transform(ST_PointFromText('POINT(" + str(lon) + " " + str(lat) +")', 4326),3763)"


cursor_psql.execute(sql)
results = cursor_psql.fetchall()
center_lon = results[0][0][0]
center_lat = results[0][0][1]

xs_min = center_lon - zoomx
xs_max = center_lon + zoomx
ys_min = center_lat - zoomy
ys_max = center_lat + zoomy

width_in_inches = (xs_max-xs_min)/0.0254
height_in_inches = (ys_max-ys_min)/0.0254

#print(width_in_inches*scale, height_in_inches*scale)

fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale),dpi=150)
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min,ys_max))

def polygon_to_points(polygon):
    xs, ys = [],[]
    for (x,y) in polygon.coords:
        xs.append(x)
        ys.append(y) 
    return xs,ys



#É ESTAAAAAAA
sql = "SELECT concelho,st_union(proj_boundary) from cont_aad_caop2018 where distrito in ('PORTO') group by concelho"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
#print(results[0])


for row in results:
    polygon = row[1][0]
    xs,ys = polygon_to_points(polygon)
    plt.plot(xs,ys,color='black',lw='0.6')

sql = "SELECT concelho,proj_boundary from cont_aad_caop2018 where distrito in ('PORTO')"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
#print(results[0])


for row in results:
    polygon = row[1][0]
    xs,ys = polygon_to_points(polygon)
    plt.plot(xs,ys,color='black',lw='0.3')
    plt.fill(xs,ys,"grey", alpha=0.2)

offsets = []
with open('offsets1.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    i=0
    for row in reader:
        l = []
        for j in row:
            x,y = j.split()
            x = float(x)
            y = float(y)
            l.append([x,y])
        offsets.append(l)

#print("len_ofssets", len(offsets))

x,y = [],[]
for i in offsets[0]:
    x.append(i[0])
    y.append(i[1])

scat = ax.scatter(x,y,s=4,color='red')
anim = FuncAnimation(
    fig, animate, interval=10, frames=len(offsets)-1, repeat = False)

""" writervideo = animation.PillowWriter(fps=30)
anim.save('rgenerate.gif',writer=writervideo) """

""" plt.draw()
plt.show() """

anim.save("rotas.mp4")