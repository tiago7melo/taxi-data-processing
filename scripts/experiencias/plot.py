import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from datetime import datetime
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register


def polygon_to_points(polygon):
    xs, ys = [],[]
    for (x,y) in polygon.coords:
        xs.append(x)
        ys.append(y) 
    return xs,ys

scale=1/30000
conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
#conn = psycopg2.connect("dbname=taxi_services user=joao")
register(conn)
cursor_psql = conn.cursor()


xs_min, xs_max, ys_min, ys_max = -47000, -34000, 163000, 169000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1

fig, ax = plt.subplots(figsize=(15,7.5))
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min,ys_max))

#É ESTAAAAAAA
sql = "SELECT proj_boundary from cont_aad_caop2018 where concelho in ('PORTO')"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
#print(results[0])

for row in results:
    polygon = row[0][0]
    xs,ys = polygon_to_points(polygon)
    plt.plot(xs,ys,color='black',lw='0.2')

def animate(n):
    delete = []
    for i in range(len(xs)):
        if n<ts[i][0]:
            break
        if n==ts[i][0]:
            if state[i]=='BUSY':
                col="red"
            elif state[i]=='FREE':
                col="green"
            else:
                col="blue"
            scat[i]=ax.scatter(xs[i][n-ts[i][0]],ys[i][n-ts[i][0]],s=5,edgecolors=col)
        elif n>ts[i][0] and n<ts[i][1]:
            scat[i].set_offsets([xs[i][n-ts[i][0]],ys[i][n-ts[i][0]]])
        elif n==ts[i][1]:
            scat[i]=ax.scatter(xs[i][n-ts[i][0]-1],ys[i][n-ts[i][0]-1],s=5,edgecolors="black")
            delete.append(i)
    for i in delete:
        scat.pop(i)
        ts.pop(i)
        xs.pop(i)
        ys.pop(i)
    if n%100 == 0:
        print(n)
    #plt.title()
    


scale=1/60000
conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
cursor_psql = conn.cursor()



sql = """select proj_track,ts,state from tracks, cont_aad_caop2018 where st_within(proj_track,proj_boundary) and concelho='PORTO' order by ts limit 100"""
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
initial_ts = results[0][1]
maximum=-1

xs, ys, scat, state,ts= [], [], [], [], []
for i in range(len(results)):
    xs.append([])
    ys.append([])
    ts.append([])
    scat.append(None)
    state.append(results[i][2])
    xy = results[i][0].coords
    for (x,y) in xy:
        xs[i].append(x)
        ys[i].append(y)
    #print(len(xs[i]), results[i][1],datetime.fromtimestamp(results[i][1]), datetime.fromtimestamp(results[i][1]+len(xs[i])))
    if i%100==0:
        print(i,len(results))
    ts[i].append(results[i][1]-initial_ts)
    ts[i].append(ts[i][0]+len(xs[i]))
    if ts[i][1]>maximum:
        maximum=ts[i][1]
#print(state)

print(maximum)

if state[i]=='BUSY':
    col="red"
elif state[i]=='FREE':
    col="green"
else:
    col="blue"

scat[0] = ax.scatter(xs[0][0],ys[0][0],s=5,edgecolors=col)
""" scat1 = ax.scatter(0,0,s=10)
xxs[1].append(xs[1][0])
yys[1].append(ys[1][0]) """

anim = animation.FuncAnimation(
    fig, animate, interval=1, frames=maximum-1)

""" writervideo = animation.PillowWriter(fps=10000)
anim.save('rota1.gif',writer=writervideo) """

plt.draw()
plt.show()



conn.close()