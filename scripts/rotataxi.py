import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register

#conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
conn = psycopg2.connect("dbname=taxi_services user=joao")
register(conn)
cursor_psql = conn.cursor()

sql = "select count(taxi) from tracks, cont_aad_caop2018 where concelho='PORTO' and st_intersects(proj_track,proj_boundary)"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

for i in results:
    print(i)