worker_class = "gevent"
workers = 2
timeout = 120
bind = "0.0.0.0:5000"
wsgi_app = "wsgi:app"
errorlog = "logging/error.log"
capture_output = True
loglevel = "debug"