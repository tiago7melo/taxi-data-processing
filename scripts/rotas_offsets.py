import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
import logging

conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
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

#define the step in seconds of the animation
step = 10


sql = "select distinct taxi from tracks where st_intersects(proj_track,ST_PolygonFromText('POLYGON((" + str(xs_min) + " " + str(ys_min) + ", " + str(xs_max) + " " + str(ys_min) + ", " + str(xs_max) + " " + str(ys_max) + ", " + str(xs_min) + " " + str(ys_max) + "," + str(xs_min) + " " + str(ys_min)+"))',3763)) order by 1"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

taxis_x ={}
taxis_y ={}

ts_i = 1570665600
#ts_f = 1570668999
ts_f = 1570751999

array_size = int(24*60*60/step)
for row in results:
    taxis_x[int(row[0])] = np.zeros(array_size)
    taxis_y[int(row[0])] = np.zeros(array_size)


for i in range(ts_i,ts_f,10):
    sql = "select taxi,st_pointn(proj_track," + str(i) + "-ts) from tracks where ts<" + str(i) + " and ts+st_numpoints(proj_track)>" + str(i) + " and st_intersects(proj_track,ST_PolygonFromText('POLYGON((" + str(xs_min) + " " + str(ys_min) + ", " + str(xs_max) + " " + str(ys_min) + ", " + str(xs_max) + " " + str(ys_max) + ", " + str(xs_min) + " " + str(ys_max) + "," + str(xs_min) + " " + str(ys_min)+"))',3763))"


    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    for row in results:
        x,y = row[1].coords
        taxis_x[int(row[0])][int((i-ts_i)/10)] = x
        taxis_y[int(row[0])][int((i-ts_i)/10)] = y
    if(i%100==0):
        logging.warning(i,ts_f)

offsets = []

for i in range(array_size):
    l = []
    for j in taxis_x:
        l.append([taxis_x[j][i],taxis_y[j][i]])
    offsets.append(l)
    logging.warning(len(l))

for i in offsets:
    print("%f %f" %(i[0][0],i[0][1]),end='')
    for j in range(1,len(i)):
        print(",%f %f" %(i[j][0],i[j][1]),end='')
    print("")

conn.close()