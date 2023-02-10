import matplotlib.pyplot as plt
import matplotlib.animation as animation
import psycopg2
import math
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register

conn = psycopg2.connect("dbname=taxi_services user=joao")
register(conn)
cursor_psql = conn.cursor()


city = "Aveiro"
lon = -8.653783
lat = 40.642147

city="Porto"
lon = -8.629179
lat = 41.158030

#city="Lisboa"
#lon = -9.149975
#lat = 38.725306

#city="Coimbra"
#lon = -8.407956
#lat = 40.204070

# execução da Query a BD a procurar 
sql = "SELECT ST_Transform(ST_PointFromText('POINT(" + str(lon) + " " + str(lat) +")', 4326),3763)"

sql2="SELECT ST_Transform(ST_PointFromText(POINT(-8.629179,41.158030), 4326),3763)"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()
center_lon = results[0][0][0]
center_lat = results[0][0][1]

# defenir escala e zoom(proximodade)
scale = 1/15000
zoom = 6000

# defenir tema escuro
plt.style.use('dark_background')

# defenir tamanho da janela do mapa 
xs_min = center_lon - zoom
xs_max = center_lon + zoom
ys_min = center_lat - zoom
ys_max = center_lat + zoom
width_in_inches = (xs_max-xs_min)/0.0254
height_in_inches = (ys_max-ys_min)/0.0254

# plot
fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale), dpi=300)
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min,ys_max))


#
sql = "select proj_track from tracks where st_intersects(proj_track,ST_PolygonFromText('POLYGON((" + str(xs_min) + " " + str(ys_min) + ", " + str(xs_max) + " " + str(ys_min) + ", " + str(xs_max) + " " + str(ys_max) + ", " + str(xs_min) + " " + str(ys_max) + "," + str(xs_min) + " " + str(ys_min)+"))',3763))"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

for track in results:
    if type(track[0]) is LineString:
        xy = track[0].coords
        xxx = []
        yyy = []
        first = 1
        for (x,y) in xy:
            if (first == 1):
                xxx.append(x)
                yyy.append(y)
                previousx = x
                previousy = y
                first = 0
            elif math.sqrt(abs(x-previousx)**2+abs(y-previousy)**2)<50:
                xxx.append(x)
                yyy.append(y)
                previousx = x
                previousy = y
        ax.plot(xxx,yyy,linewidth=0.1,color='white')


plt.text(center_lon,ys_min + 500, city + ' ' + str(lat) + '$^\circ$N, ' + str(lon) + '$^\circ$W ', fontsize=50,verticalalignment='bottom', horizontalalignment='center',bbox={'facecolor': 'black', 'alpha': 0.5, 'pad': 10})
plt.text(center_lon, ys_min + 250, 'Imagem gerada com os trajectos do dia 10 de Outubro de 2019', fontsize=15,verticalalignment='bottom', horizontalalignment='center',bbox={'facecolor': 'black', 'alpha': 0.5, 'pad': 10})



plt.savefig(city+'_simplify.png')