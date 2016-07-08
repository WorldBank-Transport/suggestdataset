command = '/var/virtualenvs/odp/bin/gunicorn'
pythonpath = '/apps/odp'
bind = "127.0.0.1:9027"
workers = 3
worker_class = 'gaiohttp'
max_requests = 10000
proc_name = 'odp'
timeout = 300
