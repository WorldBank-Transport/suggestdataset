command = '/opt/virtualenv/suggestdataset/bin/gunicorn'
pythonpath = '/opt/suggest/dataset'
bind = "127.0.0.1:8020"
workers = 3
max_requests = 10000
proc_name = 'suggestdataset'
timeout = 300
