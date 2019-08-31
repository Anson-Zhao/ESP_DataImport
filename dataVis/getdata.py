from influxdb import InfluxDBClient
import influxdb
import datetime
# Python and Gevent
from gevent.pywsgi import WSGIserver
from gevent import monkey
monkey.patch_all() # makes many blocking calls asynchronous


client = InfluxDBClient(host='10.11.90.15', port=8086, username="rayf", password="rayf", database="RayESP")
a = datetime.datetime.now() - datetime.timedelta(minutes=1)
client.query('SELECT "X","Y","Z","time" FROM "far"')
points = results.get_points()
for point in points:
print("Time: %s, Duration: %i" % (point['time'], point['duration']))




def application(environ, start_response):
    if environ["REQUEST_METHOD"]!="POST": # your JS uses post, so if it isn't post, it isn't you
        start_response("403 Forbidden", [("Content-Type", "text/html; charset=utf-8")])
        return "403 Forbidden"
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    r = environ["wsgi.input"].read() # get the post data
    return r

address = "youraddresshere", 8080
server = WSGIServer(address, application)
server.backlog = 256
server.serve_forever()