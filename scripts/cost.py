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

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def cost(id):
    #print("TaxiId: " + str(id))
    # Select ST_length(proj_track) from tracks where id=1;
    #sql = "SELECT N, ST_Distance(ST_Pointn(proj_track,N), ST_PointN(proj_track, n+1)) as D from tracks, (SELECT generate_series(1,ST_NumPoints(proj_track)-1) as N from tracks where id=" + str(id) + ") as X where id=" + str(id);
    sql = "SELECT ts,proj_track, ST_length(proj_track) FROM tracks WHERE id="+str(id)
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    xy = results[0][1].coords
    ts = results[0][0]
    dt_object = datetime.fromtimestamp(ts)
    #print(dt_object)
    if (dt_object.hour>6 and dt_object.hour<21):
        #print("DIA")
        distance_fare = 212.77
        bandeirada=1800
        total_money = 3.25
    else:
        #print("NOITE")
        distance_fare = 178.57
        bandeirada=1440
        total_money = 3.9
    #print(distance_fare)
    seconds = 0
    total_time=0
    total_distance=0
    distance = 0
    flag_first = 1
    flag_bandeirada = 1
    #print(len(xy))
    for (x,y) in xy:
        seconds+=1
        total_time+=1
        if(flag_first == 1):
            prevX = x
            prevY = y
            flag_first = 0
        else:
            distance_aux = math.sqrt(abs(x-prevX)**2+abs(y-prevY)**2)
            #print("      Dist: " + str(distance_aux))
            if(distance_aux<56):
                distance += distance_aux
                total_distance += distance_aux
                prevX=x
                prevY=y

        if(flag_bandeirada == 1):
            if distance >= bandeirada:
                flag_bandeirada = 0
                seconds = 0
                distance -= bandeirada
        else:
            if(seconds==24):
                total_money+=0.1
                seconds=0
                distance=0
                continue
            if (distance >= distance_fare):
                total_money+=0.1
                seconds=0
                distance-=distance_fare

    return total_money

def med_cost_concelho(conc):
    cost_conc=0
    sql = "SELECT tracks.id from tracks, cont_aad_caop2018 WHERE state='BUSY' AND concelho='" + conc +"' AND ST_Within(ST_StartPoint(proj_track), proj_boundary)"
    cursor_psql.execute(sql)

    results = cursor_psql.fetchall()

    for row in results:
        cost_conc += cost(row[0])

    medium = cost_conc/len(results)
    
    #print("Concelho " + conc + " with " + str(len(results)) + " tracks got a medium value of: " + str(medium))

    return medium
        
def polygon_to_points(polygon):
    xs, ys = [],[]
    for (x,y) in polygon.coords:
        xs.append(x)
        ys.append(y) 
    return xs,ys

def print_concelho(conc, grad,cost_med,num):
    plt.clf()

    sql ="select st_envelope(st_collect(st_simplify(proj_boundary,100,FALSE))) from cont_aad_caop2018 where concelho='" + conc + "'"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    polygon= results[0][0][0]

    xs,ys = polygon_to_points(polygon)

    proportion = ((max(ys)-min(ys))/(max(xs)-min(xs)))

    width = 7
    height = (width * proportion) + 1
    fig, ax = plt.subplots(figsize=(width,height))

    #É ESTAAAAAAA
    sql = "SELECT st_union(proj_boundary) from cont_aad_caop2018 where concelho='" + conc + "' group by concelho"
    #print(sql)
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    #print(results[0])

    polygon = results[0][0][0]
    xs,ys = polygon_to_points(polygon)
    plt.title(conc + '\n' + 'Average prince: ' + str(round(cost_med,2)) + '€', fontsize='large')
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.plot(xs,ys,color='black',lw='0.2')
    plt.fill(xs,ys,"r", alpha=grad)

    plt.savefig(str(num)+conc+'.png')


def select_concelhos():
    sql = "select concelho, count(tracks.id) from tracks, cont_aad_caop2018 where state='BUSY' and ST_Within(ST_StartPoint(proj_track),proj_boundary) group by concelho order by count(tracks.id) desc limit 13"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    
    dict = {}
    arr = []

    for row in results:
        med = med_cost_concelho(row[0])
        print(row[0], round(med_cost_concelho(row[0]),2))
        arr.append(round(med,4))
        dict[round(med,4)] = row[0]
    return dict,arr


"""
MAIA:                120     9.96
MATOSINHOS:          1014    6.71
OEIRAS:              758     6.65
GONDOMAR:            711     5.91
AVEIRO:              482     5.91
VILA NOVA DE GAIA:   1870    5.89
PORTO:               4646    5.77
LISBOA:              4754    5.69
ODIVELAS:            1332    5.48
SINTRA:              2955    5.32
BRAGA:               1230    4.98
COIMBRA:             4026    4.93
LOURES:              425     4.57
"""


dictionary,array = select_concelhos()
array.sort()

alpha = 1/12
x=0
for i in range(len(array)):
    print_concelho(dictionary[array[i]],x,array[i],i+1)
    x=x+alpha
    if x>1:
        x=1


#print_concelho('MAIA')