from wsgiref import simple_server
from composites.app import app

httpd = simple_server.make_server('0.0.0.0', 1234, app)
httpd.serve_forever()
