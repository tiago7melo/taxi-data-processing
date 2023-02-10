import matplotlib.pyplot as plt
import numpy as np
import psycopg2

def polygon_to_points(polygon_string):
    xs, ys = [],[]
    points = polygon_string[9:-2].split(',')
    for point in points:
        (x,y) = point.split()
        xs.append(float(x))
        ys.append(float(y))
    return xs,ys

scale=1/30000
#conn = psycopg2.connect("dbname=TABD user=tiago")
conn = psycopg2.connect("dbname=taxi_services user=joao")
cursor_psql = conn.cursor()
sql = "select  st_astext(proj_location), count(initial_point_proj) from taxi_stands, taxi_services where st_distance(proj_location,initial_point_proj) < 150 GROUP BY 1 ORDER BY 2;"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

xs = []
ys = []
num_services = []
for row in results:
    point_string = row[0]
    num_services.append(row[1])
    point_string = point_string[6:-1]
    (x,y) = point_string.split()
    xs.append(float(x))
    ys.append(float(y))
width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1
fig = plt.figure(figsize=(width_in_inches*scale,height_in_inches*scale))
plt.scatter(xs,ys,c=num_services,s=30,cmap='jet')
plt.colorbar()

sql = "select st_astext(proj_boundary) from cont_aad_caop2018 where concelho in ('PORTO')"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
for row in results:
    polygon_string = row[0]
    xs, ys = polygon_to_points(polygon_string)
    plt.plot(xs,ys,color='gray')

plt.show()
