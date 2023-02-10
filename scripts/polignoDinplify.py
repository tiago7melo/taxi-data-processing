from typing import Sized
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import psycopg2
import math
import numpy as np
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register
from matplotlib.animation import FuncAnimation
 

conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
#conn = psycopg2.connect("dbname=taxi_services user=joao")
register(conn)
cursor_psql = conn.cursor()
 
 
def polygon_to_points(polygon):
    xs, ys = [],[]
    for (x,y) in polygon.coords:
        xs.append(x)
        ys.append(y) 
    return xs,ys
 
v=[0,1,5,10,25,150,250,500,1000]

for i in v:
    sql="SELECT st_union(st_simplify(proj_boundary,"+str(i)+",False)) from cont_aad_caop2018 where concelho in ('PORTO') group by concelho;"
 
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    for row in results:
        polygon = row[0][0]
        fig,ax=plt.subplots(figsize=(17,9))
        ax.axis('off')
        xs,ys = polygon_to_points(polygon)
        print("i: ",i," xs: ", len(xs)," ys: ",len(ys))
        plt.plot(xs,ys,color='black',lw='0.5')
        plt.title("Simplify factor: " + str(i) + "\nNº of points: "+str(len(xs)))
        #plt.draw()
        #plt.show()
        plt.savefig("simplify"+str(i)+".png")

v=[]
c=[]

for i in range(0,1000,5):
    sql="SELECT st_union(st_simplify(proj_boundary,"+str(i)+",False)) from cont_aad_caop2018 where concelho in ('PORTO') group by concelho;"
 
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    for row in results:
        polygon = row[0][0]
        xs,ys = polygon_to_points(polygon)
        v.append(i)
        c.append(len(xs))
        #plt.draw()
        #plt.show()
 
 
plt.clf()
plt.plot(v,c, 'o-', linewidth='2')
#plt.show()
plt.savefig("plotSimplify.png")

plt.clf()
plt.loglog(v,c, 'o-', linewidth='2')
#plt.show()
plt.savefig("plotSimplify_log.png")