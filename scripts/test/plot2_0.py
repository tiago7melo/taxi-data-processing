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
#conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
conn = psycopg2.connect("dbname=taxi_services user=joao")
register(conn)
cursor_psql = conn.cursor()


xs_min, xs_max, ys_min, ys_max = -47000, -34000, 163000, 169000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1

fig, ax = plt.subplots(figsize=(15,7.5))

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
    for i in range(len(xs)):
        if state[i]=='BUSY':
            col="red"
        elif state[i]=='FREE':
            col="green"
        else:
            col="blue"
        if(xs[i][n]!=0 and scat[i]==None):
            scat[i]=ax.scatter(xs[i][n],ys[i][n],s=5)
        elif(xs[i][n]!=0):
            scat[i].set_offsets([xs[i][n],ys[i][n]])
            xxs[i].append(xs[i][n])
            yys[i].append(ys[i][n])
            ax.plot(xxs[i],yys[i], color=col, lw='0.5')
    if n%100 == 0:
        print(n)
    """ scat.set_offsets([xs[1][i],ys[1][i]])
    xxs[1].append(xs[1][i])
    yys[1].append(ys[1][i])
    ax.plot(xxs[1],yys[1], color="blue", lw='0.5') """
    #plt.title()
    


scale=1/60000
conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
cursor_psql = conn.cursor()



sql = """select proj_track,ts,state from tracks, cont_aad_caop2018 where st_intersects(proj_track,proj_boundary) and concelho='PORTO' order by ts"""
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
initial_ts = results[0][1]
maximum = -1

xs, xxs, ys, yys, scat, state = [], [], [], [], [], []
for i in range(len(results)):
    xs.append([])    
    xxs.append([])    
    ys.append([])
    yys.append([])
    scat.append(None)
    state.append(results[i][2])
    ts_dif = results[i][1] - initial_ts
    if ts_dif>0:
        for j in range(ts_dif):
            xs[i].append(0)
            ys[i].append(0)
    xy = results[i][0].coords
    for (x,y) in xy:
        xs[i].append(x)
        ys[i].append(y)
    print(len(xs[i]), results[i][1],datetime.fromtimestamp(results[i][1]), datetime.fromtimestamp(results[i][1]+len(xs[i])))
    if len(xs[i]) > maximum:
        maximum = len(xs[i])

print(state)

print()

for i in range(len(xs)):
    max_dif = maximum - len(xs[i])
    if max_dif > 0:
        for j in range(max_dif):
            xs[i].append(0)
            ys[i].append(0)

for i in xs:
    print(len(i))

print()

scat[0] = ax.scatter(xs[0][0],ys[0][0],s=5)
xxs[0].append(xs[0][0])
yys[0].append(ys[0][0])
""" scat1 = ax.scatter(0,0,s=10)
xxs[1].append(xs[1][0])
yys[1].append(ys[1][0]) """

anim = animation.FuncAnimation(
    fig, animate, interval=1, frames=len(ys[7])-1)

writervideo = animation.PillowWriter(fps=30)
anim.save('rota.gif',writer=writervideo)

""" plt.draw()
plt.show() """
conn.close()


""" # importing all necesaary libraries
from itertools import count
import random
import matplotlib
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# add random points for each line
l1 = [random.randint(-20, 4)+(points**1.88)/(random.randint(13, 14))
	for points in range(0, 160, 2)]
l2 = [random.randint(0, 9)+(points**1.9)/(random.randint(9, 11))
	for points in range(0, 160, 2)]
l3 = [random.randint(-10, 10)-(points**1.4)/(random.randint(9, 12))
	for points in range(0, 160, 2)]
l4 = [random.randint(-5, 10)-(points**1.1)/(random.randint(7, 12))
	for points in range(0, 160, 2)]

myvar = count(0, 3)

# subplots() function you can draw
# multiple plots in one figure
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))

# set limit for x and y axis
axes.set_ylim(-100, 500)
axes.set_xlim(0, 250)

# style for plotting line
plt.style.use("ggplot")

# create 5 list to get store element
# after every iteration
x1, y1, y2, y3, y4 = [], [], [], [], []
myvar = count(0, 3)

def animate(i):
	x1.append(next(myvar))
	y1.append((l1[i]))
	y2.append((l2[i]))
	y3.append((l3[i]))
	y4.append((l4[i]))

	axes.plot(x1, y1, color="red")
	axes.plot(x1, y2, color="gray")
	axes.plot(x1, y3, color="blue")
	axes.plot(x1, y4, color="green")


# set ani variable to call the
# function recursively
anim = FuncAnimation(fig, animate, interval=30)

plt.show() """

