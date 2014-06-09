# gunicorn config file
 
pidfile = '/tmp/stock.pid'
debug = True
workers = 2
bind = '0.0.0.0:8001'
logfile = '/var/log/stock/gunicorn.log'
loglevel = 'debug'