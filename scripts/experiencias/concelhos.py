import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register

conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
#conn = psycopg2.connect("dbname=taxi_services user=joao")
register(conn)
cursor_psql = conn.cursor()


scale=1/35000
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

print(width_in_inches*scale, height_in_inches*scale)

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











#plt.savefig('conce.png')
plt.show()